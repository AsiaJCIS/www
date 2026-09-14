#!/usr/bin/env python3
"""Wayback Machine から過去の AsiaJCIS/JWIS サイトをローカルにミラーする。

使い方:
    uv run --with requests,beautifulsoup4 www/tools/wayback_mirror.py \
        --out www/docs/archive/2021-korea \
        --start http://asiajcis2021.sch.ac.kr/ \
        --ts 20211021181036

- start URL から同一ホスト内のリンク・画像・CSS・JS をたどって取得する
- 取得は Wayback の `id_` エンドポイント（Wayback のツールバー等が入らない生データ）
- HTML/CSS 内のリンクは取得できたものだけ相対パスに書き換え、
  取れなかったものは Wayback の URL に向けておく（オンラインなら辿れる）
- ページ（HTML）は --scope（既定: start URL のディレクトリ）配下だけをたどる。
  画像・CSS・JS は同一ホストならどこでも取る
"""
import argparse
import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup

WB = "https://web.archive.org/web/{ts}id_/{url}"
WB_VIEW = "https://web.archive.org/web/{ts}/{url}"
UA = "Mozilla/5.0 (AsiaJCIS archive mirror; contact via asiajcis.github.io)"

ASSET_ATTRS = [
    ("img", "src"), ("script", "src"), ("link", "href"), ("iframe", "src"),
    ("frame", "src"), ("embed", "src"), ("object", "data"), ("input", "src"),
    ("source", "src"), ("video", "src"), ("audio", "src"), ("track", "src"),
    ("body", "background"), ("table", "background"), ("td", "background"),
    ("img", "lowsrc"),
]
LINK_ATTRS = [("a", "href"), ("area", "href"), ("form", "action")]
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)", re.I)
CSS_IMPORT_RE = re.compile(r"@import\s+(['\"])([^'\"]+)\1", re.I)
HTML_EXT = {".html", ".htm", ".php", ".asp", ".aspx", ".jsp", ".cgi", ".shtml", ""}


def norm_host(u):
    h = urlsplit(u).hostname or ""
    return h.lower().removeprefix("www.")


def clean_url(u):
    """フラグメント除去・:80 除去・%7E→~ など、比較用に正規化"""
    u = u.split("#", 1)[0].strip()
    u = re.sub(r"^(https?://[^/:]+):80(?=/|$)", r"\1", u)
    u = u.replace("%7E", "~").replace("%7e", "~")
    return u


def local_path_for(url, base_prefix):
    """元URL → アーカイブ内の相対パス"""
    sp = urlsplit(url)
    path = unquote(sp.path)
    host = norm_host(url)
    # 同一ホストの base_prefix 配下は prefix を剥がす。それ以外は _host/<host>/ 以下に置く
    bp = urlsplit(base_prefix).path
    if not bp.endswith("/"):
        bp = bp.rsplit("/", 1)[0] + "/"
    if host == norm_host(base_prefix) and path.startswith(bp):
        rel = path[len(bp):]
    elif host == norm_host(base_prefix):
        rel = "_root" + path
    else:
        rel = "_host/" + host + path
    if rel.endswith("/") or rel == "":
        rel += "index.html"
    if sp.query:
        stem, ext = os.path.splitext(rel)
        q = re.sub(r"[^A-Za-z0-9._=-]+", "_", sp.query)[:80]
        rel = f"{stem}__{q}{ext or '.html'}"
    # 拡張子なし・サーバサイドスクリプトは .html を付ける（ローカルで開けるように）
    stem, ext = os.path.splitext(rel)
    if ext.lower() in (".php", ".asp", ".aspx", ".jsp", ".cgi", ".shtml"):
        rel = rel + ".html"
    elif ext == "":
        rel = rel + ".html"
    return rel.replace("\\", "/").lstrip("/")


class Mirror:
    def __init__(self, out, start, ts, scope, max_items, delay):
        self.out = out
        self.start = clean_url(start)
        self.ts = ts
        self.scope = scope or self.start
        self.host = norm_host(self.start)
        self.max_items = max_items
        self.delay = delay
        self.sess = requests.Session()
        self.sess.headers["User-Agent"] = UA
        self.done = {}      # url -> dict(local, ts, status, type)
        self.failed = {}    # url -> reason
        self.queue = [self.start]
        self.pending_html = []  # (url, local, bytes) 後で書き換える
        self.pending_css = []

    # ---------- fetch ----------
    def fetch(self, url):
        wb = WB.format(ts=self.ts, url=url)
        last = None
        for attempt in range(6):
            try:
                r = self.sess.get(wb, timeout=60, allow_redirects=True)
            except requests.RequestException as e:
                last = f"exc {e.__class__.__name__}"
                time.sleep(3 * (attempt + 1))
                continue
            if r.status_code == 200 and b"Internet Archive: Temporarily Offline" not in r.content[:2000]:
                m = re.search(r"/web/(\d{14})id_/(.*)$", r.url)
                real_ts = m.group(1) if m else self.ts
                return r, real_ts
            if r.status_code == 404:
                return None, "404 not in wayback"
            last = f"HTTP {r.status_code}"
            time.sleep(5 * (attempt + 1) if r.status_code in (429, 503) else 2)
        return None, last

    def in_host(self, url):
        return norm_host(url) == self.host

    def in_scope(self, url):
        return self.in_host(url) and clean_url(url).startswith(self.scope.rsplit("/", 1)[0] + "/")

    def enqueue(self, url, is_page):
        url = clean_url(url)
        if not url.startswith("http"):
            return
        if url in self.done or url in self.failed or url in self.queue:
            return
        if is_page and not self.in_scope(url):
            return
        if not is_page and not self.in_host(url):
            return
        self.queue.append(url)

    # ---------- link extraction ----------
    def extract_html(self, url, html_bytes):
        soup = BeautifulSoup(html_bytes, "html.parser")
        base = url
        if soup.base and soup.base.get("href"):
            base = urljoin(url, soup.base["href"])
        for tag, attr in ASSET_ATTRS:
            for el in soup.find_all(tag):
                v = el.get(attr)
                if v and not v.startswith(("data:", "javascript:", "mailto:", "#")):
                    self.enqueue(urljoin(base, v), is_page=False)
        for tag, attr in LINK_ATTRS:
            for el in soup.find_all(tag):
                v = el.get(attr)
                if v and not v.startswith(("javascript:", "mailto:", "#", "tel:")):
                    self.enqueue(urljoin(base, v), is_page=True)
        for el in soup.find_all("meta", attrs={"http-equiv": re.compile("refresh", re.I)}):
            m = re.search(r"url\s*=\s*['\"]?([^'\"]+)", el.get("content", ""), re.I)
            if m:
                self.enqueue(urljoin(base, m.group(1)), is_page=True)
        for el in soup.find_all(style=True):
            for _, u in CSS_URL_RE.findall(el["style"]):
                self.enqueue(urljoin(base, u), is_page=False)
        for st in soup.find_all("style"):
            for _, u in CSS_URL_RE.findall(st.get_text()):
                self.enqueue(urljoin(base, u), is_page=False)

    def extract_css(self, url, text):
        for _, u in CSS_URL_RE.findall(text):
            if not u.startswith("data:"):
                self.enqueue(urljoin(url, u), is_page=False)
        for _, u in CSS_IMPORT_RE.findall(text):
            self.enqueue(urljoin(url, u), is_page=False)

    # ---------- rewrite ----------
    def target(self, from_local, abs_url, real_ts):
        """書き換え先: ローカルにあれば相対パス、なければ Wayback URL、外部はそのまま"""
        u = clean_url(abs_url)
        frag = ""
        if "#" in abs_url:
            frag = "#" + abs_url.split("#", 1)[1]
        if u in self.done:
            rel = os.path.relpath(self.done[u]["local"], os.path.dirname(from_local) or ".")
            return rel.replace(os.sep, "/") + frag
        if self.in_host(u):
            return WB_VIEW.format(ts=real_ts, url=u) + frag
        return abs_url

    def rewrite_html(self, url, local, html_bytes, real_ts):
        soup = BeautifulSoup(html_bytes, "html.parser")
        base = url
        if soup.base:
            if soup.base.get("href"):
                base = urljoin(url, soup.base["href"])
            soup.base.decompose()
        for tag, attr in ASSET_ATTRS + LINK_ATTRS:
            for el in soup.find_all(tag):
                v = el.get(attr)
                if v and not v.startswith(("data:", "javascript:", "mailto:", "#", "tel:")):
                    el[attr] = self.target(local, urljoin(base, v), real_ts)
        for el in soup.find_all("meta", attrs={"http-equiv": re.compile("refresh", re.I)}):
            c = el.get("content", "")
            m = re.search(r"(url\s*=\s*['\"]?)([^'\"]+)", c, re.I)
            if m:
                el["content"] = c[:m.start(2)] + self.target(local, urljoin(base, m.group(2)), real_ts) + c[m.end(2):]
        for el in soup.find_all(style=True):
            el["style"] = self.rewrite_css_text(local, base, el["style"], real_ts)
        for st in soup.find_all("style"):
            if st.string:
                st.string = self.rewrite_css_text(local, base, st.string, real_ts)
        # アーカイブであることを示すコメント
        note = soup.new_string(
            f" Archived copy for asiajcis.github.io. Source: {url} via Wayback Machine ({real_ts}). ")
        from bs4 import Comment
        soup.insert(0, Comment(str(note)))
        return soup.encode("utf-8")

    def rewrite_css_text(self, local, base, text, real_ts):
        def rep(m):
            u = m.group(2)
            if u.startswith("data:"):
                return m.group(0)
            return f"url({m.group(1)}{self.target(local, urljoin(base, u), real_ts)}{m.group(1)})"
        text = CSS_URL_RE.sub(rep, text)
        text = CSS_IMPORT_RE.sub(lambda m: f"@import {m.group(1)}{self.target(local, urljoin(base, m.group(2)), real_ts)}{m.group(1)}", text)
        return text

    # ---------- main ----------
    def run(self):
        while self.queue and len(self.done) + len(self.failed) < self.max_items:
            url = self.queue.pop(0)
            r, info = self.fetch(url)
            if r is None:
                self.failed[url] = info
                print(f"  FAIL {url} ({info})", flush=True)
                continue
            real_ts = info
            ctype = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
            local = local_path_for(url, self.scope)
            body = r.content
            is_html = ctype.startswith("text/html") or (ctype == "" and os.path.splitext(urlsplit(url).path)[1].lower() in HTML_EXT)
            is_css = ctype == "text/css" or urlsplit(url).path.lower().endswith(".css")
            if is_html and not local.lower().endswith((".html", ".htm")):
                local = os.path.splitext(local)[0] + ".html"
            if not is_html and local.endswith(".html") and os.path.splitext(urlsplit(url).path)[1] not in HTML_EXT:
                local = local[:-5]
            self.done[url] = {"local": local, "ts": real_ts, "type": ctype, "bytes": len(body)}
            print(f"  ok   {url} -> {local} [{ctype} {len(body)}B @{real_ts}]", flush=True)
            if is_html:
                self.extract_html(url, body)
                self.pending_html.append((url, local, body, real_ts))
            elif is_css:
                text = body.decode(r.encoding or "utf-8", errors="replace")
                self.extract_css(url, text)
                self.pending_css.append((url, local, text, real_ts))
            else:
                self.write(local, body)
            time.sleep(self.delay)
        if self.queue:
            print(f"  (max-items {self.max_items} に達したため {len(self.queue)} 件は未取得)", flush=True)
        for url, local, body, real_ts in self.pending_html:
            self.write(local, self.rewrite_html(url, local, body, real_ts))
        for url, local, text, real_ts in self.pending_css:
            base = url
            self.write(local, self.rewrite_css_text(local, base, text, real_ts).encode("utf-8"))
        manifest = {"start": self.start, "requested_ts": self.ts, "scope": self.scope,
                    "fetched": self.done, "failed": self.failed, "unfetched_queue": self.queue}
        os.makedirs(self.out, exist_ok=True)
        with open(os.path.join(self.out, "_wayback_manifest.json"), "w") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=1)
        print(f"done: {len(self.done)} fetched, {len(self.failed)} failed -> {self.out}", flush=True)

    def write(self, local, data):
        p = os.path.join(self.out, local)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--ts", required=True, help="優先する Wayback タイムスタンプ (YYYYMMDDhhmmss)")
    ap.add_argument("--scope", help="ページをたどる範囲の URL プレフィックス（既定: start のディレクトリ）")
    ap.add_argument("--max-items", type=int, default=400)
    ap.add_argument("--delay", type=float, default=0.7)
    a = ap.parse_args()
    Mirror(a.out, a.start, a.ts, a.scope, a.max_items, a.delay).run()


if __name__ == "__main__":
    main()
