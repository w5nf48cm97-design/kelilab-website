#!/usr/bin/env python3
"""Build the KeliLab static catalogue. Python standard library only."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
POLICIES = json.loads((ROOT / "content/privacy-pages.json").read_text(encoding="utf-8"))
OUT = ROOT / "dist"
E = html.escape
APPS = CONFIG["apps"]
DOMAIN = "https://" + CONFIG["domain"]

ICONS = {
    "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "diagonal": '<path d="M6 18 18 6M6 6h12v12"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4M11 19h2"/>',
    "game": '<path d="M7.2 7h9.6a4 4 0 0 1 3.9 3.2l1.1 5.7a2.7 2.7 0 0 1-4.6 2.4L14 15h-4l-3.2 3.3a2.7 2.7 0 0 1-4.6-2.4l1.1-5.7A4 4 0 0 1 7.2 7Z"/><path d="M6 11h4m-2-2v4m8-2h.01m2 2h.01"/>',
    "shield": '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="m6 6 12 12M6 18 18 6"/>',
    "spark": '<path d="m12 1 2.4 7.6L22 6l-4.9 6 4.9 6-7.6-2.6L12 23l-2.4-7.6L2 18l4.9-6L2 6l7.6 2.6L12 1Z"/>',
}

def icon(name, size=20, css=""):
    return f'<svg class="{E(css)}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def prefix(path):
    return "../" * path.strip("/").count("/") if path.endswith("index.html") else ""

def base_for(path):
    return "../" * len(Path(path).parts[:-1])

def brand(base):
    return f'<a class="brand" href="{base}index.html" aria-label="KeliLab — Inicio"><img src="{base}assets/favicon.svg" alt="" width="38" height="38"><span class="brand-word">kelilab<span>.</span></span></a>'

def header(base):
    return f'''<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="container header-inner">{brand(base)}
<button class="menu-toggle" type="button" data-menu-button aria-expanded="false" aria-controls="main-navigation" aria-label="Abrir navegación">{icon("menu",22)}</button>
<nav class="main-nav" id="main-navigation" data-navigation aria-label="Navegación principal">
<a href="{base}index.html#apps">Apps y juegos</a><a href="{base}index.html#estudio">El estudio</a><a href="{base}privacidad/index.html">Privacidad</a>
<a class="nav-cta" href="{base}index.html#apps">Explorar apps {icon("diagonal",16)}</a></nav></div></header>'''

def footer(base):
    return f'''<footer class="site-footer container"><div class="footer-main"><div class="footer-brand-group">{brand(base)}<span class="footer-tagline">Un poco de orden.<br>Un poco de juego.</span></div>
<nav class="footer-links" aria-label="Navegación al pie"><a href="{base}index.html#apps">Nuestras apps</a><a href="{base}index.html#estudio">Sobre KeliLab</a><a href="{base}privacidad/index.html">Privacidad</a></nav></div>
<div class="footer-bottom"><span>© 2026 KeliLab. Todos los derechos reservados.</span><span>Hecho con ideas propias y mucho cuidado.</span></div></footer>'''

def page(path, title, description, body, noindex=False):
    base = "/" if path == "404.html" else base_for(path)
    canonical = DOMAIN + "/" + ("" if path == "index.html" else path.removesuffix("index.html"))
    robots = "noindex, nofollow" if noindex else "index, follow"
    result = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><title>{E(title)}</title><meta name="description" content="{E(description,quote=True)}">
<meta name="robots" content="{robots}"><link rel="canonical" href="{E(canonical)}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="KeliLab">
<meta property="og:title" content="{E(title,quote=True)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{E(canonical)}">
<meta name="theme-color" content="#f8f7f2"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/site.css">
<script defer src="{base}assets/site.js"></script></head><body>{header(base)}{body}{footer(base)}</body></html>'''
    destination = OUT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result, encoding="utf-8")

def play_icon():
    return '<svg class="play-icon" viewBox="0 0 20 22" fill="currentColor" aria-hidden="true"><path d="M1.2.7a1.5 1.5 0 0 0-.7 1.4v17.8c0 .5.2 1 .7 1.4L11.8 11 1.2.7Zm1.2-.4 12.5 7.2-2.2 2.4L2.4.3Zm13.9 8L14 11l2.3 2.7 2.5-1.5a1.4 1.4 0 0 0 0-2.4l-2.5-1.5ZM14.9 14.5 2.4 21.7l10.3-9.6 2.2 2.4Z"/></svg>'

def download(app):
    if app.get("playUrl"):
        return f'<a class="play-link" href="{E(app["playUrl"],quote=True)}" rel="noopener noreferrer">{play_icon()}<span>Google Play</span>{icon("diagonal",14)}</a>'
    return f'<span class="play-pending" aria-label="{E(app["name"])}: enlace de Google Play pendiente">{play_icon()}<span>Google Play<small>Enlace próximamente</small></span></span>'

def visual(app, base, detail=False):
    if app["id"] == "wereout":
        cls = "detail-visual wereout-visual" if detail else "app-visual wereout-visual"
        return f'''<div class="{cls}"><div class="visual-copy"><div class="mini-wordmark"><img src="{base}assets/wereout/icon.png" alt="" width="23" height="23">WE'RE OUT!</div><h3>Todo en casa.<br>En su sitio.</h3><span class="mini-tag">Tu hogar, organizado</span></div><div class="visual-phone"><img src="{base}assets/wereout/inventario.png" width="402" height="844" alt="Pantalla real de inventario de We're Out!" loading="lazy"></div></div>'''
    cls = "detail-visual geoblock-visual" if detail else "app-visual geoblock-visual"
    return f'<div class="{cls}"><img src="{base}assets/geoblock/geoblock.png" alt="Imagen oficial de GeoBlock: bloques esmeralda y dorados con frutas de colores" width="662" height="643" loading="lazy"></div>'

def card(app, base=""):
    label = "App" if app["type"] == "apps" else "Juego"
    css_icon = " geoblock-icon" if app["id"] == "geoblock" else ""
    search = app["name"] + " " + app["category"] + " " + app["description"]
    card_visual = visual(app,base).replace('<div class="app-visual',f'<a href="{base}apps/{app["id"]}/index.html" aria-label="Conocer {E(app["name"])}" class="app-visual',1)
    card_visual = card_visual.rsplit("</div>",1)[0]+f'<span class="visual-corner">{icon("diagonal",16)}</span></a>'
    return f'''<article class="app-card" data-app-card data-category="{app["type"]}" data-search="{E(search,quote=True)}">
{card_visual}<div class="app-card-body"><div class="app-title-row"><div class="app-identity"><img class="app-icon{css_icon}" src="{base}{app["icon"]}" alt="" width="47" height="47" loading="lazy"><div><h3><a href="{base}apps/{app["id"]}/index.html">{E(app["name"])}</a></h3><p class="app-category">{E(app["category"])}</p></div></div><span class="type-badge">{label}</span></div>
<p class="app-description">{E(app["description"])}</p><div class="app-card-actions"><a class="card-detail" href="{base}apps/{app["id"]}/index.html">Conocer la app {icon("arrow",15)}</a>{download(app)}</div></div></article>'''

def privacy_strip(base):
    return f'''<aside class="privacy-strip"><span class="privacy-symbol">{icon("shield",23)}</span><div><h3>Tu privacidad tiene su sitio.</h3><p>La información de cada app, siempre a mano.</p></div><a class="text-link" href="{base}privacidad/index.html">Centro de privacidad {icon("arrow",17)}</a></aside>'''

def home():
    cards = "".join(card(app) for app in APPS)
    body=f'''<main id="contenido" class="container"><section class="hero" aria-labelledby="home-heading"><div class="hero-copy">
<p class="eyebrow"><span class="dot"></span>EL PEQUEÑO UNIVERSO DE KELILAB</p><h1 id="home-heading">Pequeñas apps.<br><em>Grandes días.</em></h1>
<p>Herramientas para poner orden.<br>Juegos para hacer una pausa.<br>Ideas que encuentran su sitio en tu móvil.</p>
<div class="hero-actions"><a class="button button-primary" href="#apps">Descubre nuestras apps {icon("arrow",19)}</a><a class="text-link" href="#estudio">Así es KeliLab {icon("diagonal",15)}</a></div>
<div class="hero-note"><span></span>Dos proyectos. Muchas ideas por venir.</div></div>
<div class="hero-art" aria-label="We're Out! y GeoBlock, las dos apps de KeliLab">
<a class="hero-wereout" href="apps/wereout/index.html" aria-label="Descubrir We're Out!"><div class="hero-wereout-label">Tu casa al día.</div><div class="hero-phone"><img src="assets/wereout/inventario.png" alt="Inventario de We're Out!" width="402" height="844" fetchpriority="high"></div></a>
<a class="hero-geoblock" href="apps/geoblock/index.html" aria-label="Descubrir GeoBlock"><img src="assets/geoblock/geoblock.png" alt="GeoBlock" width="662" height="643" fetchpriority="high"></a>
<span class="art-tag art-tag-top">{icon("game",16)} Un rato para ti</span><span class="art-tag art-tag-bottom">{icon("phone",15)} Un poco más fácil. Un poco más divertido.</span>{icon("spark",46,"spark")}</div></section>
<section class="collection" id="apps" aria-labelledby="apps-heading"><div class="section-heading"><div><p class="section-label">HECHAS EN KELILAB</p><h2 id="apps-heading">Encuentra tu próxima app.</h2></div><span class="project-count" data-result-count aria-live="polite">2 proyectos</span></div>
<div class="catalog-tools"><div class="filters" role="group" aria-label="Filtrar proyectos"><button class="filter is-active" type="button" data-filter="all" aria-pressed="true">{icon("grid",14)} Todas</button><button class="filter" type="button" data-filter="apps" aria-pressed="false">{icon("phone",14)} Aplicaciones</button><button class="filter" type="button" data-filter="juegos" aria-pressed="false">{icon("game",16)} Juegos</button></div>
<label class="search-box"><span class="sr-only">Buscar apps y juegos</span>{icon("search",18)}<input type="search" placeholder="Encuentra algo para ti…" data-app-search autocomplete="off" maxlength="120"></label></div>
<div class="app-grid">{cards}<div class="empty-result" data-empty-result hidden><h3>Aún no tenemos esa app.</h3><p>Prueba con otro nombre o vuelve a ver todos los proyectos.</p><button type="button" class="button button-light" data-reset-search>Ver todas las apps {icon("arrow",17)}</button></div></div></section>
<section class="studio-section" id="estudio" aria-labelledby="studio-heading"><div class="studio-story"><span class="section-label">CONOCE EL ESTUDIO</span><h2 id="studio-heading">Un laboratorio.<br>Muchas buenas ideas.</h2><p>KeliLab es el lugar donde reunimos nuestras apps y juegos. Proyectos distintos, una misma idea: que merezca la pena tenerlos en el móvil.</p><img class="studio-symbol" src="assets/favicon.svg" alt="" width="218" height="218" loading="lazy"></div>
<div class="studio-note"><div class="note-top"><span class="section-label">PARA LO COTIDIANO.<br>Y PARA DESCONECTAR.</span>{icon("spark",40)}</div><div><h3>Hay un momento<br>para cada app.</h3><p>Organizar la compra. Encontrar un hueco para jugar. Creamos para esos pequeños momentos de tu día.</p></div></div></section>{privacy_strip("")}</main>'''
    page("index.html","KeliLab — Pequeñas apps. Grandes días.",CONFIG["description"],body)

def breadcrumb(base, current, middle=None):
    mid = f'<a href="{base}privacidad/index.html">Privacidad</a><span aria-hidden="true">/</span>' if middle else ""
    return f'<nav class="breadcrumb" aria-label="Ruta"><a href="{base}index.html">Inicio</a><span aria-hidden="true">/</span>{mid}<span aria-current="page">{E(current)}</span></nav>'

def app_detail(app):
    base="../../"
    css_icon=" geoblock-icon" if app["id"]=="geoblock" else ""
    features=""
    gallery=""
    if app["features"]:
        features='<section class="feature-grid" aria-label="Funciones principales">'+''.join(f'<article class="feature"><span class="feature-number">0{i+1}</span><h3>{E(f["title"])}</h3><p>{E(f["text"])}</p></article>' for i,f in enumerate(app["features"]))+'</section>'
    if app["id"]=="wereout":
        screenshots=[("compra","Lista de compra"),("inventario","Inventario"),("informes","Informes")]
        figures=''.join(f'<figure class="screenshot-item"><button type="button" data-enlarge aria-label="Ampliar captura: {E(label)}"><img src="{base}assets/wereout/{name}.png" alt="{E(label)} de We&#x27;re Out!" loading="lazy" width="402" height="844"></button><figcaption>{E(label)}</figcaption></figure>' for name,label in screenshots)
        gallery=f'''<section aria-labelledby="screenshots-heading"><div class="screenshots-heading"><h2 id="screenshots-heading">Así se ve por dentro.</h2><p>Capturas reales de desarrollo.<br>El diseño puede cambiar antes del lanzamiento.</p></div><div class="screenshot-grid">{figures}</div></section>
<dialog class="image-dialog" data-image-dialog aria-label="Captura ampliada"><div class="dialog-top"><span data-dialog-caption></span><button type="button" class="dialog-close" data-close-dialog aria-label="Cerrar captura">{icon("close",18)}</button></div><img src="{base}assets/wereout/inventario.png" alt="Captura ampliada de We're Out!"></dialog>'''
    else:
        gallery='<section class="game-note"><h2>Un juego con<br>personalidad propia.</h2><p>GeoBlock forma parte de la colección de juegos de KeliLab. En esta página reuniremos sus novedades, capturas y acceso a la ficha oficial de Google Play.</p></section>'
    body=f'''<main id="contenido" class="container">{breadcrumb(base,app["name"])}<section class="detail-hero"><div class="detail-copy"><div class="detail-identity"><img class="app-icon{css_icon}" src="{base}{app["icon"]}" alt="" width="66" height="66"><span class="eyebrow">{E(app["category"])}</span></div><h1>{E(app["name"])}</h1><h2>{E(app["short"])}</h2><p>{E(app["description"])}</p><div class="detail-actions">{download(app)}<a class="text-link" href="{base}privacidad/{app["id"]}/index.html">Privacidad {icon("arrow",16)}</a></div><p class="detail-note">El acceso directo a la descarga aparecerá aquí cuando esté disponible el enlace oficial.</p></div>{visual(app,base,True)}</section>{features}{gallery}<div class="detail-bottom">{privacy_strip(base)}</div></main>'''
    page(f'apps/{app["id"]}/index.html',f'{app["name"]} — KeliLab',app["description"],body)

def privacy_hub():
    base="../"
    rows=""
    for app in APPS:
        rows+=f'''<article class="privacy-card"><img src="{base}{app["icon"]}" alt="" width="52" height="52"><span class="draft-pill">En preparación</span><h2>{E(app["name"])}</h2><p>Información sobre datos, permisos y servicios de esta aplicación.</p><a class="text-link" href="{app["id"]}/index.html">Ver documento {icon("arrow",17)}</a></article>'''
    rows+=f'<article class="privacy-card"><img src="{base}assets/favicon.svg" alt="" width="52" height="52"><span class="draft-pill">En preparación</span><h2>Este sitio web</h2><p>Información sobre la navegación en kelilab.es y sus enlaces externos.</p><a class="text-link" href="web/index.html">Ver documento {icon("arrow",17)}</a></article>'
    body=f'''<main id="contenido" class="container">{breadcrumb(base,"Centro de privacidad")}<section class="page-intro"><p class="eyebrow"><span class="dot"></span>LA INFORMACIÓN, A MANO</p><h1>Un espacio para<br>tu privacidad.</h1><p>Cada aplicación tiene su propio documento. Aquí reunimos la información sobre sus datos, permisos y servicios.</p></section><div class="review-notice"><strong>Documentos en preparación</strong><p>Los documentos están en preparación. Estas páginas todavía no constituyen políticas de privacidad definitivas para Google Play o AdMob.</p></div><div class="privacy-grid">{rows}</div></main>'''
    page("privacidad/index.html","Centro de privacidad — KeliLab","Documentos de privacidad de We're Out!, GeoBlock y kelilab.es.",body,True)

def privacy_page(key, slug):
    base="../../"
    policy=POLICIES[key]
    body=f'''<main id="contenido" class="container">{breadcrumb(base,policy["title"],True)}<section class="page-intro"><span class="draft-pill">En preparación</span><h1>{E(policy["title"])}</h1><p>La información de privacidad de {E(policy["name"])} se publicará en esta página cuando esté completada.</p></section><div class="review-notice"><strong>Esta política todavía no está publicada.</strong><p>Estamos preparando la información sobre el responsable, el contacto y el tratamiento de datos. Esta página no debe presentarse como política definitiva en Google Play ni AdMob.</p></div><a class="button button-primary" href="{base}privacidad/index.html">Volver al centro de privacidad {icon("arrow",17)}</a></main>'''
    page(f"privacidad/{slug}/index.html",policy["title"]+" — KeliLab","Política de privacidad en preparación.",body,True)

def validate_config():
    for app in APPS:
        url=app.get("playUrl")
        if url:
            parsed=urlparse(url)
            if parsed.scheme!="https" or parsed.netloc!="play.google.com" or parsed.path!="/store/apps/details" or not re.search(r"(?:^|&)id=[A-Za-z0-9_.]+(?:&|$)",parsed.query):
                raise ValueError("playUrl must be an official Google Play app detail link")
    line=CONFIG.get("adMobPublisherLine")
    if line and not re.fullmatch(r"google\.com,\s*pub-\d{16},\s*DIRECT,\s*f08c47fec0942fa0",line.strip()):
        raise ValueError("Use the exact AdMob app-ads.txt publisher line, never an app/ad-unit ID")

def build():
    validate_config()
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/"assets",OUT/"assets",dirs_exist_ok=True)
    home()
    for app in APPS:
        app_detail(app)
    privacy_hub()
    for key,slug in [("wereout","wereout"),("geoblock","geoblock"),("site","web")]:
        privacy_page(key,slug)
    error=f'<main id="contenido" class="container"><div class="error-page"><span class="error-code">404</span><h1>Esta pieza no encaja aquí.</h1><p>La página que buscas no está disponible. Nuestras apps siguen en su sitio.</p><a class="button button-primary" href="{DOMAIN}/">Volver a KeliLab {icon("arrow",18)}</a></div></main>'
    page("404.html","Página no encontrada — KeliLab","Vuelve al catálogo de KeliLab.",error,True)
    (OUT/".nojekyll").write_text("",encoding="utf-8")
    (OUT/"CNAME").write_text(CONFIG["domain"]+"\n",encoding="utf-8")
    (OUT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+DOMAIN+"/sitemap.xml\n",encoding="utf-8")
    pages=["","apps/wereout/","apps/geoblock/"]
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join("<url><loc>"+DOMAIN+"/"+p+"</loc></url>" for p in pages)+"</urlset>\n"
    (OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    if CONFIG.get("adMobPublisherLine"):
        (OUT/"app-ads.txt").write_text(CONFIG["adMobPublisherLine"].strip()+"\n",encoding="utf-8")
    elif (OUT/"app-ads.txt").exists():
        (OUT/"app-ads.txt").unlink()
    print(json.dumps({"pages":len(list(OUT.rglob("*.html"))),"output":str(OUT),"privacyStatus":"draft","playLinks":sum(bool(a["playUrl"]) for a in APPS),"appAdsTxt":bool(CONFIG["adMobPublisherLine"])},ensure_ascii=False))

if __name__=="__main__":
    build()
