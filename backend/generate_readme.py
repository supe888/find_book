"""
生成 GitHub 格式的网站 README（含全部图书下载链接）

用法:
  python generate_readme.py
  python generate_readme.py --output ../README.md
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.book_classifier import CATEGORY_DEFINITIONS, classify_title
from app.services.book_parser import parse_file

SITE_NAME = "自由图书"
SITE_DESC = "免费电子书资源分享平台，支持夸克网盘、城通网盘直接下载"


def format_download_link(url: str, extract_code: str) -> str:
    link = f"[⬇️ 下载]({url})"
    if extract_code:
        link += f" `提取码:{extract_code}`"
    return link


def escape_table_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def generate_readme(file_path: str, output_path: str):
    print(f"解析: {file_path}")
    books = parse_file(file_path)
    print(f"共 {len(books)} 本图书")

    by_category: dict[str, list] = defaultdict(list)
    slug_to_name = {c["slug"]: c["name"] for c in CATEGORY_DEFINITIONS}

    for book in books:
        slug = classify_title(book.title)
        by_category[slug].append(book)

    lines: list[str] = []
    lines.append(f"# {SITE_NAME}")
    lines.append("")
    lines.append(f"<p align=\"center\">")
    lines.append(f"  <strong>{SITE_NAME}</strong> — {SITE_DESC}")
    lines.append(f"</p>")
    lines.append("")
    lines.append("<p align=\"center\">")
    lines.append(f"  📚 共 <strong>{len(books)}</strong> 本电子书 &nbsp;|&nbsp; 🔗 点击即可跳转网盘下载 &nbsp;|&nbsp; 🛠️ [本地部署](docs/SETUP.md)")
    lines.append("</p>")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📖 目录")
    lines.append("")

    ordered_slugs = [c["slug"] for c in CATEGORY_DEFINITIONS]
    for slug in ordered_slugs:
        items = by_category.get(slug, [])
        if items:
            name = slug_to_name.get(slug, slug)
            anchor = name
            lines.append(f"- [{name}（{len(items)} 本）](#{anchor})")

    lines.append("")
    lines.append("---")
    lines.append("")

    for slug in ordered_slugs:
        items = by_category.get(slug, [])
        if not items:
            continue
        name = slug_to_name.get(slug, slug)
        lines.append(f"## {name}")
        lines.append("")
        lines.append(f"> 共 {len(items)} 本")
        lines.append("")
        lines.append("| # | 书名 | 格式 | 网盘 | 下载 |")
        lines.append("|:-:|------|:----:|:----:|------|")

        for idx, book in enumerate(sorted(items, key=lambda b: b.title), 1):
            title = escape_table_cell(book.title)
            dl = format_download_link(book.link_url, book.extract_code)
            lines.append(
                f"| {idx} | {title} | {book.file_format} | {book.platform} | {dl} |"
            )

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## 关于")
    lines.append("")
    lines.append(f"**{SITE_NAME}** 是一个开源电子书索引项目，所有资源均来自公开网盘分享链接。")
    lines.append("")
    lines.append("> ⚠️ 本站仅提供索引服务，不存储任何电子书文件。如有侵权请联系删除。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"<p align=\"center\">{SITE_NAME} © 2026</p>")
    lines.append("")

    output = Path(output_path)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成: {output} ({output.stat().st_size // 1024} KB)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        default=str(Path(__file__).parent.parent / "电子书链接.txt"),
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).parent.parent / "README.md"),
    )
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"错误: 文件不存在 {args.file}")
        sys.exit(1)

    generate_readme(args.file, args.output)


if __name__ == "__main__":
    main()
