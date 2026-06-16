from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Admin, Book, Category, DownloadLink
from app.schemas import (
    BookCreate,
    BookDetailOut,
    BookListOut,
    BookUpdate,
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    LoginRequest,
    PageResult,
    StatsOut,
    TokenResponse,
)
from app.utils.auth import create_access_token, verify_password
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=TokenResponse)
def admin_login(data: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_access_token({"sub": admin.username})
    return TokenResponse(access_token=token)


@router.get("/stats", response_model=StatsOut)
def get_stats(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_books = db.query(func.count(Book.id)).scalar() or 0
    published_books = db.query(func.count(Book.id)).filter(Book.is_published.is_(True)).scalar() or 0
    total_downloads = db.query(func.coalesce(func.sum(Book.download_count), 0)).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    return StatsOut(
        total_books=total_books,
        published_books=published_books,
        total_downloads=int(total_downloads),
        total_categories=total_categories,
    )


# ---------- Categories ----------
@router.get("/categories", response_model=list[CategoryOut])
def admin_list_categories(_: Admin = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.sort_order, Category.id).all()


@router.post("/categories", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    if db.query(Category).filter((Category.name == data.name) | (Category.slug == data.slug)).first():
        raise HTTPException(status_code=400, detail="分类名称或标识已存在")
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    db.delete(category)
    db.commit()
    return {"message": "删除成功"}


# ---------- Books ----------
def _save_download_links(book: Book, links_data: list, db: Session):
    db.query(DownloadLink).filter(DownloadLink.book_id == book.id).delete()
    for link_data in links_data:
        link = DownloadLink(book_id=book.id, **link_data.model_dump())
        db.add(link)


@router.get("/books", response_model=PageResult)
def admin_list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    keyword: str = Query("", max_length=100),
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Book).options(joinedload(Book.category))

    if keyword.strip():
        kw = f"%{keyword.strip()}%"
        query = query.filter(Book.title.like(kw) | Book.author.like(kw))

    total = query.count()
    items = (
        query.order_by(Book.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PageResult(
        items=[BookListOut.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/books/{book_id}", response_model=BookDetailOut)
def admin_get_book(
    book_id: int,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    book = (
        db.query(Book)
        .options(joinedload(Book.category), joinedload(Book.download_links))
        .filter(Book.id == book_id)
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    return BookDetailOut.model_validate(book)


@router.post("/books", response_model=BookDetailOut)
def create_book(
    data: BookCreate,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    book_data = data.model_dump(exclude={"download_links"})
    book = Book(**book_data)
    db.add(book)
    db.flush()

    if data.download_links:
        _save_download_links(book, data.download_links, db)

    db.commit()
    db.refresh(book)
    book = (
        db.query(Book)
        .options(joinedload(Book.category), joinedload(Book.download_links))
        .filter(Book.id == book.id)
        .first()
    )
    return BookDetailOut.model_validate(book)


@router.put("/books/{book_id}", response_model=BookDetailOut)
def update_book(
    book_id: int,
    data: BookUpdate,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")

    update_data = data.model_dump(exclude_unset=True, exclude={"download_links"})
    for key, value in update_data.items():
        setattr(book, key, value)

    if data.download_links is not None:
        _save_download_links(book, data.download_links, db)

    db.commit()
    book = (
        db.query(Book)
        .options(joinedload(Book.category), joinedload(Book.download_links))
        .filter(Book.id == book.id)
        .first()
    )
    return BookDetailOut.model_validate(book)


@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    _: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")

    db.delete(book)
    db.commit()
    return {"message": "删除成功"}
