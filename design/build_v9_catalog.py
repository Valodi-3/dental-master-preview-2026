#!/usr/bin/env python3
"""
Synchronizes v9 interactive catalog directly from v2/data/services_master.json
Single source of truth for all prices and service titles.
Removes any unverified durations.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SERVICES_PATH = ROOT / "v2" / "data" / "services_master.json"
OUTPUT_PATH = ROOT / "v9" / "assets" / "catalog-data.js"

with open(SERVICES_PATH, encoding="utf-8") as f:
    services = {s["id"]: s for s in json.load(f)}

# Approved configuration mapping
CATEGORIES_CONFIG = {
    "treatment": {
        "categoryName": "Лечение зубов",
        "icon": "🦷",
        "serviceIds": ["svc_treatment_027", "svc_treatment_028", "svc_treatment_029"],
        "defaultImg": "../design/assets/prokshino/treatment.webp",
        "meta": {
            "svc_treatment_027": {
                "shortName": "Восстановление зуба пломбой (1 поверхность)",
                "tag": "Кариес 1 пов.",
                "desc": "Лечение кариеса современными светоотверждаемыми композитами с восстановлением анатомии зуба."
            },
            "svc_treatment_028": {
                "shortName": "Восстановление зуба пломбой (2 поверхности)",
                "tag": "Кариес 2 пов.",
                "desc": "Пломбирование при контактном кариесе с созданием правильного контактного пункта зубной нити."
            },
            "svc_treatment_029": {
                "shortName": "Восстановление зуба пломбой (3 поверхности)",
                "tag": "Кариес 3 пов.",
                "desc": "Послойное анатомическое восстановление разрушенной коронковой части зуба фотополимерами."
            }
        }
    },
    "endodontics": {
        "categoryName": "Микроскопия Zeiss",
        "icon": "🔬",
        "serviceIds": ["svc_endodontics_055", "svc_endodontics_048", "svc_endodontics_049"],
        "defaultImg": "../design/assets/prokshino/microscope.webp",
        "meta": {
            "svc_endodontics_055": {
                "shortName": "Первичное эндодонтическое лечение (1 канал)",
                "tag": "Лечение канала",
                "desc": "Лечение корневых каналов под увеличением до 25 крат немецкого микроскопа Carl Zeiss."
            },
            "svc_endodontics_048": {
                "shortName": "Инструментальная и медикаментозная обработка канала",
                "tag": "Обработка канала",
                "desc": "Прецизионная механическая обработка никель-титановыми ротационными инструментами."
            },
            "svc_endodontics_049": {
                "shortName": "Временное пломбирование лекарственным препаратом",
                "tag": "Терапия канала",
                "desc": "Антисептическая терапия кальцийсодержащими препаратами для снятия воспаления в периодонте."
            }
        }
    },
    "implantation": {
        "categoryName": "Имплантация",
        "icon": "🔩",
        "serviceIds": ["svc_implantation_091", "svc_implantation_093", "svc_implantation_092"],
        "defaultImg": "../design/assets/prokshino/treatment.webp",
        "meta": {
            "svc_implantation_091": {
                "shortName": "Установка имплантата Osstem / Dentium",
                "tag": "Имплантат Osstem",
                "desc": "Операция установки имплантата проверенной корейской системы с высокой степенью приживаемости."
            },
            "svc_implantation_093": {
                "shortName": "Установка имплантата Straumann (Швейцария)",
                "tag": "Имплантат Straumann",
                "desc": "Золотой стандарт мировой дентальной имплантологии с ускоренной остеоинтеграцией."
            },
            "svc_implantation_092": {
                "shortName": "Установка формирователя десны",
                "tag": "Формирователь десны",
                "desc": "Создание естественного и эстетичного контура десны вокруг будущей коронки."
            }
        }
    },
    "orthodontics": {
        "categoryName": "Ортодонтия и прикус",
        "icon": "✨",
        "serviceIds": ["svc_orthodontics_211", "svc_orthodontics_212", "svc_consultations_002"],
        "defaultImg": "../design/assets/prokshino/orthodontics.webp",
        "meta": {
            "svc_orthodontics_211": {
                "shortName": "Фиксация брекет-системы металл (лигатурная, 1 челюсть)",
                "tag": "Брекеты металл",
                "desc": "Классическая брекет-система для точного исправления нарушений прикуса любой сложности."
            },
            "svc_orthodontics_212": {
                "shortName": "Фиксация брекет-системы металл (самолигирующая, 1 челюсть)",
                "tag": "Брекеты Damon",
                "desc": "Низкотрениевая система с комфортным перемещением зубов и меньшим числом визитов."
            },
            "svc_consultations_002": {
                "shortName": "Первичный прием врача-ортодонта с консультацией",
                "tag": "Консультация ортодонта",
                "desc": "Диагностический осмотр, анализ смыкания зубных рядов и составление плана коррекции."
            }
        }
    },
    "prosthetics": {
        "categoryName": "Протезирование",
        "icon": "👑",
        "serviceIds": ["svc_prosthetics_127", "svc_prosthetics_122", "svc_prosthetics_117"],
        "defaultImg": "../design/assets/prokshino/hero-clinic.webp",
        "meta": {
            "svc_prosthetics_127": {
                "shortName": "Восстановление зуба металлокерамической коронкой",
                "tag": "Металлокерамика",
                "desc": "Прочная ортопедическая конструкция для восстановления жевательной функции зуба."
            },
            "svc_prosthetics_122": {
                "shortName": "Коронка с использованием циркониевой вкладки",
                "tag": "Цирконий",
                "desc": "Безметалловая коронка высшей эстетики с биосовместимой циркониевой вкладкой."
            },
            "svc_prosthetics_117": {
                "shortName": "Временная защитная коронка прямым методом",
                "tag": "Временная коронка",
                "desc": "Защита обточенного зуба от температурных факторов на период изготовления постоянной коронки."
            }
        }
    },
    "hygiene": {
        "categoryName": "Гигиена и уход",
        "icon": "🌿",
        "serviceIds": ["svc_hygiene_012", "svc_hygiene_014", "svc_hygiene_013"],
        "defaultImg": "../design/assets/prokshino/hygiene.webp",
        "meta": {
            "svc_hygiene_012": {
                "shortName": "Профессиональная комплексная гигиена полости рта",
                "tag": "Комплекс AirFlow",
                "desc": "Снятие зубного налета AirFlow, ультразвуковое удаление камня и полировка пастами."
            },
            "svc_hygiene_014": {
                "shortName": "Удаление зубных отложений ультразвуком (1 зуб)",
                "tag": "Ультразвук",
                "desc": "Деликатное снятие наддесневых и поддесневых отложений без травмирования эмали."
            },
            "svc_hygiene_013": {
                "shortName": "Реминерализирующая терапия эмали",
                "tag": "Реминерализация",
                "desc": "Укрепление эмали минеральными компонентами для снижения чувствительности."
            }
        }
    }
}

catalog_export = {}

for cat_key, cfg in CATEGORIES_CONFIG.items():
    cat_items = []
    for sid in cfg["serviceIds"]:
        svc = services.get(sid)
        if not svc:
            continue
        m = cfg["meta"].get(sid, {})
        price_prok = svc["pricing"]["prokshino"]["formatted"]
        price_isp = svc["pricing"]["ispanskie"]["formatted"]
        cat_items.append({
            "id": sid,
            "name": m.get("shortName", svc["name"]),
            "officialFullName": svc["name"],
            "shortDesc": m.get("desc", ""),
            "tag": m.get("tag", "Процедура"),
            "price": price_prok,
            "priceIspanskie": price_isp,
            "img": cfg["defaultImg"]
        })
    catalog_export[cat_key] = {
        "categoryName": cfg["categoryName"],
        "icon": cfg["icon"],
        "procedures": cat_items
    }

js_content = f"""/**
 * DENTAL MASTER V9 — SINGLE SOURCE OF TRUTH CATALOG DATA
 * Generated automatically from v2/data/services_master.json
 * NO unverified durations. Authentic official prices.
 */
window.DENTAL_V9_CATALOG = {json.dumps(catalog_export, ensure_ascii=False, indent=2)};
"""

OUTPUT_PATH.write_text(js_content, encoding="utf-8")
print(f"Successfully generated {OUTPUT_PATH} ({len(catalog_export)} categories, {sum(len(c['procedures']) for c in catalog_export.values())} procedures).")
