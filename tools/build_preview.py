#!/usr/bin/env python3
"""公開前チェック用の確認サイトを作る。

使い方: python3 tools/build_preview.py 出力先フォルダ [表示用のコミットID]

本番サイトのファイルをコピーし、次の処理をする。
- 全ページに noindex,nofollow を入れ、robots.txt で全体のクロールを禁止する（検索に出さない）
- 全ページの先頭に「確認用（未公開）」の帯を表示する
- Search Console の所有権確認タグ、サイトマップ、llms.txt は確認用サイトには入れない
canonical や hreflang は本番URLのまま残すので、検索エンジンが確認用を本番と取り違えることはない。
"""
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git", ".github", "tools", "README.md", "README.ja.md", "sitemap.xml", "llms.txt", "CLAUDE.md"}

BANNER = (
    '<div role="note" style="background:#5b2a18;color:#fff;'
    'font:600 14px/1.5 system-ui,sans-serif;padding:8px 16px;text-align:center">'
    '確認用ページ（未公開）／Preview, not public　'
    '<span style="font-weight:400;opacity:.85">{stamp}</span></div>'
)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: build_preview.py OUT_DIR [COMMIT]")
    out = Path(sys.argv[1]).resolve()
    commit = sys.argv[2] if len(sys.argv) > 2 else ""
    if out == ROOT or ROOT in out.parents:
        sys.exit("出力先はリポジトリの外にしてください")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT, out, ignore=lambda d, names: [n for n in names if Path(d) == ROOT and n in SKIP])

    jst = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M")
    stamp = f"更新 {jst}" + (f" ・ {commit}" if commit else "")
    pages = 0
    for page in out.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        text = re.sub(r'\s*<meta name="google-site-verification"[^>]*>', "", text)
        text = re.sub(r'\s*<meta name="robots"[^>]*>', "", text)
        text, n = re.subn(r"<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">', text, count=1)
        if n != 1:
            sys.exit(f"<head> が見つかりません: {page}")
        text, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n  " + BANNER.format(stamp=stamp), text, count=1)
        if n != 1:
            sys.exit(f"<body> が見つかりません: {page}")
        page.write_text(text, encoding="utf-8")
        pages += 1
    (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print(f"確認用サイトを作成しました: {out}（{pages}ページ）")


if __name__ == "__main__":
    main()
