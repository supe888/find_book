from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Book, Category, DownloadLink
from app.schemas import (
    BookDetailOut,
    BookListOut,
    DownloadLinkPublic,
    PageResult,
)

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    results = (
        db.query(Category, func.count(Book.id).label("book_count"))
        .outerjoin(Book, (Book.category_id == Category.id) & Book.is_published.is_(True))
        .group_by(Category.id)
        .order_by(Category.sort_order, Category.id)
        .all()
    )
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "sort_order": cat.sort_order,
            "book_count": count,
        }
        for cat, count in results
        if count > 0
    ]


@router.get("/stats")
def public_stats(db: Session = Depends(get_db)):
    total_books = db.query(func.count(Book.id)).filter(Book.is_published.is_(True)).scalar() or 0
    total_categories = db.query(func.count(Category.id)).scalar() or 0
    total_downloads = db.query(func.coalesce(func.sum(Book.download_count), 0)).scalar() or 0
    return {
        "total_books": total_books,
        "total_categories": total_categories,
        "total_downloads": int(total_downloads),
    }


@router.get("/books", response_model=PageResult)
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    keyword: str = Query("", max_length=100),
    category_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(Book.is_published.is_(True))
    )

    if keyword.strip():
        kw = f"%{keyword.strip()}%"
        query = query.filter(or_(Book.title.like(kw), Book.author.like(kw), Book.tags.like(kw)))

    if category_id:
        query = query.filter(Book.category_id == category_id)

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


@router.get("/books/hot", response_model=list[BookListOut])
def hot_books(limit: int = Query(8, ge=1, le=20), db: Session = Depends(get_db)):
    items = (
        db.query(Book)
        .options(joinedload(Book.category))
        .filter(Book.is_published.is_(True))
        .order_by(Book.download_count.desc(), Book.view_count.desc())
        .limit(limit)
        .all()
    )
    return [BookListOut.model_validate(item) for item in items]


@router.get("/books/{book_id}", response_model=BookDetailOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = (
        db.query(Book)
        .options(joinedload(Book.category), joinedload(Book.download_links))
        .filter(Book.id == book_id, Book.is_published.is_(True))
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")

    book.view_count += 1
    db.commit()
    db.refresh(book)
    return BookDetailOut.model_validate(book)


@router.post("/books/{book_id}/download", response_model=DownloadLinkPublic)
def record_download(book_id: int, link_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.is_published.is_(True)).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")

    link = (
        db.query(DownloadLink)
        .filter(DownloadLink.id == link_id, DownloadLink.book_id == book_id)
        .first()
    )
    if not link:
        raise HTTPException(status_code=404, detail="下载链接不存在")

    book.download_count += 1
    db.commit()
    db.refresh(link)
    return DownloadLinkPublic.model_validate(link)
