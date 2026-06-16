from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ---------- Category ----------
class CategoryBase(BaseModel):
    name: str
    slug: str
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    sort_order: Optional[int] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------- Download Link ----------
class DownloadLinkBase(BaseModel):
    platform: str
    link_url: str
    extract_code: str = ""
    password: str = ""
    is_primary: bool = False


class DownloadLinkCreate(DownloadLinkBase):
    pass


class DownloadLinkOut(DownloadLinkBase):
    id: int
    book_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DownloadLinkPublic(BaseModel):
    id: int
    platform: str
    link_url: str
    extract_code: str = ""
    password: str = ""
    is_primary: bool = False

    model_config = {"from_attributes": True}


# ---------- Book ----------
class BookBase(BaseModel):
    title: str
    author: str = ""
    cover_url: str = ""
    description: str = ""
    category_id: Optional[int] = None
    tags: str = ""
    file_format: str = "PDF"
    file_size: str = ""
    is_published: bool = True


class BookCreate(BookBase):
    download_links: list[DownloadLinkCreate] = Field(default_factory=list)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    cover_url: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    file_format: Optional[str] = None
    file_size: Optional[str] = None
    is_published: Optional[bool] = None
    download_links: Optional[list[DownloadLinkCreate]] = None


class BookListOut(BaseModel):
    id: int
    title: str
    author: str
    cover_url: str
    description: str
    category_id: Optional[int]
    tags: str
    file_format: str
    file_size: str
    download_count: int
    view_count: int
    is_published: bool
    created_at: datetime
    category: Optional[CategoryOut] = None

    model_config = {"from_attributes": True}


class BookDetailOut(BookListOut):
    download_links: list[DownloadLinkPublic] = Field(default_factory=list)


# ---------- Auth ----------
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Pagination ----------
class PageResult(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


class StatsOut(BaseModel):
    total_books: int
    published_books: int
    total_downloads: int
    total_categories: int
