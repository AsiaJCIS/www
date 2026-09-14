# 過去大会サイトのアーカイブ手順（docs/archive/）

`docs/archive/YYYY-country/` に 2006〜2026 の全大会サイトの静的コピーを置いている。
`docs/index.md` の Past Conferences 表から `archive/YYYY-country/index.html` でリンク。

## 方針
- **写真（集合写真・会場スナップ等のギャラリー）は保存しない。** ギャラリーページ・画像は削除し、
  リンクは Wayback Machine の該当URLに向けている（2008 gallery.html, 2009 photo/, 2011 photo.html）。
- 論文PDF・CFP・プログラム等の資料はそのまま保持。
- **外部トラッカー・外部スクリプトは載せない。** アナリティクス、Cookie 同意バナー（Osano/IEEE）、
  Facebook SDK、Google Sites の viewer JS などは削除済み（削除箇所には HTML コメントを残している）。
  Wayback に存在しないファイルへの `<script>`/`<link>` も削除。残している外部参照は
  Google Fonts（2019/2020/2023/2025）、Google Sites の CSS（2011）、Google Maps の埋め込み iframe のみ。
  追加時は `grep -rhoiE '<(script|link|iframe)[^>]+(src|href)="(https?:)?//[^"/]+' docs/archive` で確認。
- 原サイトが生きている年は wget、死んでいる年は Wayback からの復元（`_wayback_manifest.json` に取得元と時刻を記録）。

## 取得方法
### 原サイトが生きている場合（例: 2012 は明大・菊池研に移設されて現存）
```sh
cd docs/archive && mkdir -p 2012-japan
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
     -nH --cut-dirs=1 -e robots=off --wait=0.5 -P 2012-japan \
     "https://www.kikn.fms.meiji.ac.jp/ASIAJCIS2012/"
```

### Wayback Machine から復元する場合
```sh
uv run --with requests,beautifulsoup4 tools/wayback_mirror.py \
    --out docs/archive/2021-korea --start http://asiajcis2021.sch.ac.kr/ --ts 20211021181036
```
- `--ts` は優先するキャプチャ時刻（大会終了直後あたり）。Wayback が最寄りのキャプチャに解決する。
- start URL から同一ホスト内のページ・画像・CSS・PDF をたどって取得し、リンクを相対パスに書き換える。
  Wayback に無いものへのリンクは Wayback の閲覧URLに向ける。
- 本体が別パス／別ホストにある場合は start を変える（2013 は `asiajcis.org/2013/`、2008 は
  `cs.sookmyung.ac.kr/~rhee/jwis2008/` が `esslab.hanyang.ac.kr/jwis2008/` へリダイレクトしていた）。
- キャプチャの有無は CDX API で確認できる:
  `https://web.archive.org/cdx/search/cdx?url=HOST/PATH/*&filter=statuscode:200&collapse=urlkey&fl=original,timestamp`
- Wayback は時々 "Temporarily Offline" / 429 を返す。スクリプトはリトライするが、失敗が多い時は時間を置く。

## 各年の取得元と状態（2026-09-14 時点）
| 年 | 取得元 | 状態 |
|---|---|---|
| 2026〜2023, 2019 | 原サイト（wget） | 完全 |
| 2022 | Wayback 2022-04-04 | index のみ（原サイトは河北大CMSから消滅） |
| 2021 | Wayback | 全ページ＋PDF。画像・CSS は Wayback に無い |
| 2020, 2018 | Wayback | index のみ（それしか無い） |
| 2017, 2016, 2015, 2014, 2010, 2007 | Wayback | ほぼ全ページ |
| 2013 | Wayback（asiajcis.org/2013/） | index のみ現存 |
| 2012 | 明大・菊池研の現存コピー（wget） | 完全 |
| 2011 | Wayback（Google Sites） | 全ページ、写真ページは除外 |
| 2009 | Wayback（OJS 系サイト） | 138ページ＋論文PDF。写真ギャラリー(469MB zip 含む)は除外 |
| 2008 | Wayback（esslab.hanyang.ac.kr） | 全ページ、gallery は除外 |
| 2006 | Wayback | index + program の3ページ |
