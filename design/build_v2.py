from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
DATA = V2 / "data"
ASSETS = V2 / "assets"
BRANCHES = ("prokshino", "ispanskie")
CATEGORY_SLUG = {
    "consultations": "consultations",
    "diagnostics": "diagnostics",
    "anesthesia": "anesthesia",
    "hygiene": "hygiene",
    "treatment": "treatment",
    "endodontics": "endodontics",
    "surgery": "surgery",
    "implantation": "implantation",
    "prosthetics": "prosthetics",
    "orthodontics": "orthodontics",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


SERVICES = load_json(DATA / "services_master.json")
CATEGORIES = load_json(DATA / "categories_summary.json")
CLINIC_CONTENT = load_json(DATA / "clinic-content.json")
DOCTORS = load_json(DATA / "doctors.json")
FEATURED = CLINIC_CONTENT["featuredServiceIds"]
SHARED = CLINIC_CONTENT["shared"]
SERVICE_BY_ID = {item["id"]: item for item in SERVICES}
BY_CATEGORY = {
    code: [item for item in SERVICES if item["category"] == code]
    for code in CATEGORIES
}


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def rel_path(page: Path, target: Path) -> str:
    return os.path.relpath(target, page.parent).replace(os.sep, "/")


def repo_asset(page: Path, source_path: str) -> str:
    return rel_path(page, ROOT / source_path)


def service_route(branch: str, category: str) -> str:
    return f"v2/{branch}/services/{CATEGORY_SLUG[category]}.html"


def relative_service_route(page: Path, branch: str, category: str) -> str:
    return rel_path(page, ROOT / service_route(branch, category))


def branch_route(page: Path, branch: str, route: str) -> str:
    return rel_path(page, ROOT / f"v2/{branch}/{route}")


def category_records(category: str) -> list[dict]:
    return BY_CATEGORY[category]


def price_for(service: dict, branch: str) -> str:
    return service["pricing"][branch]["formatted"]


def safe_js_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def validate_source_data() -> None:
    if len(SERVICES) != 254 or len(SERVICE_BY_ID) != 254:
        raise ValueError("canonical service file must contain 254 unique IDs")
    for category, info in CATEGORIES.items():
        rows = BY_CATEGORY.get(category, [])
        if len(rows) != info["count"]:
            raise ValueError(f"category count mismatch for {category}: {len(rows)} != {info['count']}")
        for service in rows:
            for branch in BRANCHES:
                pricing = service.get("pricing", {}).get(branch, {})
                if not service.get("id") or not service.get("name") or not pricing.get("formatted"):
                    raise ValueError(f"incomplete service record: {service.get('id')}")
        picks = FEATURED.get(category, [])
        if not picks:
            raise ValueError(f"no selector examples configured for {category}")
        for service_id in picks:
            item = SERVICE_BY_ID.get(service_id)
            if item is None or item["category"] != category:
                raise ValueError(f"invalid selector service ID {service_id} for {category}")
    if sum(item["count"] for item in CATEGORIES.values()) != len(SERVICES):
        raise ValueError("category counts do not add up to the service total")
    for doctor in DOCTORS:
        if not (ROOT / doctor["portrait"]).is_file():
            raise FileNotFoundError(doctor["portrait"])


def render_nav(page: Path, branch: str, active: str) -> str:
    content = CLINIC_CONTENT["branches"][branch]
    links = [
        ("home", "Главная", "index.html"),
        ("directions", "Направления", "directions/index.html"),
        ("doctors", "Врачи", "doctors/index.html"),
        ("prices", "Прайс · 254", "prices/index.html"),
        ("contacts", "Контакты", "contacts/index.html"),
    ]
    items = []
    for key, label, route in links:
        href = branch_route(page, branch, route)
        current = ' aria-current="page"' if key == active else ""
        items.append(f'<a href="{h(href)}"{current}>{h(label)}</a>')
    other = "ispanskie" if branch == "prokshino" else "prokshino"
    other_content = CLINIC_CONTENT["branches"][other]
    logo = repo_asset(page, "design/assets/prokshino/logo.png")
    booking_label = "Запись" if branch == "ispanskie" else "Записаться"
    return f'''<div class="microbar"><div class="shell microbar-inner"><span>Москва · Коммунарка · {h(content['name'])}</span><a href="{h(branch_route(page, other, 'index.html'))}" aria-label="Перейти на сайт филиала {h(other_content['name'])}">Другой филиал <span aria-hidden="true">↗</span></a></div></div>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="{h(branch_route(page, branch, 'index.html'))}" aria-label="ДантистЪ — главная, {h(content['name'])}"><img src="{h(logo)}" alt="ДантистЪ" width="213" height="44"><span class="brand-location">{h(content['name'])}</span></a><button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-navigation"><span class="menu-lines" aria-hidden="true"></span><span class="sr-only">Открыть меню</span></button><nav class="primary-nav" id="site-navigation" data-primary-nav aria-label="Основная навигация">{''.join(items)}<button class="nav-book" type="button" data-open-booking>{booking_label}</button></nav></div></header>'''


def booking_dialog(page: Path, branch: str) -> str:
    dentalpro = h(SHARED["dentalpro"])
    whatsapp = h(SHARED["whatsapp"])
    telegram = h(SHARED["telegram"])
    tel = h(SHARED["tel"])
    if branch == "ispanskie":
        online_kicker = "ОНЛАЙН · ФИЛИАЛ ПРОКШИНО"
        online_title = "DentalPRO · Прокшино"
        online_description = "Официальная ссылка на сайте Испанских кварталов открывает расписание филиала Прокшино. Для записи именно сюда используйте телефон регистратуры."
        online_button = "Открыть DentalPRO · Прокшино ↗"
        dialog_intro = "Важно: официальный переход на онлайн-запись с сайта Испанских кварталов ведёт в филиал Прокшино. Для записи в Испанские кварталы позвоните в регистратуру."
    else:
        online_kicker = "ОНЛАЙН · DentalPRO"
        online_title = "Выбрать врача и время"
        online_description = "Свободные интервалы и варианты приёма — в официальной системе онлайн-записи."
        online_button = "Продолжить в DentalPRO ↗"
        dialog_intro = "Выберите реальный способ связи с клиникой."
    return f'''<dialog class="booking-dialog" data-booking-dialog aria-labelledby="booking-title">
  <div class="booking-dialog-inner">
    <header class="dialog-topline"><span class="eyebrow">ДАНТИСТЪ · ВЫБОР СПОСОБА ЗАПИСИ</span><button type="button" class="dialog-close" data-close-booking aria-label="Закрыть окно">×</button></header>
    <div class="booking-service" data-booking-service hidden><span>Вы выбрали интересующее направление</span><strong data-booking-service-name></strong><span data-booking-service-price></span></div>
    <p class="booking-explainer" data-booking-service-note hidden>{h(SHARED['appointmentNote'])}</p>
    <section data-booking-step="choices">
      <h2 id="booking-title">Как вам удобнее записаться?</h2><p class="dialog-intro">{h(dialog_intro)}</p>
      <div class="booking-choice-grid">
        <article class="booking-choice booking-choice-call"><div class="choice-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.4 1.6a14 14 0 0 0 4.8 4.8L15 13l5 2v4c0 1.1-.9 2-2 2C10.5 21 3 13.5 3 6c0-1.1.9-2 2-2Z"/></svg></div><span class="choice-kicker">ПО ТЕЛЕФОНУ</span><h3>Позвонить</h3><a class="choice-number" href="{tel}">{h(SHARED['phone'])}</a><p>{h(SHARED['hours'])}</p><button type="button" class="button button-light" data-book-call>Посмотреть варианты звонка</button></article>
        <article class="booking-choice booking-choice-online"><div class="choice-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg></div><span class="choice-kicker">{h(online_kicker)}</span><h3>{h(online_title)}</h3><p>{h(online_description)}</p><a class="button button-primary" href="{dentalpro}" target="_blank" rel="noopener noreferrer">{h(online_button)}</a></article>
      </div>
      <p class="booking-data-note">Выбранное направление отображается в этом окне только для вашего ориентира и не передаётся в DentalPRO.</p>
      <div class="booking-messengers"><span>Ещё можно написать:</span><a href="{whatsapp}" target="_blank" rel="noopener noreferrer">WhatsApp</a><a href="{telegram}" target="_blank" rel="noopener noreferrer">Telegram · канал/чат</a></div>
    </section>
    <section data-booking-step="call" hidden aria-labelledby="booking-call-title">
      <button type="button" class="text-button call-back" data-booking-back>← К способам записи</button><p class="choice-kicker">ПРЯМОЙ НОМЕР РЕГИСТРАТУРЫ</p><h2 id="booking-call-title" tabindex="-1">Позвонить в клинику</h2><p>Режим работы: {h(SHARED['hours'])}. На компьютере звонок откроет телефонное приложение, если оно подключено.</p><div class="call-confirm-number"><a href="{tel}">{h(SHARED['phone'])}</a><button type="button" class="button button-light" data-copy-phone>Скопировать номер</button></div><p class="copy-status" data-copy-status role="status" aria-live="polite"></p></section>
  </div>
</dialog>'''

def shell(page: Path, *, title: str, description: str, body: str, branch: str | None, active: str, page_type: str, category: str = "") -> str:
    repo_root = rel_path(page, ROOT).rstrip("/") + "/"
    css = rel_path(page, ASSETS / "v2.css")
    data_js = rel_path(page, ASSETS / "v2-data.js")
    app_js = rel_path(page, ASSETS / "v2.js")
    theme = "#183d42" if branch == "prokshino" else "#6d3f36"
    nav = render_nav(page, branch, active) if branch else ""
    footer = render_footer(page, branch) if branch else ""
    dialog = booking_dialog(page, branch) if branch else ""
    body_class = f"v2-page page-{page_type}" + (f" clinic-{branch}" if branch else "")
    category_attr = f' data-category="{h(category)}"' if category else ""
    return f'''<!doctype html>
<html lang="ru" data-repo-root="{h(repo_root)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="{theme}">
  <title>{h(title)} · ДантистЪ</title>
  <meta name="description" content="{h(description)}">
  <link rel="stylesheet" href="{h(css)}">
  <script defer src="{h(data_js)}"></script>
  <script defer src="{h(app_js)}"></script>
</head>
<body class="{h(body_class)}" data-page="{h(page_type)}" data-clinic="{h(branch or '')}"{category_attr}>
<a class="skip-link" href="#main-content">Перейти к содержимому</a>
{nav}
<main id="main-content">{body}</main>
{footer}
{dialog}
</body>
</html>'''


def render_footer(page: Path, branch: str | None) -> str:
    if not branch:
        return '<footer class="v2-footer chooser-footer"><div class="shell"><span>ДантистЪ · V2 preview</span><span>Самостоятельная демонстрационная сборка</span></div></footer>'
    content = CLINIC_CONTENT["branches"][branch]
    other = "ispanskie" if branch == "prokshino" else "prokshino"
    logo = repo_asset(page, "design/assets/prokshino/logo.png")
    tel = SHARED["tel"]
    rows = [
        ("Главная", "index.html"),
        ("Направления", "directions/index.html"),
        ("Врачи", "doctors/index.html"),
        ("Прайс", "prices/index.html"),
        ("Контакты", "contacts/index.html"),
    ]
    links = "".join(f'<a href="{h(branch_route(page, branch, path))}">{h(label)}</a>' for label, path in rows)
    other_link = branch_route(page, other, "index.html")
    return f'''<footer class="v2-footer"><div class="shell footer-grid"><div class="footer-brand"><a href="{h(branch_route(page, branch, 'index.html'))}"><img src="{h(logo)}" alt="ДантистЪ" width="170" height="36"></a><p>{h(content['fullName'])}</p><a href="{h(tel)}">{h(SHARED['phone'])}</a></div><nav aria-label="Навигация в подвале">{links}</nav><div class="footer-contact"><span>{h(content['address'])}</span><span>{h(SHARED['hours'])}</span><a class="text-button" href="{h(other_link)}">Выбрать другой филиал ↗</a></div></div><div class="shell footer-bottom"><span>Preview V2 · сведения и цены приведены для ознакомления.</span><span>План лечения и его стоимость обсудите с врачом.</span></div></footer>'''


def selector_markup(page: Path, branch: str, mode: str = "home") -> str:
    default_category = "implantation"
    default_service = SERVICE_BY_ID[FEATURED[default_category][0]]
    image = repo_asset(page, CLINIC_CONTENT["branches"][branch]["selectorImages"][default_category])
    detail_url = relative_service_route(page, branch, default_category) + "?service=" + quote(default_service["id"]) + "#selected-procedure"
    heading_id = "selector-heading-" + mode
    variant_label_id = "selector-variants-label-" + mode
    service_base = rel_path(page, ROOT / f"v2/{branch}/services")
    return f'''<div class="service-selector" data-service-selector data-selector-mode="{h(mode)}" data-service-base="{h(service_base)}">
  <div class="selector-column">
    <div class="selector-column-head"><span class="section-index">01 / 10</span><h3>Выберите направление</h3></div>
    <div class="selector-categories" role="tablist" aria-label="Направления стоматологии" data-selector-categories></div>
    <div class="selector-variants-box"><div class="selector-column-head variant-head"><span class="section-index">ВАРИАНТЫ</span><h4 id="{h(variant_label_id)}">Выберите позицию прайса</h4></div><div class="selector-variants" role="tablist" aria-labelledby="{h(variant_label_id)}" data-selector-variants></div></div>
  </div>
  <article class="selected-procedure" id="selected-procedure" data-selector-card aria-labelledby="{h(heading_id)}">
    <div class="selected-procedure-image"><img data-selector-image src="{h(image)}" alt="Изображение стоматологического приёма в клинике" width="720" height="520"><span class="image-mark">01 <i>·</i> ДантистЪ</span></div>
    <div class="selected-procedure-copy"><span class="eyebrow" data-selector-category>ДЕНТАЛЬНАЯ ИМПЛАНТАЦИЯ</span><h3 id="{h(heading_id)}" data-selector-name>{h(default_service['name'])}</h3><p data-selector-description>{h(CLINIC_CONTENT['categoryDescriptions'][default_category])}</p><div class="selected-price"><span>Цена позиции в каталоге</span><strong data-selector-price>{h(price_for(default_service, branch))}</strong></div><p class="selected-price-note">Стоимость отдельной позиции не равна стоимости полного плана лечения.</p><div class="selected-actions"><button class="button button-primary" type="button" data-open-booking data-service-id="{h(default_service['id'])}">Обсудить запись</button><a class="button button-secondary" data-selector-details href="{h(detail_url)}">Подробнее</a></div><a class="all-prices-link" href="{h(branch_route(page, branch, 'prices/index.html'))}">Открыть все 254 позиции прайса ↗</a></div>
  </article>
</div>'''


def render_chooser() -> None:
    page = V2 / "index.html"
    cards = []
    for key in BRANCHES:
        content = CLINIC_CONTENT["branches"][key]
        target = ROOT / f"v2/{key}/index.html"
        image = repo_asset(page, content["image"])
        cards.append(f'''<article class="branch-card branch-card-{key}"><a class="branch-card-image" href="{h(rel_path(page,target))}"><img src="{h(image)}" alt="{h(content['imageAlt'])}" width="900" height="640"><span class="branch-card-index">0{BRANCHES.index(key)+1} / ДАНТИСТЪ</span></a><div class="branch-card-copy"><p class="eyebrow">{h(content['eyebrow'])}</p><h2>{h(content['fullName'])}</h2><p>{h(content['description'])}</p><div class="card-actions"><a class="button button-primary" href="{h(rel_path(page,target))}">Открыть сайт филиала ↗</a><a class="text-button" href="{h(branch_route(page,key,'directions/index.html'))}">Выбрать направление</a></div></div></article>''')
    body = f'''<section class="chooser-hero shell"><p class="eyebrow">ДАНТИСТЪ · НОВАЯ АРХИТЕКТУРА САЙТА</p><h1>Выберите клинику.<br><em>Потом — направление.</em></h1><p>Два филиала сети, связанные понятной навигацией. Сравните цены конкретных процедур, изучите врачей и выберите удобный способ записи.</p><div class="chooser-facts"><span><b>254</b> позиции в прайсе каждого филиала</span><span>Выбор услуги не является рекомендацией лечения</span></div></section><section class="branch-cards shell" aria-label="Сайты клиник">{''.join(cards)}</section><section class="chooser-note shell"><span class="note-number">V2</span><p>Выбранное направление остаётся в демонстрационном интерфейсе и не передаётся в систему записи.</p><p><a href="../index.html">На общую страницу проекта</a></p></section>'''
    write(page, shell(page, title="Выберите филиал", description="Два сайта стоматологии ДантистЪ — Прокшино и Испанские кварталы", body=body, branch=None, active="", page_type="chooser"))


def render_home(branch: str) -> None:
    page = V2 / branch / "index.html"
    info = CLINIC_CONTENT["branches"][branch]
    hero_image = repo_asset(page, info["image"])
    gallery = "".join(f'<figure class="gallery-photo"><img src="{h(repo_asset(page,item["src"]))}" alt="{h(item["alt"])}" loading="lazy"><figcaption>{h(item["alt"])}</figcaption></figure>' for item in info["gallery"])
    preview_doctors = DOCTORS[:3]
    doctor_cards = "".join(f'''<a class="doctor-mini" href="{h(branch_route(page,branch,'doctors/'+doc['slug']+'.html'))}"><img src="{h(repo_asset(page,doc['portrait']))}" alt="Портрет врача {h(doc['name'])}" loading="lazy"><span><strong>{h(doc['shortName'])}</strong><small>{h(doc['role'])}</small><small>Стаж {h(doc['experience'])}</small></span><b aria-hidden="true">↗</b></a>''' for doc in preview_doctors)
    facts = '<div class="hero-facts"><div><strong>10</strong><span>направлений</span></div><div><strong>254</strong><span>позиции прайса</span></div><div><strong>09—21</strong><span>ежедневно</span></div></div>'

    if branch == "prokshino":
        hero = f'''<section class="home-hero home-hero-clinical"><div class="shell home-hero-inner"><div class="home-hero-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>ПРОКШИНО · СТОМАТОЛОГИЧЕСКАЯ КЛИНИКА</p><h1>Сначала —<br><em>ясный план.</em></h1><p class="hero-lead">Изучите направления и цены клиники, познакомьтесь с врачами и выберите удобный способ связи.</p><div class="hero-actions"><a class="button button-secondary" href="#service-selection">Услуги и цены <span aria-hidden="true">↓</span></a><button class="button button-primary" type="button" data-open-booking>Онлайн-запись <span aria-hidden="true">↗</span></button></div>{facts}</div><figure class="home-hero-image"><img src="{h(hero_image)}" alt="{h(info['imageAlt'])}" width="1000" height="667"><figcaption><span>КОНСУЛЬТАЦИЯ</span><span>МОСКВА · ПРОКШИНО</span></figcaption><aside class="hero-photo-note"><span class="hero-photo-number">01</span><span><b>Первый шаг</b><small>Разговор и снимок</small></span></aside></figure></div></section>'''
    else:
        inset = repo_asset(page, "design/assets/ispanskie/gallery-8.jpg")
        hero = f'''<section class="home-hero home-hero-family"><div class="shell home-hero-inner"><div class="home-hero-copy"><p class="eyebrow"><span class="eyebrow-dot"></span>ИСПАНСКИЕ КВАРТАЛЫ · МОСКВА</p><h1>Стоматология<br><em>рядом с домом.</em></h1><p class="hero-lead">Семейная стоматология в Испанских кварталах. Изучите направления и цены, познакомьтесь с врачами филиала и выберите удобный способ связи.</p><div class="hero-actions"><a class="button button-secondary" href="#service-selection">Услуги и цены <span aria-hidden="true">↓</span></a><button class="button button-primary" type="button" data-open-booking>Записаться <span aria-hidden="true">↗</span></button></div>{facts}</div><div class="family-photo-stack"><figure class="family-photo-main"><img src="{h(hero_image)}" alt="{h(info['imageAlt'])}" width="824" height="549"><figcaption>ИСПАНСКИЕ КВАРТАЛЫ · ДАНТИСТЪ</figcaption></figure><figure class="family-photo-inset"><img src="{h(inset)}" alt="Врач стоматолог в кабинете клиники" width="575" height="862" loading="lazy"><figcaption>ВРАЧИ ФИЛИАЛА</figcaption></figure></div></div></section>'''

    body = f'''{hero}
<section class="section-shell selector-section" id="service-selection"><div class="shell section-heading-row"><div><p class="eyebrow">УСЛУГИ КЛИНИКИ</p><h2>С чего <em>начнём?</em></h2></div><p>Выберите интересующее направление и конкретную позицию прайса. Это не подбор лечения и не медицинская рекомендация.</p></div><div class="shell">{selector_markup(page,branch,'home')}</div><div class="shell selector-footnote"><span>Стоимость — за позицию из прайса</span><a href="{h(branch_route(page,branch,'directions/index.html'))}">Открыть все направления ↗</a></div></section>
<section class="section-shell team-strip"><div class="shell section-heading-row"><div><p class="eyebrow">КОМАНДА КЛИНИКИ</p><h2>Врачи <em>филиала</em></h2></div><a class="text-button" href="{h(branch_route(page,branch,'doctors/index.html'))}">Все специалисты ↗</a></div><div class="shell doctor-mini-list">{doctor_cards}</div></section>
<section class="section-shell clinic-strip"><div class="shell section-heading-row"><div><p class="eyebrow">ПРОСТРАНСТВО КЛИНИКИ</p><h2>Увидеть <em>изнутри</em></h2></div><p>Реальные фотографии пространства и приёма из официальной галереи филиала.</p></div><div class="shell gallery-grid gallery-count-{len(info['gallery'])}">{gallery}</div></section>
<section class="contact-band shell home-contact-{branch}"><div><p class="eyebrow">{h(info['name'].upper())} · МОСКВА</p><h2>{'Обсудить.<br><em>Уточнить. Выбрать.</em>' if branch == 'prokshino' else 'Рядом,<br><em>когда нужно уточнить.</em>'}</h2><p>{h(info['address'])}<br>{h(SHARED['hours'])}</p></div><div class="contact-band-actions"><a href="{h(SHARED['tel'])}" class="contact-phone">{h(SHARED['phone'])}</a><button type="button" class="button button-primary" data-open-booking>Как вам удобнее записаться?</button><a href="{h(branch_route(page,branch,'contacts/index.html'))}" class="text-button">Контакты и карта ↗</a></div></section>'''
    write(page, shell(page, title=info["fullName"], description=info["description"], body=body, branch=branch, active="home", page_type="home"))

def render_directions(branch: str) -> None:
    page = V2 / branch / "directions" / "index.html"
    info = CLINIC_CONTENT["branches"][branch]
    body = f'''<section class="subpage-hero shell"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><span>Направления</span></nav><div class="subpage-hero-grid"><div><p class="eyebrow">{h(info['eyebrow'])} · ВЫБОР НАПРАВЛЕНИЯ</p><h1>Изучите варианты.<br><em>Вы решаете, что открыть.</em></h1><p>Интерактив помогает ориентироваться в каталоге. Он не оценивает состояние здоровья и не подбирает лечение.</p><a class="button button-primary" href="{h(branch_route(page,branch,'prices/index.html'))}">Все 254 цены ↗</a></div><figure><img src="{h(repo_asset(page,info['image']))}" alt="{h(info['imageAlt'])}" width="900" height="620"></figure></div></section>
<section class="section-shell directions-selector"><div class="shell section-heading-row"><div><p class="eyebrow">10 НАПРАВЛЕНИЙ · {len(SERVICES)} ПОЗИЦИЙ</p><h2>Выбор — <em>за вами.</em></h2></div><p>Переключайте разделы и конкретные услуги. Цена относится к опубликованной позиции, не к полному индивидуальному плану.</p></div><div class="shell">{selector_markup(page,branch,'directions')}</div></section>
<section class="section-shell service-directory"><div class="shell section-heading-row"><div><p class="eyebrow">СТРУКТУРА ПРАЙСА</p><h2>Все <em>разделы</em></h2></div><p>Нажмите на направление, чтобы открыть отдельную страницу с подтверждёнными позициями.</p></div><div class="shell direction-card-grid">{render_direction_cards(page,branch)}</div></section>'''
    write(page, shell(page, title=f"Направления — {info['fullName']}", description="Интерактивный выбор направления и позиции каталога", body=body, branch=branch, active="directions", page_type="directions"))


def render_direction_cards(page: Path, branch: str) -> str:
    result = []
    for index, (code, details) in enumerate(CATEGORIES.items(), 1):
        href = relative_service_route(page, branch, code)
        result.append(f'''<a class="direction-card" data-category-card="{h(code)}" href="{h(href)}"><span class="section-index">{index:02d} / {details['count']:02d}</span><h3>{h(details['title'])}</h3><span class="direction-arrow" aria-hidden="true">↗</span></a>''')
    return "".join(result)


def render_service_page(branch: str, category: str) -> None:
    page = V2 / branch / "services" / f"{CATEGORY_SLUG[category]}.html"
    info = CLINIC_CONTENT["branches"][branch]
    cat = CATEGORIES[category]
    image = repo_asset(page, info["selectorImages"][category])
    entries = [SERVICE_BY_ID[service_id] for service_id in FEATURED[category]]
    cards = []
    for i, service in enumerate(entries, 1):
        route = relative_service_route(page, branch, category)
        link = route + "?service=" + quote(service["id"]) + "#selected-procedure"
        cards.append(f'''<a class="featured-price" href="{h(link)}" data-service-id="{h(service['id'])}"><span class="section-index">ВЫБРАТЬ · {i:02d}</span><strong>{h(service['name'])}</strong><span class="featured-price-value">{h(price_for(service,branch))}</span><span class="featured-price-arrow" aria-hidden="true">↗</span></a>''')
    body = f'''<section class="subpage-hero shell service-hero category-{h(category)}"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><a href="{h(branch_route(page,branch,'directions/index.html'))}">Направления</a><span>{h(cat['title'])}</span></nav><div class="service-hero-grid"><div class="service-hero-copy"><p class="eyebrow">НАПРАВЛЕНИЕ · {h(info['name'].upper())}</p><h1>{h(cat['title'])}</h1><p>{h(CLINIC_CONTENT['categoryDescriptions'][category])}</p><div class="service-hero-facts"><span><strong>{h(cat['count'])}</strong> опубликованных позиций</span><span>цены в каталоге филиала</span></div><button type="button" class="button button-primary" data-open-booking>Выбрать способ записи ↗</button></div><figure class="service-hero-image"><img src="{h(image)}" alt="Стоматологический приём в клинике {h(info['name'])}" width="900" height="660"><figcaption>Фото клиники · {h(info['name'])}</figcaption></figure></div></section>
<section class="section-shell category-price-section" id="selected-procedure"><div class="shell section-heading-row"><div><p class="eyebrow">ВАРИАНТЫ ИЗ ПРАЙСА</p><h2>Выберите <em>позицию.</em></h2></div><p>{h(SHARED['catalogNote'])}</p></div><div class="shell featured-price-list">{''.join(cards)}</div><div class="shell category-actions"><a class="button button-secondary" href="{h(branch_route(page,branch,'prices/index.html'))}#{h(category)}">Все {h(cat['count'])} позиции направления</a><a class="text-button" href="{h(branch_route(page,branch,'directions/index.html'))}">← Другие направления</a></div><div class="shell selected-service-deep-link" data-service-detail aria-live="polite"><p class="eyebrow">ВЫБРАННАЯ ПОЗИЦИЯ</p><h3 data-detail-name></h3><strong data-detail-price></strong><p>Выбранная позиция останется видна в модальном окне записи. Она не передаётся в DentalPRO.</p><button class="button button-primary" type="button" data-detail-booking data-open-booking>Как вам удобнее записаться?</button></div></section>
<section class="section-shell clinical-note"><div class="shell clinical-note-inner"><span class="note-number">i</span><div><p class="eyebrow">ИНФОРМАЦИЯ О СТОИМОСТИ</p><h2>Отдельная цена —<br><em>часть общего плана.</em></h2><p>{h(SHARED['catalogNote'])}</p></div><a class="text-button" href="{h(branch_route(page,branch,'prices/index.html'))}">Полный каталог цен ↗</a></div></section>'''
    write(page, shell(page, title=f"{cat['title']} — {info['fullName']}", description=CLINIC_CONTENT["categoryDescriptions"][category], body=body, branch=branch, active="directions", page_type="service", category=category))


def render_doctor_index(branch: str) -> None:
    page = V2 / branch / "doctors" / "index.html"
    info = CLINIC_CONTENT["branches"][branch]
    cards = []
    for index, doctor in enumerate(DOCTORS, 1):
        href = branch_route(page, branch, f"doctors/{doctor['slug']}.html")
        cards.append(f'''<article class="doctor-profile-card"><a class="doctor-photo-link" href="{h(href)}"><img src="{h(repo_asset(page,doctor['portrait']))}" alt="Портрет врача {h(doctor['name'])}" loading="lazy"><span class="section-index">СПЕЦИАЛИСТ · {index:02d}</span></a><div class="doctor-profile-copy"><h2><a href="{h(href)}">{h(doctor['name'])}</a></h2><p>{h(doctor['role'])}</p><span class="doctor-experience">Стаж {h(doctor['experience'])}</span><a class="text-button" href="{h(href)}">Профиль и обучение ↗</a></div></article>''')
    body = f'''<section class="subpage-hero shell doctors-hero"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><span>Врачи</span></nav><div class="subpage-title-row"><div><p class="eyebrow">КОМАНДА · {h(info['name'].upper())}</p><h1>Специалисты<br><em>клиники.</em></h1></div><p>Профили собраны по сведениям официальных страниц клиники. Стаж и специализации приведены так, как их публикует филиал.</p></div></section><section class="section-shell doctors-directory"><div class="shell doctor-profile-grid">{''.join(cards)}</div></section><section class="shell compact-cta"><div><p class="eyebrow">ПЕРВЫЙ ШАГ</p><h2>Уточните удобный<br><em>способ записи.</em></h2></div><button type="button" class="button button-primary" data-open-booking>Открыть варианты записи ↗</button></section>'''
    write(page, shell(page, title=f"Врачи — {info['fullName']}", description=f"Врачи стоматологии {info['name']} и опубликованные сведения о специализации", body=body, branch=branch, active="doctors", page_type="doctors"))


def render_doctor_detail(branch: str, doctor: dict) -> None:
    page = V2 / branch / "doctors" / f"{doctor['slug']}.html"
    info = CLINIC_CONTENT["branches"][branch]
    portrait = repo_asset(page, doctor["portrait"])
    certs = "".join(f'<a class="certificate-link" href="{h(cert["url"])}" target="_blank" rel="noopener noreferrer"><span class="certificate-mark" aria-hidden="true">↗</span><span>{h(cert["title"])}</span></a>' for cert in doctor["certificates"])
    cert_section = f'''<section class="profile-section certificates-section"><p class="eyebrow">ПУБЛИКОВАННЫЕ ДОКУМЕНТЫ</p><h2>Сертификаты <em>обучения</em></h2><div class="certificate-grid">{certs}</div><p class="source-note">Документы открываются с официального сайта клиники.</p></section>''' if certs else ""
    body = f'''<section class="doctor-detail-hero shell"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><a href="{h(branch_route(page,branch,'doctors/index.html'))}">Врачи</a><span>{h(doctor['shortName'])}</span></nav><div class="doctor-detail-grid"><figure class="doctor-detail-photo"><img src="{h(portrait)}" alt="Портрет врача {h(doctor['name'])}"><figcaption>{h(info['fullName'])}</figcaption></figure><div class="doctor-detail-copy"><p class="eyebrow">{h(info['name'].upper())} · СПЕЦИАЛИСТ</p><h1>{h(doctor['name'])}</h1><p class="doctor-role-large">{h(doctor['role'])}</p><div class="experience-stamp"><strong>{h(doctor['experience'])}</strong><span>стаж работы<br>по опубликованной странице</span></div><p>{h(doctor['practice'])}</p><button class="button button-primary" type="button" data-open-booking>Выбрать способ записи ↗</button></div></div></section>
<section class="section-shell doctor-profile-content"><div class="shell profile-content-grid"><div class="profile-section"><p class="eyebrow">ОБРАЗОВАНИЕ И ОБУЧЕНИЕ</p><h2>Опубликованные<br><em>сведения.</em></h2><p>{h(doctor['education'])}</p><a class="source-note" href="{h(doctor['source'])}" target="_blank" rel="noopener noreferrer">Официальная страница клиники ↗</a></div><div class="profile-section profile-practice"><p class="eyebrow">ПРАКТИКА</p><h2>Основные <em>сведения</em></h2><p>{h(doctor['practice'])}</p><p>На этой странице приведена информация, опубликованная клиникой. Подходящий специалист и план действий обсуждаются на приёме.</p></div></div>{cert_section}</section>
<section class="shell profile-return"><a class="text-button" href="{h(branch_route(page,branch,'doctors/index.html'))}">← Вернуться к каталогу врачей</a><button type="button" class="button button-secondary" data-open-booking>Как записаться?</button></section>'''
    write(page, shell(page, title=f"{doctor['name']} — {info['name']}", description=f"Официально опубликованные сведения о враче {doctor['name']}", body=body, branch=branch, active="doctors", page_type="doctor"))


def render_prices(branch: str) -> None:
    page = V2 / branch / "prices" / "index.html"
    info = CLINIC_CONTENT["branches"][branch]
    cat_filters = []
    for key, category in CATEGORIES.items():
        cat_filters.append(f'<button type="button" class="catalog-filter" data-catalog-filter="{h(key)}" aria-pressed="false">{h(category["title"])} <span>{category["count"]}</span></button>')
    all_rows = []
    for key, category in CATEGORIES.items():
        rows = []
        target = relative_service_route(page, branch, key)
        for service in BY_CATEGORY[key]:
            name = h(service["name"])
            service_id = h(service["id"])
            code = h(service["id"])
            price = h(price_for(service, branch))
            rows.append(f'''<details class="price-item" data-price-item data-service-id="{service_id}" data-category="{h(key)}" id="{service_id}"><summary class="price-summary"><span class="price-code">{code}</span><span class="price-name">{name}</span><strong class="price-value">{price}</strong><span class="price-chevron" aria-hidden="true">⌄</span></summary><div class="price-detail"><p>{h(SHARED['catalogNote'])}</p><div class="price-detail-actions"><a href="{h(target)}?service={quote(service['id'])}#selected-procedure">Подробнее о направлении ↗</a><button type="button" class="button button-small" data-open-booking data-service-id="{service_id}">Обсудить запись</button></div></div></details>''')
        all_rows.append(f'''<section class="catalog-category" id="{h(key)}" data-catalog-category="{h(key)}"><header class="catalog-category-heading"><div><span class="eyebrow">РАЗДЕЛ {len(all_rows)+1:02d}</span><h2>{h(category['title'])}</h2></div><span class="category-total">{category['count']} позиций</span></header><div class="price-items">{''.join(rows)}</div></section>''')
    body = f'''<section class="subpage-hero shell prices-hero"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><span>Прайс</span></nav><div class="subpage-title-row"><div><p class="eyebrow">ПОЛНЫЙ КАТАЛОГ · {h(info['name'].upper())}</p><h1>Цены на отдельные<br><em>процедуры.</em></h1><p>{h(SHARED['catalogNote'])}</p></div><div class="catalog-count-orbit"><strong>{len(SERVICES)}</strong><span>позиций<br>10 направлений</span></div></div></section>
<section class="section-shell catalog-section"><div class="shell catalog-toolbar"><label class="catalog-search-label" for="catalog-search">Найти по названию или коду</label><div class="catalog-search-wrap"><span aria-hidden="true">⌕</span><input id="catalog-search" type="search" data-catalog-search placeholder="Например, имплантация или svc_…" autocomplete="off"><button type="button" data-clear-search aria-label="Очистить поиск" hidden>×</button></div><p class="catalog-result-count" role="status" aria-live="polite" data-catalog-count>Показано {len(SERVICES)} услуг</p><div class="catalog-filters" role="group" aria-label="Фильтр по направлениям"><button type="button" class="catalog-filter is-active" data-catalog-filter="all" aria-pressed="true">Все направления <span>{len(SERVICES)}</span></button>{''.join(cat_filters)}</div><p class="catalog-no-results" data-catalog-empty hidden>Ничего не найдено. Измените запрос или выберите все направления.</p></div><div class="shell catalog-content">{''.join(all_rows)}</div></section><section class="shell compact-cta"><div><p class="eyebrow">СЛЕДУЮЩИЙ ШАГ</p><h2>Обсудите цену<br><em>и план с врачом.</em></h2></div><button type="button" class="button button-primary" data-open-booking>Открыть способы записи ↗</button></section>'''
    write(page, shell(page, title=f"Прайс — {info['fullName']}", description=f"Все 254 позиции прейскуранта стоматологии {info['name']}, поиск и фильтр по направлениям", body=body, branch=branch, active="prices", page_type="prices"))


def render_contacts(branch: str) -> None:
    page = V2 / branch / "contacts" / "index.html"
    info = CLINIC_CONTENT["branches"][branch]
    map_href = "https://yandex.ru/maps/?text=" + quote(info["address"])
    if branch == "ispanskie":
        booking_intro = "Для записи именно в Испанские кварталы используйте телефон. Официальная ссылка сайта на онлайн-запись сейчас ведёт в филиал Прокшино."
        booking_channel = "DentalPRO · филиал Прокшино"
        booking_heading = "Онлайн-запись<br><em>на Прокшино.</em>"
        booking_details = "Выбранный на этой странице филиал не передаётся в DentalPRO. Если вам нужен приём в Испанских кварталах, позвоните в регистратуру."
        booking_button = "Открыть DentalPRO · Прокшино ↗"
    else:
        booking_intro = "Врача и время можно выбрать в официальной системе DentalPRO клиники Прокшино."
        booking_channel = "DentalPRO · Прокшино"
        booking_heading = "Выбрать врача<br><em>и время.</em>"
        booking_details = "Онлайн-система открывается на официальной странице записи. Направление из preview автоматически не передаётся."
        booking_button = "Продолжить в DentalPRO ↗"
    body = f'''<section class="subpage-hero shell contacts-hero"><nav class="breadcrumbs" aria-label="Хлебные крошки"><a href="{h(branch_route(page,branch,'index.html'))}">Главная</a><span>Контакты</span></nav><div class="subpage-title-row"><div><p class="eyebrow">{h(info['name'].upper())} · МОСКВА</p><h1>Как нас<br><em>найти.</em></h1></div><p>{h(booking_intro)}</p></div></section><section class="section-shell contact-detail-section"><div class="shell contact-detail-grid"><article class="contact-card contact-card-primary"><span class="contact-index">01 / СВЯЗЬ</span><p class="eyebrow">ТЕЛЕФОН РЕГИСТРАТУРЫ</p><a class="contact-large-number" href="{h(SHARED['tel'])}">{h(SHARED['phone'])}</a><p>Единый опубликованный номер регистратуры филиалов ДантистЪ.</p><button type="button" class="button button-primary" data-open-booking>Как вам удобнее записаться?</button><a href="{h(SHARED['whatsapp'])}" target="_blank" rel="noopener noreferrer">Написать в WhatsApp ↗</a><a href="{h(SHARED['telegram'])}" target="_blank" rel="noopener noreferrer">Telegram · канал/чат ↗</a></article><article class="contact-card"><span class="contact-index">02 / АДРЕС</span><p class="eyebrow">{h(info['name'].upper())}</p><h2>{h(info['address'])}</h2><p>Москва · Коммунарка<br>{h(SHARED['hours'])}</p><a class="button button-secondary" href="{h(map_href)}" target="_blank" rel="noopener noreferrer">Построить маршрут ↗</a></article><article class="contact-card booking-card"><span class="contact-index">03 / ONLINE</span><p class="eyebrow">{h(booking_channel)}</p><h2>{booking_heading}</h2><p>{h(booking_details)}</p><a class="button button-primary" href="{h(SHARED['dentalpro'])}" target="_blank" rel="noopener noreferrer">{h(booking_button)}</a></article></div></section>'''
    write(page, shell(page, title=f"Контакты — {info['fullName']}", description=f"Телефон, адрес и реальные способы записи в клинику {info['name']}", body=body, branch=branch, active="contacts", page_type="contacts"))

def render_data_js() -> None:
    data = {
        "categories": CATEGORIES,
        "services": SERVICES,
        "doctors": DOCTORS,
        "branches": CLINIC_CONTENT["branches"],
        "shared": SHARED,
        "categoryDescriptions": CLINIC_CONTENT["categoryDescriptions"],
        "featuredServiceIds": FEATURED,
        "source": {
            "branch": "tech/dental-master-foundation-2026",
            "commit": "a1607f79c28aafb7d2ee73818cdd5d996f7f5d3f",
            "verifiedDate": "2026-11-09",
        },
    }
    write(ASSETS / "v2-data.js", "window.DENTAL_V2 = " + safe_js_json(data) + ";")


def render() -> int:
    validate_source_data()
    render_data_js()
    render_chooser()
    total = 1
    for branch in BRANCHES:
        render_home(branch)
        render_directions(branch)
        total += 2
        for category in CATEGORIES:
            render_service_page(branch, category)
            total += 1
        render_doctor_index(branch)
        total += 1
        for doctor in DOCTORS:
            render_doctor_detail(branch, doctor)
            total += 1
        render_prices(branch)
        render_contacts(branch)
        total += 2
    manifest = {
        "entry": "index.html",
        "branches": {
            branch: {
                "home": f"{branch}/index.html",
                "directions": f"{branch}/directions/index.html",
                "services": [f"{branch}/services/{slug}.html" for slug in CATEGORY_SLUG.values()],
                "doctors": [f"{branch}/doctors/index.html"] + [f"{branch}/doctors/{doctor['slug']}.html" for doctor in DOCTORS],
                "prices": f"{branch}/prices/index.html",
                "contacts": f"{branch}/contacts/index.html",
            }
            for branch in BRANCHES
        },
        "serviceCount": len(SERVICES),
        "source": "tech/dental-master-foundation-2026@a1607f79c28aafb7d2ee73818cdd5d996f7f5d3f",
    }
    write(V2 / "route-manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"V2_BUILD_PASS routes={total} serviceRecords={len(SERVICES)} categories={len(CATEGORIES)} doctorProfiles={len(DOCTORS)*len(BRANCHES)}")
    return total


if __name__ == "__main__":
    try:
        render()
    except Exception as exc:
        print(f"V2_BUILD_FAIL: {exc}", file=sys.stderr)
        raise
