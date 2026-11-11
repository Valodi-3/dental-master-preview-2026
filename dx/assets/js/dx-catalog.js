/**
 * DENTAL MASTER X — SINGLE SOURCE OF TRUTH CATALOG DATA
 * Extracted directly from v2/data/services_master.json
 * Official pricing for Ispanskie Kvartaly and Prokshino branches.
 * NO unverified durations.
 */
window.DX_CATALOG = {
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
        {
          "src": "../design/assets/ispanskie/gallery-5.jpg",
          "title": "Лечебный кабинет с современным креслом",
          "cat": "cabinets"
        },
        {
          "src": "../design/assets/ispanskie/gallery-2.jpg",
          "title": "Зона консультации и стоматологического осмотра",
          "cat": "cabinets"
        },
        {
          "src": "../design/assets/ispanskie/gallery-7.jpg",
          "title": "Пациент оценивает результат лечения в зеркале",
          "cat": "interior"
        },
        {
          "src": "../design/assets/ispanskie/gallery-6.jpg",
          "title": "Приём врача-стоматолога в кабинете",
          "cat": "cabinets"
        },
        {
          "src": "../design/assets/ispanskie/gallery-1.jpg",
          "title": "Стерилизационный блок и стандарты антисептики",
          "cat": "equipment"
        },
        {
          "src": "../design/assets/ispanskie/gallery-8.jpg",
          "title": "Холл клиники и комфортная зона ожидания",
          "cat": "interior"
        }
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
        {
          "src": "../design/assets/prokshino/hero-clinic.webp",
          "title": "Главный холл и зона консультации пациентов",
          "cat": "interior"
        },
        {
          "src": "../design/assets/prokshino/microscope.webp",
          "title": "Операционный кабинет с микроскопом Carl Zeiss",
          "cat": "equipment"
        },
        {
          "src": "../design/assets/prokshino/treatment.webp",
          "title": "Хирургический кабинет имплантации и навигации",
          "cat": "cabinets"
        },
        {
          "src": "../design/assets/prokshino/orthodontics.webp",
          "title": "Ортодонтическое рабочее место и 3D-сетап",
          "cat": "equipment"
        },
        {
          "src": "../design/assets/prokshino/hygiene.webp",
          "title": "Кабинет гигиены полости рта и спа-протокола AirFlow",
          "cat": "cabinets"
        }
      ]
    }
  },
  "categories": [
    {
      "id": "treatment",
      "name": "Лечение кариеса",
      "icon": "🦷",
      "badge": "Терапия",
      "sub": "Восстановление анатомической формы и эстетики зуба",
      "procedures": [
        {
          "id": "svc_treatment_027",
          "name": "Восстановление зуба пломбой (1 поверхность)",
          "officialName": "Восстановление зуба пломбой с использованием фотополимеров (1 поверхность)",
          "shortDesc": "Лечение поверхностного и среднего кариеса современными светоотверждаемыми композитами с восстановлением анатомии зуба.",
          "tag": "Кариес 1 пов.",
          "prices": {
            "ispanskie": "4 950 ₽",
            "prokshino": "4 950 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/treatment.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        },
        {
          "id": "svc_treatment_028",
          "name": "Восстановление зуба пломбой (2 поверхности)",
          "officialName": "Восстановление зуба пломбой с использованием фотополимеров (2 поверхности)",
          "shortDesc": "Пломбирование при межзубном контактном кариесе с созданием плотного контактного пункта для зубной нити.",
          "tag": "Контактный кариес",
          "prices": {
            "ispanskie": "5 500 ₽",
            "prokshino": "5 500 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/treatment.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        },
        {
          "id": "svc_treatment_029",
          "name": "Восстановление зуба пломбой (3 поверхности)",
          "officialName": "Восстановление зуба пломбой с использованием фотополимеров(3 поверхности)",
          "shortDesc": "Послойное анатомическое восстановление разрушенной коронковой части зуба фотополимерными нанокомпозитами.",
          "tag": "Разрушение 3 пов.",
          "prices": {
            "ispanskie": "6 050 ₽",
            "prokshino": "6 050 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/treatment.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        }
      ]
    },
    {
      "id": "endodontics",
      "name": "Микроскопия Zeiss",
      "icon": "🔬",
      "badge": "Эндодонтия",
      "sub": "Прецизионное лечение сложных корневых каналов",
      "procedures": [
        {
          "id": "svc_endodontics_055",
          "name": "Первичное эндодонтическое лечение (1 канал)",
          "officialName": "Первичное эндодонтическое лечение - однокорневой зуб без стоимости штифта и пломбы, все посещения. Радиовизиография. Инфильтрационная анестезия. Инструментальная и медикаментозная обработка хорошо проходимого корневого канала. Пломбирование корневого канала зуба гуттаперчивыми штифтами. Наложение временной пломбы",
          "shortDesc": "Прецизионная механическая и медикаментозная обработка корневого канала под оптическим увеличением до 25 крат.",
          "tag": "Лечение канала",
          "prices": {
            "ispanskie": "7 150 ₽",
            "prokshino": "7 150 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-5.jpg",
            "prokshino": "../design/assets/prokshino/microscope.webp"
          }
        },
        {
          "id": "svc_endodontics_048",
          "name": "Инструментальная и антисептическая обработка",
          "officialName": "Инструментальная и медикаментозная обработка хорошо проходимого корневого канала",
          "shortDesc": "Очищение инфицированных каналов никель-титановыми ротационными инструментами и ультразвуковая дезинфекция.",
          "tag": "Обработка канала",
          "prices": {
            "ispanskie": "1 320 ₽",
            "prokshino": "1 320 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-5.jpg",
            "prokshino": "../design/assets/prokshino/microscope.webp"
          }
        },
        {
          "id": "svc_endodontics_049",
          "name": "Временное пломбирование лечебной пастой",
          "officialName": "Временное пломбирование лекарственным препаратом корневого канала",
          "shortDesc": "Введение противовоспалительных кальцийсодержащих препаратов для надежного устранения воспаления в тканях периодонта.",
          "tag": "Терапия периодонтита",
          "prices": {
            "ispanskie": "880 ₽",
            "prokshino": "880 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-5.jpg",
            "prokshino": "../design/assets/prokshino/microscope.webp"
          }
        }
      ]
    },
    {
      "id": "implantation",
      "name": "Имплантация",
      "icon": "🔩",
      "badge": "Хирургия",
      "sub": "Надежное восстановление утраченных зубов под ключ",
      "procedures": [
        {
          "id": "svc_implantation_091",
          "name": "Установка имплантата Osstem / Dentium",
          "officialName": "Внутрикостная дентальная имплантация.(Операция установки имплантата Osstem/Dentium )",
          "shortDesc": "Хирургическая установка корейской имплантационной системы с приживаемостью более 98.8% и надежной остеоинтеграцией.",
          "tag": "Имплантат Osstem",
          "prices": {
            "ispanskie": "33 000 ₽",
            "prokshino": "33 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hero-clinic.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        },
        {
          "id": "svc_implantation_093",
          "name": "Установка имплантата Straumann (Швейцария)",
          "officialName": "Внутрикостная дентальная имплантация.(Операция установки имплантата Straumann)",
          "shortDesc": "Золотой стандарт мировой дентальной имплантологии с поверхностью SLActive для сокращенных сроков приживления.",
          "tag": "Straumann Swiss",
          "prices": {
            "ispanskie": "66 000 ₽",
            "prokshino": "66 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hero-clinic.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        },
        {
          "id": "svc_implantation_092",
          "name": "Установка формирователя десны",
          "officialName": "Внутрикостная дентальная имплантация. (Установка Формирователя десны Osstem/Dentium )",
          "shortDesc": "Создание естественного и гармоничного десневого контура перед изготовлением и установкой постоянной коронки.",
          "tag": "Пластика десны",
          "prices": {
            "ispanskie": "4 400 ₽",
            "prokshino": "4 400 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hero-clinic.webp",
            "prokshino": "../design/assets/prokshino/treatment.webp"
          }
        }
      ]
    },
    {
      "id": "orthodontics",
      "name": "Ортодонтия и прикус",
      "icon": "✨",
      "badge": "Эстетика улыбки",
      "sub": "Исправление положения зубов и гармонизация профиля",
      "procedures": [
        {
          "id": "svc_orthodontics_211",
          "name": "Фиксация брекет-системы металл (лигатурная, 1 челюсть)",
          "officialName": "фиксация брекет системы металл (1 челюсть) лигатурная",
          "shortDesc": "Классическая проверенная брекет-система для точной коррекции нарушений прикуса любой сложности у подростков и взрослых.",
          "tag": "Брекеты металл",
          "prices": {
            "ispanskie": "75 000 ₽",
            "prokshino": "75 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/orthodontics.jpg",
            "prokshino": "../design/assets/prokshino/orthodontics.webp"
          }
        },
        {
          "id": "svc_orthodontics_212",
          "name": "Фиксация брекет-системы металл (самолигирующая, 1 челюсть)",
          "officialName": "фиксация брекет системы металл (1 челюсть) самолигирующая",
          "shortDesc": "Низкотрениевые замочки с мягкими биологическими силами. Комфортное перемещение зубов и более редкие визиты к врачу.",
          "tag": "Брекеты Damon",
          "prices": {
            "ispanskie": "75 000 ₽",
            "prokshino": "75 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/orthodontics.jpg",
            "prokshino": "../design/assets/prokshino/orthodontics.webp"
          }
        },
        {
          "id": "svc_consultations_002",
          "name": "Первичный прием врача-ортодонта с консультацией",
          "officialName": "Прием (осмотр, консультация) врача-ортодонта первичный",
          "shortDesc": "Клинический осмотр, фотопротокол лица и зубных рядов, анализ прикуса и составление подробного плана коррекции.",
          "tag": "Диагностика прикуса",
          "prices": {
            "ispanskie": "880 ₽",
            "prokshino": "880 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/orthodontics.jpg",
            "prokshino": "../design/assets/prokshino/orthodontics.webp"
          }
        }
      ]
    },
    {
      "id": "prosthetics",
      "name": "Протезирование",
      "icon": "👑",
      "badge": "Ортопедия",
      "sub": "Эстетические коронки, виниры и вкладки высшего класса",
      "procedures": [
        {
          "id": "svc_prosthetics_127",
          "name": "Восстановление зуба металлокерамической коронкой",
          "officialName": "Восстановление зуба коронкой. (Металлокерамическая коронка)",
          "shortDesc": "Классическая ортопедическая конструкция для восстановления жевательной функции и целостности зубного ряда.",
          "tag": "Металлокерамика",
          "prices": {
            "ispanskie": "14 300 ₽",
            "prokshino": "14 300 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-3.jpg",
            "prokshino": "../design/assets/prokshino/hero-clinic.webp"
          }
        },
        {
          "id": "svc_prosthetics_122",
          "name": "Коронка с использованием циркониевой вкладки",
          "officialName": "Восстановление зуба коронкой с использованием циркониевой вкладки (без учета стоимости коронки). Циркониевая внутрикорневая вкладка штифт",
          "shortDesc": "Высокоэстетичная безметалловая реставрация из биосовместимого диоксида циркония с естественной полупрозрачностью эмали.",
          "tag": "Цирконий прецизионный",
          "prices": {
            "ispanskie": "11 000 ₽",
            "prokshino": "11 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-3.jpg",
            "prokshino": "../design/assets/prokshino/hero-clinic.webp"
          }
        },
        {
          "id": "svc_prosthetics_117",
          "name": "Временная защитная коронка прямым методом",
          "officialName": "Восстановление зуба коронкой ( временная коронка прямым методом -1 единица)",
          "shortDesc": "Защита обточенного зуба от температурных факторов и сохранение эстетики на период изготовления постоянной конструкции.",
          "tag": "Временная защита",
          "prices": {
            "ispanskie": "3 850 ₽",
            "prokshino": "3 850 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/gallery-3.jpg",
            "prokshino": "../design/assets/prokshino/hero-clinic.webp"
          }
        }
      ]
    },
    {
      "id": "hygiene",
      "name": "Профгигиена и уход",
      "icon": "🌿",
      "badge": "Профилактика",
      "sub": "Бережное спа-очищение зубов и укрепление эмали",
      "procedures": [
        {
          "id": "svc_hygiene_012",
          "name": "Профессиональная комплексная гигиена полости рта",
          "officialName": "Профессиональная гигиена полости рта и зубов",
          "shortDesc": "Снятие плотного пигментированного налета мелкодисперсным AirFlow, ультразвуковое удаление камня и полировка пастами.",
          "tag": "Комплекс AirFlow",
          "prices": {
            "ispanskie": "6 000 ₽",
            "prokshino": "6 000 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hygiene.webp",
            "prokshino": "../design/assets/prokshino/hygiene.webp"
          }
        },
        {
          "id": "svc_hygiene_014",
          "name": "Удаление зубных отложений ультразвуком (1 зуб)",
          "officialName": "Удаление наддесневых и поддесневых зубных отложений в области зуба ручным методом (1 зуб)",
          "shortDesc": "Деликатное снятие наддесневых и поддесневых минерализованных отложений без микроповреждения здоровой эмали.",
          "tag": "Ультразвук",
          "prices": {
            "ispanskie": "440 ₽",
            "prokshino": "440 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hygiene.webp",
            "prokshino": "../design/assets/prokshino/hygiene.webp"
          }
        },
        {
          "id": "svc_hygiene_013",
          "name": "Реминерализирующая терапия эмали",
          "officialName": "Профессиональная гигиена полости рта и зубов. ( в области одного зуба)",
          "shortDesc": "Глубокое насыщение эмали минеральными соединениями кальция и фосфора для снятия повышенной чувствительности.",
          "tag": "Реминерализация",
          "prices": {
            "ispanskie": "275 ₽",
            "prokshino": "275 ₽"
          },
          "images": {
            "ispanskie": "../design/assets/ispanskie/hygiene.webp",
            "prokshino": "../design/assets/prokshino/hygiene.webp"
          }
        }
      ]
    }
  ]
};
