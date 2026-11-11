/**
 * DENTAL ATLAS — REAL DATA STORE (SSOT)
 * Single source of truth compiled from:
 * - v2/data/services_master.json
 * - v2/data/doctors.json
 * - v2/data/clinic-content.json
 * - docs/BOOKING_LINK_AUDIT.md
 * Zero invented facts. Zero unverified durations.
 */

window.ATLAS_DATA = {
  branches: {
    ispanskie: {
      key: 'ispanskie',
      isPrimary: true,
      name: 'Испанские кварталы',
      badge: 'Основной филиал сети',
      shortName: 'Испанские кв.',
      address: 'Москва, Коммунарка, улица Магеллана, 5',
      metro: 'м. Прокшино / Ольховая',
      phone: '+7 (904) 519-96-97',
      phoneClean: '+79045199697',
      hours: 'Ежедневно 09:00–21:00',
      heroImage: '../design/assets/ispanskie/gallery-5.jpg',
      heroAlt: 'Стоматологический кабинет филиала «Испанские кварталы»'
    },
    prokshino: {
      key: 'prokshino',
      isPrimary: false,
      name: 'Прокшино',
      badge: 'Второй филиал сети',
      shortName: 'Прокшино',
      address: 'Москва, Коммунарка, проспект Магеллана, 5 (Лобановский Лес, 11)',
      metro: 'м. Прокшино',
      phone: '+7 (904) 519-96-97',
      phoneClean: '+79045199697',
      hours: 'Ежедневно 09:00–21:00',
      heroImage: '../design/assets/prokshino/hero-clinic.webp',
      heroAlt: 'Консультационный кабинет филиала «Прокшино»'
    }
  },

  booking: {
    phone: '+7 (904) 519-96-97',
    phoneTel: 'tel:+79045199697',
    whatsapp: 'https://wa.me/message/2WBFWCZJGHQDG1',
    telegram: 'https://t.me/Stomatologiya1108',
    dentalpro: 'https://dantist-prokshino.ru/online-zapis/',
    dentalproNotice: 'Централизованный сервис онлайн-записи сети клиник «ДантистЪ»'
  },

  categories: [
    {
      id: 'diagnostics',
      name: 'Диагностика',
      fullName: 'Диагностика и первичный приём',
      icon: '◎',
      lead: 'Точная оценка состояния зубов и костной ткани перед началом любого вмешательства.'
    },
    {
      id: 'treatment',
      name: 'Лечение зубов',
      fullName: 'Терапия и эндодонтия под микроскопом',
      icon: '◈',
      lead: 'Лечение кариеса, пульпита и периодонтита с сохранением максимального объёма здоровых тканей.'
    },
    {
      id: 'implants',
      name: 'Имплантация',
      fullName: 'Дентальная имплантация и костная пластика',
      icon: '❖',
      lead: 'Восстановление утраченных зубов на сертифицированных системах Osstem и Straumann.'
    },
    {
      id: 'prosthetics',
      name: 'Протезирование',
      fullName: 'Ортопедическая стоматология и виниры',
      icon: '▣',
      lead: 'Керамические коронки E-max, циркониевые конструкции и эстетические виниры.'
    },
    {
      id: 'orthodontics',
      name: 'Ортодонтия',
      fullName: 'Исправление прикуса и брекет-системы',
      icon: '◐',
      lead: 'Ортодонтическое лечение на элайнерах, металлических и сапфировых брекетах.'
    },
    {
      id: 'hygiene',
      name: 'Профгигиена',
      fullName: 'Профессиональная гигиена и профилактика',
      icon: '○',
      lead: 'Аппаратная чистка Air-Flow, удаление зубного камня ультразвуком и реминерализация.'
    }
  ],

  procedures: [
    // Diagnostics
    {
      id: 'consult-head',
      catId: 'diagnostics',
      name: 'Консультация главного врача с составлением плана',
      tag: 'Консультация',
      desc: 'Комплексный осмотр полости рта, анализ КТ/ОПТГ, определение этапности и стоимости лечения.',
      prices: { ispanskie: '2 500 ₽', prokshino: '2 500 ₽' },
      doctorSlugs: ['danielyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-2.jpg',
        prokshino: '../design/assets/prokshino/hero-clinic.webp'
      }
    },
    {
      id: 'ct-scan',
      catId: 'diagnostics',
      name: 'Компьютерная 3D-томография (КЛКТ)',
      tag: 'Аппаратная диагностика',
      desc: 'Высокоточное трёхмерное сканирование зубочелюстной системы для безопасной имплантации и эндодонтии.',
      prices: { ispanskie: '3 500 ₽', prokshino: '3 500 ₽' },
      doctorSlugs: ['danielyan', 'nadzhafov'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-1.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },
    {
      id: 'aim-xray',
      catId: 'diagnostics',
      name: 'Прицельный радиовизиографический снимок',
      tag: 'Снимок',
      desc: 'Локальная рентген-диагностика одного зуба в кресле во время приёма с минимальной лучевой нагрузкой.',
      prices: { ispanskie: '500 ₽', prokshino: '500 ₽' },
      doctorSlugs: ['karapetyan', 'mashrabova'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-5.jpg',
        prokshino: '../design/assets/prokshino/microscope.webp'
      }
    },

    // Treatment
    {
      id: 'caries-composite',
      catId: 'treatment',
      name: 'Лечение кариеса с анатомической реставрацией',
      tag: 'Терапия',
      desc: 'Бережное удаление поражённых тканей, изоляция коффердамом и восстановление анатомической формы жевательной поверхности.',
      prices: { ispanskie: '6 500 ₽', prokshino: '6 500 ₽' },
      doctorSlugs: ['karapetyan', 'mashrabova'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-6.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },
    {
      id: 'endo-microscope',
      catId: 'treatment',
      name: 'Эндодонтическое лечение каналов под микроскопом Zeiss',
      tag: 'Эндодонтия',
      desc: 'Обработка и трёхмерная обтурация сложных корневых каналов под многократным оптическим увеличением Carl Zeiss.',
      prices: { ispanskie: '14 000 ₽', prokshino: '14 000 ₽' },
      doctorSlugs: ['karapetyan', 'danielyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-5.jpg',
        prokshino: '../design/assets/prokshino/microscope.webp'
      }
    },
    {
      id: 'aesthetic-restoration',
      catId: 'treatment',
      name: 'Художественная реставрация зоны улыбки',
      tag: 'Эстетика',
      desc: 'Послойное воссоздание микрорельефа, прозрачности режущего края и оттенка фронтальных зубов композитами премиум-класса.',
      prices: { ispanskie: '9 500 ₽', prokshino: '9 500 ₽' },
      doctorSlugs: ['karapetyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-7.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },

    // Implants
    {
      id: 'osstem-implant',
      catId: 'implants',
      name: 'Установка дентального имплантата Osstem (Южная Корея)',
      tag: 'Имплантация',
      desc: 'Популярная надёжная система с гидрофильной поверхностью SA, обеспечивающая быстрое приживление в костной ткани.',
      prices: { ispanskie: '36 000 ₽', prokshino: '36 000 ₽' },
      doctorSlugs: ['danielyan', 'nadzhafov'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-5.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },
    {
      id: 'straumann-implant',
      catId: 'implants',
      name: 'Установка дентального имплантата Straumann (Швейцария)',
      tag: 'Премиум-класс',
      desc: 'Швейцарский эталон биосовместимости с поверхностью SLActive, сокращающий срок остеоинтеграции до 3–4 недель.',
      prices: { ispanskie: '66 000 ₽', prokshino: '66 000 ₽' },
      doctorSlugs: ['danielyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-2.jpg',
        prokshino: '../design/assets/prokshino/hero-clinic.webp'
      }
    },
    {
      id: 'immediate-implant',
      catId: 'implants',
      name: 'Одномоментная имплантация сразу после удаления',
      tag: 'Хирургия',
      desc: 'Установка имплантата в лунку только что удалённого зуба за один хирургический приём с установкой формирователя десны.',
      prices: { ispanskie: '45 000 ₽', prokshino: '45 000 ₽' },
      doctorSlugs: ['danielyan', 'nadzhafov'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-1.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },

    // Prosthetics
    {
      id: 'crown-emax',
      catId: 'prosthetics',
      name: 'Керамическая коронка IPS E-max (Германия)',
      tag: 'Ортопедия',
      desc: 'Безметалловая пресс-керамика с естественной опалесценцией и прочностью, идеальна для зоны улыбки и премоляров.',
      prices: { ispanskie: '28 000 ₽', prokshino: '28 000 ₽' },
      doctorSlugs: ['danielyan', 'nadzhafov'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-7.jpg',
        prokshino: '../design/assets/prokshino/hero-clinic.webp'
      }
    },
    {
      id: 'crown-zirconia',
      catId: 'prosthetics',
      name: 'Коронка из диоксида циркония на имплантат',
      tag: 'Ортопедия',
      desc: 'Сверхпрочная биоинертная конструкция с индивидуальным титановым или циркониевым абатментом для жевательного отдела.',
      prices: { ispanskie: '34 000 ₽', prokshino: '34 000 ₽' },
      doctorSlugs: ['danielyan', 'nadzhafov'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-6.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    },
    {
      id: 'ceramic-veneer',
      catId: 'prosthetics',
      name: 'Керамический винир E-max с индивидуальной подкраской',
      tag: 'Эстетика',
      desc: 'Тончайшая микропротезная накладка с минимальным препарированием эмали для изменения формы, длины и цвета фронтального зуба.',
      prices: { ispanskie: '32 000 ₽', prokshino: '32 000 ₽' },
      doctorSlugs: ['danielyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-2.jpg',
        prokshino: '../design/assets/prokshino/hero-clinic.webp'
      }
    },

    // Orthodontics
    {
      id: 'ortho-consult',
      catId: 'orthodontics',
      name: 'Консультация ортодонта с фотометрией и расчётом TRG',
      tag: 'Ортодонтия',
      desc: 'Полная ортодонтическая диагностика, анализ окклюзии, расчёт телерентгенограммы и подбор аппаратуры.',
      prices: { ispanskie: '3 000 ₽', prokshino: '3 000 ₽' },
      doctorSlugs: ['fiasheva'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-2.jpg',
        prokshino: '../design/assets/prokshino/orthodontics.webp'
      }
    },
    {
      id: 'aligners-course',
      catId: 'orthodontics',
      name: 'Ортодонтическое лечение на прозрачных элайнерах',
      tag: 'Элайнеры',
      desc: 'Незаметное исправление зубных рядов с помощью серии индивидуальных съёмных прозрачных капп.',
      prices: { ispanskie: 'от 180 000 ₽', prokshino: 'от 180 000 ₽' },
      doctorSlugs: ['fiasheva'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-7.jpg',
        prokshino: '../design/assets/prokshino/orthodontics.webp'
      }
    },
    {
      id: 'brackets-ceramic',
      catId: 'orthodontics',
      name: 'Керамическая брекет-система (1 челюсть)',
      tag: 'Брекеты',
      desc: 'Эстетичные полупрозрачные замочки под тон собственной эмали для надёжного корпусного перемещения зубов.',
      prices: { ispanskie: '55 000 ₽', prokshino: '55 000 ₽' },
      doctorSlugs: ['fiasheva'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-6.jpg',
        prokshino: '../design/assets/prokshino/orthodontics.webp'
      }
    },

    // Hygiene
    {
      id: 'complex-hygiene',
      catId: 'hygiene',
      name: 'Комплексная профессиональная гигиена полости рта',
      tag: 'Профилактика',
      desc: 'Трёхэтапная чистка: ультразвуковое снятие камня, мягкая воздушно-абразивная полировка Air-Flow и реминерализующая терапия.',
      prices: { ispanskie: '7 000 ₽', prokshino: '7 000 ₽' },
      doctorSlugs: ['karapetyan', 'mashrabova'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-1.jpg',
        prokshino: '../design/assets/prokshino/hygiene.webp'
      }
    },
    {
      id: 'air-flow-cleaning',
      catId: 'hygiene',
      name: 'Снятие пигментированного налёта Air-Flow',
      tag: 'Air-Flow',
      desc: 'Бережное удаление налёта от чая, кофе и табака сферическим порошком глицина без повреждения эмали.',
      prices: { ispanskie: '4 500 ₽', prokshino: '4 500 ₽' },
      doctorSlugs: ['mashrabova'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-5.jpg',
        prokshino: '../design/assets/prokshino/hygiene.webp'
      }
    },
    {
      id: 'enamel-remineralization',
      catId: 'hygiene',
      name: 'Глубокое фторирование и реминерализация эмали',
      tag: 'Укрепление',
      desc: 'Аппликация кальций-фосфатных и фторсодержащих лаков для снижения гиперчувствительности и укрепления твёрдых тканей.',
      prices: { ispanskie: '2 500 ₽', prokshino: '2 500 ₽' },
      doctorSlugs: ['mashrabova', 'karapetyan'],
      images: {
        ispanskie: '../design/assets/ispanskie/gallery-7.jpg',
        prokshino: '../design/assets/prokshino/treatment.webp'
      }
    }
  ],

  doctors: [
    {
      slug: 'danielyan',
      name: 'Даниелян Арам Яковлевич',
      shortName: 'Арам Даниелян',
      role: 'Стоматолог-хирург, имплантолог, ортопед, терапевт',
      experience: '25 лет',
      portrait: '../design/assets/doctors/danielyan.jpg',
      practice: 'Сложная дентальная имплантация на системах Osstem и Straumann, костная пластика, синус-лифтинг и ортопедическая реабилитация.',
      education: 'Высшее медицинское образование. Сведения о дополнительном обучении по имплантации, хирургическим и ортопедическим протоколам, препарированию под виниры и эндодонтии под микроскопом.',
      certificates: [
        'Osstem: базовый хирургический курс (2018)',
        'Имплантация: хирургические и ортопедические протоколы (2018)',
        'Препарирование под виниры (2021)',
        'Лечение корневых каналов под микроскопом'
      ],
      branches: ['ispanskie', 'prokshino']
    },
    {
      slug: 'nadzhafov',
      name: 'Наджафов Азер Этибарович',
      shortName: 'Азер Наджафов',
      role: 'Врач-стоматолог, хирург-имплантолог',
      experience: '10 лет',
      portrait: '../design/assets/doctors/nadzhafov.webp',
      practice: 'Хирургическая, имплантологическая и ортопедическая практика, атравматичное удаление зубов любой сложности, синус-лифтинг.',
      education: 'РНИМУ им. Н. И. Пирогова; специальность «Стоматология», квалификация «врач-стоматолог». Дополнительное обучение: реставрация жевательной группы зубов, синус-лифтинг.',
      certificates: [
        'Реставрация жевательной группы зубов (2022)'
      ],
      branches: ['ispanskie', 'prokshino']
    },
    {
      slug: 'fiasheva',
      name: 'Фиашева Диана Андзоровна',
      shortName: 'Диана Фиашева',
      role: 'Стоматолог-ортодонт',
      experience: '7 лет',
      portrait: '../design/assets/doctors/fiasheva.webp',
      practice: 'Коррекция патологий прикуса у взрослых и детей, ведение пациентов на элайнерах и брекет-системах, подготовка к протезированию.',
      education: 'МГМСУ им. А. И. Евдокимова; специальность «Стоматология», квалификация «врач-стоматолог». Ординатура по специальности «Ортодонтия».',
      certificates: [],
      branches: ['ispanskie', 'prokshino']
    },
    {
      slug: 'karapetyan',
      name: 'Карапетян Анна Арменаковна',
      shortName: 'Анна Карапетян',
      role: 'Стоматолог-терапевт, эндодонтист',
      experience: 'Более 10 лет',
      portrait: '../design/assets/doctors/karapetyan.jpg',
      practice: 'Терапевтическая стоматология, эндодонтическое перелечивание труднопроходимых каналов под микроскопом, эстетическая реставрация.',
      education: 'Дополнительное обучение: художественная реставрация фронтальных зубов, клиническая эндодонтия и эндодонтическое перелечивание.',
      certificates: [
        'Художественная реставрация фронтальных зубов, AVS school (2021)',
        'Ultimate Endo: клиническая эндодонтия, AVS school (2021)',
        'Эндодонтическое перелечивание (2021)'
      ],
      branches: ['ispanskie', 'prokshino']
    },
    {
      slug: 'mashrabova',
      name: 'Машрабова Амина Мубораккадамовна',
      shortName: 'Амина Машрабова',
      role: 'Врач-стоматолог общей практики',
      experience: 'Более 5 лет',
      portrait: '../design/assets/doctors/mashrabova.jpg',
      practice: 'Терапевтический приём, профессиональная гигиена полости рта, подготовка к ортопедическому лечению.',
      education: 'Диплом специалиста по специальности «Стоматология»; ординатура по стоматологии ортопедической.',
      certificates: [],
      branches: ['ispanskie', 'prokshino']
    }
  ]
};
