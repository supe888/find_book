"""解析电子书链接文本文件"""

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse


@dataclass
class ParsedBook:
    title: str
    author: str
    file_format: str
    link_url: str
    platform: str
    extract_code: str


TITLE_EXT_RE = re.compile(r"^(.+?)\.(epub|pdf|mobi|azw3)\s*:?\s*$", re.IGNORECASE)
LINK_LINE_RE = re.compile(r"^链接[：:]\s*(https?://\S+)", re.IGNORECASE)
AUTHOR_PATTERNS = [
    re.compile(r"作者[：:]\s*([^\s，,。.]+)"),
    re.compile(r"——\s*([^\s，,。.]+)\s*$"),
    re.compile(r"[-—]\s*([A-Za-z\u4e00-\u9fff]{2,10})\s*$"),
]


def detect_platform(url: str) -> str:
    url_lower = url.lower()
    if "quark" in url_lower:
        return "夸克网盘"
    if "ctfile" in url_lower:
        return "城通网盘"
    if "baidu" in url_lower or "pan.baidu" in url_lower:
        return "百度网盘"
    if "alipan" in url_lower or "aliyundrive" in url_lower:
        return "阿里云盘"
    if "123pan" in url_lower:
        return "123云盘"
    if "lanzou" in url_lower or "lanzoux" in url_lower:
        return "蓝奏云"
    return "网盘"


def extract_code_from_url(url: str) -> str:
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if "p" in params and params["p"]:
        return params["p"][0]
    return ""


def parse_author_title(raw_title: str) -> tuple[str, str]:
    title = raw_title.strip()
    author = ""

    for pattern in AUTHOR_PATTERNS:
        match = pattern.search(title)
        if match:
            author = match.group(1).strip()
            title = pattern.sub("", title).strip(" -—：:")
            break

    return title, author


def parse_file(file_path: str) -> list[ParsedBook]:
    with open(file_path, encoding="utf-8") as f:
        lines = [line.rstrip("\n\r") for line in f]

    items: list[ParsedBook] = []
    seen: set[tuple[str, str]] = set()
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        title_match = TITLE_EXT_RE.match(line)
        if not title_match:
            i += 1
            continue

        raw_title = title_match.group(1).strip()
        file_format = title_match.group(2).upper()
        url = ""

        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("http"):
                url = next_line
            else:
                link_match = LINK_LINE_RE.match(next_line)
                if link_match:
                    url = link_match.group(1)

        if url:
            title, author = parse_author_title(raw_title)
            key = (title, url)
            if key not in seen:
                seen.add(key)
                platform = detect_platform(url)
                extract_code = extract_code_from_url(url) if platform == "城通网盘" else ""
                items.append(
                    ParsedBook(
                        title=title[:250],
                        author=author[:250],
                        file_format=file_format,
                        link_url=url,
                        platform=platform,
                        extract_code=extract_code,
                    )
                )
            i += 2
            continue

        i += 1

    return items
