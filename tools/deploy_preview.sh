#!/usr/bin/env bash
# 確認用サイト（keikanolab/kanolab-web-preview）を、今の作業内容で更新する。
# 使い方: bash tools/deploy_preview.sh
# 本番サイト（main）には何も反映しない。確認用リポジトリは毎回まるごと置き換える。
set -euo pipefail
cd "$(dirname "$0")/.."
PREVIEW_REPO="${PREVIEW_REPO:-https://github.com/keikanolab/kanolab-web-preview}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

COMMIT="$(git rev-parse --short HEAD)"
if ! git diff --quiet HEAD; then COMMIT="$COMMIT+未コミットの変更"; fi
python3 tools/build_preview.py "$WORK/site" "$COMMIT"

cd "$WORK/site"
git init -q -b main
git add -A
git -c user.name="Claude" -c user.email="noreply@anthropic.com" \
    commit -q -m "確認用サイトを更新（元: kanolab-web $COMMIT）"
git push -q --force "$PREVIEW_REPO" main
echo "確認用サイトを更新しました: https://keikanolab.github.io/kanolab-web-preview/"
