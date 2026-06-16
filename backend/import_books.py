"""
从 电子书链接.txt 导入图书数据到数据库

用法:
  python import_books.py
  python import_books.py --file ../电子书链接.txt
  python import_books.py --clear   # 清空已有图书后导入
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal
from app.models import Book, Category, DownloadLink
from app.services.book_classifier import CATEGORY_DEFINITIONS, classify_title, get_cover_url
from app.services.book_parser import parse_file


def ensure_categories(db) -> dict[str, int]:
    slug_to_id: dict[str, int] = {}
    existing = {c.slug: c for c in db.query(Category).all()}

    for cat_def in CATEGORY_DEFINITIONS:
        if cat_def["slug"] in existing:
            slug_to_id[cat_def["slug"]] = existing[cat_def["slug"]].id
        else:
            category = Category(
                name=cat_def["name"],
                slug=cat_def["slug"],
                sort_order=cat_def["sort_order"],
            )
            db.add(category)
            db.flush()
            slug_to_id[cat_def["slug"]] = category.id
            print(f"  + 创建分类: {cat_def['name']}")

    return slug_to_id


def import_books(file_path: str, clear: bool = False, batch_size: int = 200):
    print(f"解析文件: {file_path}")
    parsed = parse_file(file_path)
    print(f"解析到 {len(parsed)} 条图书记录（已去重）")

    db = SessionLocal()
    try:
        if clear:
            count = db.query(Book).count()
            db.query(DownloadLink).delete()
            db.query(Book).delete()
            db.commit()
            print(f"已清空 {count} 本现有图书")

        print("同步分类...")
        slug_to_id = ensure_categories(db)
        db.commit()

        existing_urls = {
            row[0]
            for row in db.query(DownloadLink.link_url).all()
        }
        existing_titles = {
            row[0]
            for row in db.query(Book.title).all()
        }

        imported = 0
        skipped = 0
        category_stats: dict[str, int] = {}

        for i, item in enumerate(parsed):
            if item.link_url in existing_urls:
                skipped += 1
                continue

            slug = classify_title(item.title)
            category_id = slug_to_id.get(slug, slug_to_id.get("other"))
            category_stats[slug] = category_stats.get(slug, 0) + 1

            book = Book(
                title=item.title,
                author=item.author,
                cover_url=get_cover_url(slug),
                description=f"《{item.title}》电子书资源，支持{item.platform}下载。",
                category_id=category_id,
                tags=slug,
                file_format=item.file_format,
                file_size="",
                is_published=True,
            )
            db.add(book)
            db.flush()

            link = DownloadLink(
                book_id=book.id,
                platform=item.platform,
                link_url=item.link_url,
                extract_code=item.extract_code,
                is_primary=True,
            )
            db.add(link)

            existing_urls.add(item.link_url)
            existing_titles.add(item.title)
            imported += 1

            if imported % batch_size == 0:
                db.commit()
                print(f"  已导入 {imported} 本...")

        db.commit()

        print("\n导入完成!")
        print(f"  新增: {imported} 本")
        print(f"  跳过(重复): {skipped} 本")
        print("\n分类统计:")
        for cat_def in CATEGORY_DEFINITIONS:
            count = category_stats.get(cat_def["slug"], 0)
            if count:
                print(f"  {cat_def['name']}: {count} 本")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="导入电子书链接到数据库")
    parser.add_argument(
        "--file",
        default=str(Path(__file__).parent.parent / "电子书链接.txt"),
        help="电子书链接文件路径",
    )
    parser.add_argument("--clear", action="store_true", help="导入前清空所有图书")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"错误: 文件不存在 {file_path}")
        sys.exit(1)

    import_books(str(file_path), clear=args.clear)


if __name__ == "__main__":
    main()
