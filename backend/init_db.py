"""Initialize database with seed data."""

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Admin, Book, Category, DownloadLink
from app.utils.auth import get_password_hash


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Admin).count() == 0:
            admin = Admin(
                username=settings.admin_username,
                password_hash=get_password_hash(settings.admin_password),
            )
            db.add(admin)
            print(f"Created admin: {settings.admin_username} / {settings.admin_password}")

        if db.query(Category).count() == 0:
            categories = [
                Category(name="计算机", slug="computer", sort_order=1),
                Category(name="文学", slug="literature", sort_order=2),
                Category(name="历史", slug="history", sort_order=3),
                Category(name="科幻", slug="sci-fi", sort_order=4),
                Category(name="经济管理", slug="business", sort_order=5),
            ]
            db.add_all(categories)
            db.flush()

            sample_books = [
                {
                    "title": "深入理解计算机系统",
                    "author": "Randal E. Bryant",
                    "cover_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400",
                    "description": "计算机系统领域的经典教材，从程序员视角深入理解计算机系统的工作原理。",
                    "category_id": categories[0].id,
                    "tags": "计算机,系统,编程",
                    "file_format": "PDF",
                    "file_size": "25MB",
                    "download_count": 128,
                    "view_count": 520,
                    "links": [
                        {"platform": "百度网盘", "link_url": "https://pan.baidu.com/s/example1", "extract_code": "abc1", "is_primary": True},
                        {"platform": "夸克网盘", "link_url": "https://pan.quark.cn/s/example1", "extract_code": "", "is_primary": False},
                    ],
                },
                {
                    "title": "三体",
                    "author": "刘慈欣",
                    "cover_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
                    "description": "中国科幻文学的里程碑之作，讲述地球文明与三体文明的恢宏史诗。",
                    "category_id": categories[3].id,
                    "tags": "科幻,小说,雨果奖",
                    "file_format": "EPUB",
                    "file_size": "2.5MB",
                    "download_count": 356,
                    "view_count": 1200,
                    "links": [
                        {"platform": "百度网盘", "link_url": "https://pan.baidu.com/s/example2", "extract_code": "xyz9", "is_primary": True},
                    ],
                },
                {
                    "title": "人类简史",
                    "author": "尤瓦尔·赫拉利",
                    "cover_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7c?w=400",
                    "description": "从认知革命到科学革命，讲述人类如何成为地球主宰的宏大历史。",
                    "category_id": categories[2].id,
                    "tags": "历史,人文,畅销",
                    "file_format": "PDF",
                    "file_size": "8MB",
                    "download_count": 89,
                    "view_count": 340,
                    "links": [
                        {"platform": "阿里云盘", "link_url": "https://www.alipan.com/s/example3", "extract_code": "", "is_primary": True},
                    ],
                },
                {
                    "title": "百年孤独",
                    "author": "加西亚·马尔克斯",
                    "cover_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400",
                    "description": "魔幻现实主义文学代表作，布恩迪亚家族七代人的传奇故事。",
                    "category_id": categories[1].id,
                    "tags": "文学,经典,诺贝尔",
                    "file_format": "EPUB",
                    "file_size": "1.8MB",
                    "download_count": 210,
                    "view_count": 680,
                    "links": [
                        {"platform": "百度网盘", "link_url": "https://pan.baidu.com/s/example4", "extract_code": "book4", "is_primary": True},
                        {"platform": "123云盘", "link_url": "https://www.123pan.com/s/example4", "extract_code": "", "is_primary": False},
                    ],
                },
                {
                    "title": "穷查理宝典",
                    "author": "查理·芒格",
                    "cover_url": "https://images.unsplash.com/photo-1553729450-efb1c8d1d8e2?w=400",
                    "description": "查理·芒格的智慧箴言录，投资与人生的多元思维模型。",
                    "category_id": categories[4].id,
                    "tags": "投资,商业,思维",
                    "file_format": "PDF",
                    "file_size": "12MB",
                    "download_count": 67,
                    "view_count": 290,
                    "links": [
                        {"platform": "夸克网盘", "link_url": "https://pan.quark.cn/s/example5", "extract_code": "mm88", "is_primary": True},
                    ],
                },
                {
                    "title": "JavaScript高级程序设计",
                    "author": "Matt Frisbie",
                    "cover_url": "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=400",
                    "description": "前端开发红宝书，全面介绍 JavaScript 语言核心及 Web 开发技术。",
                    "category_id": categories[0].id,
                    "tags": "JavaScript,前端,编程",
                    "file_format": "PDF",
                    "file_size": "35MB",
                    "download_count": 445,
                    "view_count": 1500,
                    "links": [
                        {"platform": "百度网盘", "link_url": "https://pan.baidu.com/s/example6", "extract_code": "js44", "is_primary": True},
                    ],
                },
            ]

            for item in sample_books:
                links = item.pop("links")
                book = Book(**item)
                db.add(book)
                db.flush()
                for link_data in links:
                    db.add(DownloadLink(book_id=book.id, **link_data))

            print(f"Created {len(categories)} categories and {len(sample_books)} sample books")

        db.commit()
        print("Database initialized successfully!")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
