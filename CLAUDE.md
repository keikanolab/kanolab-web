# kanolab-web の作業ルール

- 公開は GitHub Actions（`.github/workflows/deploy.yml`）が行う。`main` の内容が本番サイト（https://keikanolab.github.io/kanolab-web/）、`preview` の内容が確認用ページ（https://keikanolab.github.io/kanolab-web/preview/）になる。
- サイトの変更は、まず `preview` ブランチにコミットしてpushし、確認用ページで確認してもらう。`main` へのpushは即公開になる。
- 本番（`main`）へのマージとpushは、加納先生から公開のOK（「公開して」「pushして」など）が出てから行う。
- 公開後は `preview` を `main` と同じ状態にそろえておく。
- ページのタイトル・説明・URLを変えたら `python3 tools/add_seo.py` を実行して、canonical、hreflang、サイトマップを作り直す。
- 詳しくは README.ja.md の「公開前の確認」を参照。
