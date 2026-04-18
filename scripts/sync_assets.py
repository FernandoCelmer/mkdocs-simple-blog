from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path
from urllib.request import urlretrieve


ROOT = Path(__file__).resolve().parent.parent

SRC_CSS = ROOT / "assets" / "css"
SRC_JS = ROOT / "assets" / "js"

BUILD_CSS = ROOT / "mkdocs_simple_blog" / "assets" / "css"
BUILD_JS = ROOT / "mkdocs_simple_blog" / "assets" / "js"

SIMPLE_BLOG_UI_VERSION = "0.4.0"
SIMPLE_BLOG_UI_LOCAL = ROOT.parent / "simple-blog-ui"

EXTERNAL_CSS: dict[str, str] = {}
EXTERNAL_JS: dict[str, str] = {}


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, dest)


def _bundle_from_pkg(
    pkg: Path,
    js_dest: Path,
    style_dest: Path,
    tokens_dest: Path,
) -> None:
    js_dest.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "npx", "--yes", "esbuild",
            str(pkg / "dist" / "index.js"),
            "--bundle",
            "--format=esm",
            "--platform=browser",
            "--minify",
            f"--outfile={js_dest}",
        ],
        check=True,
        capture_output=True,
    )

    style_dest.parent.mkdir(parents=True, exist_ok=True)

    main_text = (pkg / "src" / "styles" / "main.css").read_text()
    main_text = re.sub(
        r'@import url\(["\']\./root\.css["\']\);\s*',
        "",
        main_text,
    )

    style_dest.write_text(minify_css(main_text))

    tokens_text = (pkg / "src" / "styles" / "root.css").read_text()
    tokens_dest.write_text(minify_css(tokens_text))


def bundle_simple_blog_ui(
    version: str,
    js_dest: Path,
    style_dest: Path,
    tokens_dest: Path,
    local_path: Path | None = None,
) -> None:
    if local_path and local_path.exists():
        _bundle_from_pkg(local_path, js_dest, style_dest, tokens_dest)
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        (tmp_path / "package.json").write_text(
            '{"name":"_sync","version":"0.0.0","private":true}'
        )

        subprocess.run(
            ["npm", "install", "--silent", f"simple-blog-ui@{version}"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )

        pkg = tmp_path / "node_modules" / "simple-blog-ui"
        _bundle_from_pkg(pkg, js_dest, style_dest, tokens_dest)


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,>])\s*", r"\1", text)
    text = re.sub(r";}", "}", text)
    return text.strip()


def sync_css() -> None:
    BUILD_CSS.mkdir(parents=True, exist_ok=True)

    for src in sorted(SRC_CSS.glob("*.css")):
        dst = BUILD_CSS / (src.stem + ".min.css")
        dst.write_text(minify_css(src.read_text()))


def sync_js() -> None:
    BUILD_JS.mkdir(parents=True, exist_ok=True)

    for src in sorted(SRC_JS.glob("*.js")):
        dst = BUILD_JS / (src.stem + ".min.js")
        subprocess.run(
            [
                "npx", "--yes", "esbuild",
                str(src),
                "--minify",
                f"--outfile={dst}",
            ],
            check=True,
            capture_output=True,
        )


def main() -> None:
    for name, url in EXTERNAL_CSS.items():
        download(url, BUILD_CSS / name)

    for name, url in EXTERNAL_JS.items():
        download(url, BUILD_JS / name)

    sync_css()
    sync_js()

    bundle_simple_blog_ui(
        SIMPLE_BLOG_UI_VERSION,
        BUILD_JS / "simple-blog-ui.min.js",
        BUILD_CSS / "style.min.css",
        BUILD_CSS / "tokens.min.css",
        local_path=SIMPLE_BLOG_UI_LOCAL,
    )


if __name__ == "__main__":
    main()
