#!/usr/bin/env python3
"""
Dental Master X — Single Source of Truth Catalog Builder
Builds dx/assets/js/dx-catalog.js from v2/data/services_master.json
Stores verified prices for both branches: Ispanskie Kvartaly and Prokshino.
Zero fake durations.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVICES_PATH = ROOT / "v2" / "data" / "services_master.json"
OUTPUT_PATH = ROOT / "dx" / "assets" / "js" / "dx-catalog.js"

with open(SERVICES_PATH, encoding="utf-8") as f:
    services = {s["id"]: s for s in json.load(f)}

# 6 Primary Clinical Directions
CATEGORIES_CONFIG = {
    "treatment": {
        "id": "treatment",
        "name": "Лечение кариеса",
        "icon": "🦷",
        "badge": "Терапия",
        "sub": "Восстановление анатомической формы и эстетики зуба",
        "imgIspanskie": "../design/assets/ispanskie/treatment.webp",
        "imgProkshino": "../design/assets/prokshino/treatment.webp",
        "serviceIds": ["svc_treatment_027", "svc_treatment_028", "svc_treatment_029"],
        "meta": {
            "svc_treatment_027": {
                "shortName": "Восстановление зуба пломбой (1 поверхность)",
                "tag": "Кариес 1 пов.",
                "desc": "Лечение поверхностного и среднего кариеса современными светоотверждаемыми композитами с восстановлением анатомии зуба."
            },
            "svc_treatment_028": {
                "shortName": "Восстановление зуба пломбой (2 поверхности)",
                "tag": "Контактный кариес",
                "desc": "Пломбирование при межзубном контактном кариесе с созданием плотного контактного пункта для зубной нити."
            },
            "svc_treatment_029": {
                "shortName": "Восстановление зуба пломбой (3 поверхности)",
                "tag": "Разрушение 3 пов.",
                "desc": "Послойное анатомическое восстановление разрушенной коронковой части зуба фотополимерными нанокомпозитами."
            }
        }
    },
    "endodontics": {
        "id": "endodontics",
        "name": "Микроскопия Zeiss",
        "icon": "🔬",
        "badge": "Эндодонтия",
        "sub": "Прецизионное лечение сложных корневых каналов",
        "imgIspanskie": "../design/assets/ispanskie/gallery-5.jpg",
        "imgProkshino": "../design/assets/prokshino/microscope.webp",
        "serviceIds": ["svc_endodontics_055", "svc_endodontics_048", "svc_endodontics_049"],
        "meta": {
            "svc_endodontics_055": {
                "shortName": "Первичное эндодонтическое лечение (1 канал)",
                "tag": "Лечение канала",
                "desc": "Прецизионная механическая и медикаментозная обработка корневого канала под оптическим увеличением до 25 крат."
            },
            "svc_endodontics_048": {
                "shortName": "Инструментальная и антисептическая обработка",
                "tag": "Обработка канала",
                "desc": "Очищение инфицированных каналов никель-титановыми ротационными инструментами и ультразвуковая дезинфекция."
            },
            "svc_endodontics_049": {
                "shortName": "Временное пломбирование лечебной пастой",
                "tag": "Терапия периодонтита",
                "desc": "Введение противовоспалительных кальцийсодержащих препаратов для надежного устранения воспаления в тканях периодонта."
            }
        }
    },
    "implantation": {
        "id": "implantation",
        "name": "Имплантация",
        "icon": "🔩",
        "badge": "Хирургия",
        "sub": "Надежное восстановление утраченных зубов под ключ",
        "imgIspanskie": "../design/assets/ispanskie/hero-clinic.webp",
        "imgProkshino": "../design/assets/prokshino/treatment.webp",
        "serviceIds": ["svc_implantation_091", "svc_implantation_093", "svc_implantation_092"],
        "meta": {
            "svc_implantation_091": {
                "shortName": "Установка имплантата Osstem / Dentium",
                "tag": "Имплантат Osstem",
                "desc": "Хирургическая установка корейской имплантационной системы с приживаемостью более 98.8% и надежной остеоинтеграцией."
            },
            "svc_implantation_093": {
                "shortName": "Установка имплантата Straumann (Швейцария)",
                "tag": "Straumann Swiss",
                "desc": "Золотой стандарт мировой дентальной имплантологии с поверхностью SLActive для сокращенных сроков приживления."
            },
            "svc_implantation_092": {
                "shortName": "Установка формирователя десны",
                "tag": "Пластика десны",
                "desc": "Создание естественного и гармоничного десневого контура перед изготовлением и установкой постоянной коронки."
            }
        }
    },
    "orthodontics": {
        "id": "orthodontics",
        "name": "Ортодонтия и прикус",
        "icon": "✨",
        "badge": "Эстетика улыбки",
        "sub": "Исправление положения зубов и гармонизация профиля",
        "imgIspanskie": "../design/assets/ispanskie/orthodontics.jpg",
        "imgProkshino": "../design/assets/prokshino/orthodontics.webp",
        "serviceIds": ["svc_orthodontics_211", "svc_orthodontics_212", "svc_consultations_002"],
        "meta": {
            "svc_orthodontics_211": {
                "shortName": "Фиксация брекет-системы металл (лигатурная, 1 челюсть)",
                "tag": "Брекеты металл",
                "desc": "Классическая проверенная брекет-система для точной коррекции нарушений прикуса любой сложности у подростков и взрослых."
            },
            "svc_orthodontics_212": {
                "shortName": "Фиксация брекет-системы металл (самолигирующая, 1 челюсть)",
                "tag": "Брекеты Damon",
                "desc": "Низкотрениевые замочки с мягкими биологическими силами. Комфортное перемещение зубов и более редкие визиты к врачу."
            },
            "svc_consultations_002": {
                "shortName": "Первичный прием врача-ортодонта с консультацией",
                "tag": "Диагностика прикуса",
                "desc": "Клинический осмотр, фотопротокол лица и зубных рядов, анализ прикуса и составление подробного плана коррекции."
            }
        }
    },
    "prosthetics": {
        "id": "prosthetics",
        "name": "Протезирование",
        "icon": "👑",
        "badge": "Ортопедия",
        "sub": "Эстетические коронки, виниры и вкладки высшего класса",
        "imgIspanskie": "../design/assets/ispanskie/gallery-3.jpg",
        "imgProkshino": "../design/assets/prokshino/hero-clinic.webp",
        "serviceIds": ["svc_prosthetics_127", "svc_prosthetics_122", "svc_prosthetics_117"],
        "meta": {
            "svc_prosthetics_127": {
                "shortName": "Восстановление зуба металлокерамической коронкой",
                "tag": "Металлокерамика",
                "desc": "Классическая ортопедическая конструкция для восстановления жевательной функции и целостности зубного ряда."
            },
            "svc_prosthetics_122": {
                "shortName": "Коронка с использованием циркониевой вкладки",
                "tag": "Цирконий прецизионный",
                "desc": "Высокоэстетичная безметалловая реставрация из биосовместимого диоксида циркония с естественной полупрозрачностью эмали."
            },
            "svc_prosthetics_117": {
                "shortName": "Временная защитная коронка прямым методом",
                "tag": "Временная защита",
                "desc": "Защита обточенного зуба от температурных факторов и сохранение эстетики на период изготовления постоянной конструкции."
            }
        }
    },
    "hygiene": {
        "id": "hygiene",
        "name": "Профгигиена и уход",
        "icon": "🌿",
        "badge": "Профилактика",
        "sub": "Бережное спа-очищение зубов и укрепление эмали",
        "imgIspanskie": "../design/assets/ispanskie/hygiene.webp",
        "imgProkshino": "../design/assets/prokshino/hygiene.webp",
        "serviceIds": ["svc_hygiene_012", "svc_hygiene_014", "svc_hygiene_013"],
        "meta": {
            "svc_hygiene_012": {
                "shortName": "Профессиональная комплексная гигиена полости рта",
                "tag": "Комплекс AirFlow",
                "desc": "Снятие плотного пигментированного налета мелкодисперсным AirFlow, ультразвуковое удаление камня и полировка пастами."
            },
            "svc_hygiene_014": {
                "shortName": "Удаление зубных отложений ультразвуком (1 зуб)",
                "tag": "Ультразвук",
                "desc": "Деликатное снятие наддесневых и поддесневых минерализованных отложений без микроповреждения здоровой эмали."
            },
            "svc_hygiene_013": {
                "shortName": "Реминерализирующая терапия эмали",
                "tag": "Реминерализация",
                "desc": "Глубокое насыщение эмали минеральными соединениями кальция и фосфора для снятия повышенной чувствительности."
            }
        }
    }
}

catalog_export = {
    "branches": {
        "ispanskie": {
            "key": "ispanskie",
            "name": "Испанские кварталы",
            "fullName": "ДантистЪ · Испанские кварталы",
            "headline": "Лечение зубов для всей семьи в Испанских кварталах",
            "lead": "Узнайте точную стоимость процедур, познакомьтесь с врачами и выберите удобное время приёма в спокойной и заботливой обстановке.",
            "address": "Москва, Коммунарка, улица Магеллана, 5",
            "metro": "м. Прокшино / Ольховая",
            "phone": "+7 (904) 519-96-97",
            "phoneClean": "+79045199697",
            "hours": "Ежедневно 09:00–21:00",
            "badge": "Основной филиал · Семейная стоматология",
            "heroPhoto": "../design/assets/ispanskie/gallery-5.jpg",
            "heroPhotoAlt": "Кабинет стоматологии филиала Испанские кварталы",
            "gallery": [
                {"src": "../design/assets/ispanskie/gallery-5.jpg", "title": "Лечебный кабинет с современным креслом", "cat": "cabinets"},
                {"src": "../design/assets/ispanskie/gallery-2.jpg", "title": "Зона консультации и стоматологического осмотра", "cat": "cabinets"},
                {"src": "../design/assets/ispanskie/gallery-7.jpg", "title": "Пациент оценивает результат лечения в зеркале", "cat": "interior"},
                {"src": "../design/assets/ispanskie/gallery-6.jpg", "title": "Приём врача-стоматолога в кабинете", "cat": "cabinets"},
                {"src": "../design/assets/ispanskie/gallery-1.jpg", "title": "Стерилизационный блок и стандарты антисептики", "cat": "equipment"},
                {"src": "../design/assets/ispanskie/gallery-8.jpg", "title": "Холл клиники и комфортная зона ожидания", "cat": "interior"}
            ]
        },
        "prokshino": {
            "key": "prokshino",
            "name": "Прокшино",
            "fullName": "ДантистЪ · Прокшино",
            "headline": "Прецизионная стоматология и микроскопия Zeiss в Прокшино",
            "lead": "Точная диагностика, немецкая оптика Carl Zeiss до 25 крат, бережная имплантация и открытый официальный прейскурант.",
            "address": "Москва, поселение Сосенское, улица Лобановский Лес, д. 11",
            "metro": "м. Прокшино (4 мин пешком)",
            "phone": "+7 (904) 519-96-97",
            "phoneClean": "+79045199697",
            "hours": "Ежедневно 09:00–21:00",
            "badge": "Технологичный филиал · Микроскопия Zeiss",
            "heroPhoto": "../design/assets/prokshino/hero-clinic.webp",
            "heroPhotoAlt": "Холл и кабинет клиники ДантистЪ Прокшино",
            "gallery": [
                {"src": "../design/assets/prokshino/hero-clinic.webp", "title": "Главный холл и зона консультации пациентов", "cat": "interior"},
                {"src": "../design/assets/prokshino/microscope.webp", "title": "Операционный кабинет с микроскопом Carl Zeiss", "cat": "equipment"},
                {"src": "../design/assets/prokshino/treatment.webp", "title": "Хирургический кабинет имплантации и навигации", "cat": "cabinets"},
                {"src": "../design/assets/prokshino/orthodontics.webp", "title": "Ортодонтическое рабочее место и 3D-сетап", "cat": "equipment"},
                {"src": "../design/assets/prokshino/hygiene.webp", "title": "Кабинет гигиены полости рта и спа-протокола AirFlow", "cat": "cabinets"}
            ]
        }
    },
    "categories": []
}

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
            "officialName": svc["name"],
            "shortDesc": m.get("desc", ""),
            "tag": m.get("tag", "Процедура"),
            "prices": {
                "ispanskie": price_isp,
                "prokshino": price_prok
            },
            "images": {
                "ispanskie": cfg["imgIspanskie"],
                "prokshino": cfg["imgProkshino"]
            }
        })
    catalog_export["categories"].append({
        "id": cfg["id"],
        "name": cfg["name"],
        "icon": cfg["icon"],
        "badge": cfg["badge"],
        "sub": cfg["sub"],
        "procedures": cat_items
    })

js_content = f"""/**
 * DENTAL MASTER X — SINGLE SOURCE OF TRUTH CATALOG DATA
 * Extracted directly from v2/data/services_master.json
 * Official pricing for Ispanskie Kvartaly and Prokshino branches.
 * NO unverified durations.
 */
window.DX_CATALOG = {json.dumps(catalog_export, ensure_ascii=False, indent=2)};
"""

OUTPUT_PATH.write_text(js_content, encoding="utf-8")
print(f"Successfully generated {OUTPUT_PATH} ({len(catalog_export['categories'])} categories, SSOT for both branches).")
