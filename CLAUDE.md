# kanolab-web の作業ルール

- 本番サイト（GitHub Pages）は `main` ブランチから公開される。`main` へのpushは即公開になる。
- サイトの変更は、まず `preview` ブランチにコミットしてpushし、`bash tools/deploy_preview.sh` で確認用サイト（https://keikanolab.github.io/kanolab-web-preview/）を更新する。
- 本番（`main`）へのマージとpushは、加納先生から公開のOK（「公開して」「pushして」など）が出てから行う。
- 公開後は `preview` を `main` と同じ状態にそろえておく。
- ページのタイトル・説明・URLを変えたら `python3 tools/add_seo.py` を実行して、canonical、hreflang、サイトマップを作り直す。
- 詳しくは README.ja.md の「公開前の確認」を参照。
