#!/usr/bin/env python3
"""Генерирует папки с чистыми адресами (/films/, /music-videos/, /commercials/, /about/)
из единственного исходника index.html и обновляет sitemap.xml.
Запускать после КАЖДОЙ правки index.html:   python3 tools/build_pages.py
(GitHub Pages отдаёт только готовые файлы, поэтому у каждого раздела свой index.html.)"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/'index.html').read_text(encoding='utf8')
SITE = 'https://ilyashpota.com'
PAGES = {
  'films':        'Films — Ilya Shpota',
  'music-videos': 'Music videos — Ilya Shpota',
  'commercials':  'Commercials — Ilya Shpota',
  'about':        'About — Ilya Shpota',
}
for slug, title in PAGES.items():
    url = f'{SITE}/{slug}/'
    h = src
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', rf'\g<1>{url}', h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', rf'\g<1>{url}', h, count=1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\g<1>{title}', h, count=1)
    h = re.sub(r'(<meta name="twitter:title" content=")[^"]*', rf'\g<1>{title}', h, count=1)
    d = root/slug; d.mkdir(exist_ok=True)
    (d/'index.html').write_text(h, encoding='utf8')
urls = [f'{SITE}/'] + [f'{SITE}/{s}/' for s in PAGES]
(root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n', encoding='utf8')
print('built:', ', '.join(PAGES), '+ sitemap.xml')
