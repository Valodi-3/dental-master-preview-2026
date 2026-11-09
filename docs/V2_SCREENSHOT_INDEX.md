# Dental Master V2 — screenshot index

Все скриншоты сделаны локальным Chromium/Playwright. Текущий V5-прогон обновил 47 кадров; полный набор QA-свидетельств теперь содержит 74 PNG. Полные desktop-страницы 1440 px выделены отдельным разделом внизу.

## Root-регрессии — 9 снимков

**Прокшино, 1024 px.** Tech-baseline на коммите `72ad9a3` имеет 36 px горизонтального overflow; дизайн-ветка до текущего modal/search-патча уже имела 0 px, а после него сохраняет 0 px. CSS исправленной responsive-композиции сохранён.

- [Tech-baseline Прокшино, 1024 px](../design/v2qa/screenshots/tech-baseline-prokshino-1024.png)
- [Дизайн-ветка до добавления modal/search, 1024 px](../design/v2qa/screenshots/regression-before-prokshino-1024.png)
- [Текущая дизайн-ветка после изменений, 1024 px](../design/v2qa/screenshots/regression-after-prokshino-1024.png)

**Испанские кварталы, врачи, мобильный экран.** Tech-отчёт отметил внешние изображения как незагруженные. Их реальный HTTP-ответ в ходе повторной проверки был 200; дизайн использует официальные локальные файлы, все 5/5 проходят naturalWidth-проверку.

- [Tech-baseline со внешними источниками](../design/v2qa/screenshots/tech-baseline-ispanskie-doctors-390.png)
- [Дизайн-ветка до текущей правки](../design/v2qa/screenshots/regression-before-ispanskie-doctors-390.png)
- [Текущая дизайн-ветка, локальные портреты](../design/v2qa/screenshots/regression-after-ispanskie-doctors-390.png)

**Новые действия на главных страницах.**

- [Диалог записи Прокшино, 390 px](../design/v2qa/screenshots/regression-after-booking-prokshino-390.png)
- [Диалог Испанских кварталов с пометкой «Прокшино», 390 px](../design/v2qa/screenshots/regression-after-booking-ispanskie-390.png)
- [Быстрый поиск, точные позиции «Лечение кариеса», 390 px](../design/v2qa/screenshots/regression-after-quick-search-prokshino-390.png)

## До/после V1 и V2 — 4 пары

- [Прокшино — мобильная пара](../design/v2qa/screenshots/v2-before-after-mobile-prokshino.png)
- [Прокшино — desktop-пара](../design/v2qa/screenshots/v2-before-after-desktop-prokshino.png)
- [Испанские кварталы — мобильная пара](../design/v2qa/screenshots/v2-before-after-mobile-ispanskie.png)
- [Испанские кварталы — desktop-пара](../design/v2qa/screenshots/v2-before-after-desktop-ispanskie.png)

## V2 — chooser, главные страницы и селектор направлений

- [Chooser, desktop 1440 px](../design/v2qa/screenshots/v2-desktop-chooser-1440.png)
- [Chooser, mobile 390 px](../design/v2qa/screenshots/v2-mobile-chooser-390.png)
- [Прокшино, главная desktop 1440 px](../design/v2qa/screenshots/v2-desktop-home-prokshino-1440.png)
- [Прокшино, главная mobile 390 px](../design/v2qa/screenshots/v2-mobile-home-prokshino-390.png)
- [Прокшино, главная full-page mobile](../design/v2qa/screenshots/v2-full-home-prokshino-390.png)
- [Испанские кварталы, главная desktop 1440 px](../design/v2qa/screenshots/v2-desktop-home-ispanskie-1440.png)
- [Испанские кварталы, главная mobile 390 px](../design/v2qa/screenshots/v2-mobile-home-ispanskie-390.png)
- [Испанские кварталы, главная full-page mobile](../design/v2qa/screenshots/v2-full-home-ispanskie-390.png)
- [Прокшино, выбор направлений desktop](../design/v2qa/screenshots/v2-desktop-directions-prokshino-1440.png)
- [Прокшино, выбор направлений mobile](../design/v2qa/screenshots/v2-mobile-directions-prokshino-390.png)
- [Испанские кварталы, выбор направлений desktop](../design/v2qa/screenshots/v2-desktop-directions-ispanskie-1440.png)
- [Испанские кварталы, выбор направлений mobile](../design/v2qa/screenshots/v2-mobile-directions-ispanskie-390.png)

## V2 — услуги, специалисты, каталоги и контакты

- [Услуга Прокшино, desktop](../design/v2qa/screenshots/v2-desktop-service-prokshino-1440.png)
- [Услуга Прокшино, mobile](../design/v2qa/screenshots/v2-mobile-service-prokshino-390.png)
- [Услуга Испанских кварталов, desktop](../design/v2qa/screenshots/v2-desktop-service-ispanskie-1440.png)
- [Услуга Испанских кварталов, mobile](../design/v2qa/screenshots/v2-mobile-service-ispanskie-390.png)
- [Врачи Прокшино, desktop](../design/v2qa/screenshots/v2-desktop-doctors-prokshino-1440.png)
- [Врачи Прокшино, mobile](../design/v2qa/screenshots/v2-mobile-doctors-prokshino-390.png)
- [Врачи Испанских кварталов, desktop](../design/v2qa/screenshots/v2-desktop-doctors-ispanskie-1440.png)
- [Врачи Испанских кварталов, mobile](../design/v2qa/screenshots/v2-mobile-doctors-ispanskie-390.png)
- [Профиль врача Прокшино, desktop](../design/v2qa/screenshots/v2-desktop-doctor-prokshino-1440.png)
- [Профиль врача Прокшино, mobile](../design/v2qa/screenshots/v2-mobile-doctor-prokshino-390.png)
- [Профиль врача Испанских кварталов, desktop](../design/v2qa/screenshots/v2-desktop-doctor-ispanskie-1440.png)
- [Профиль врача Испанских кварталов, mobile](../design/v2qa/screenshots/v2-mobile-doctor-ispanskie-390.png)
- [Каталог Прокшино, desktop](../design/v2qa/screenshots/v2-desktop-prices-prokshino-1440.png)
- [Каталог Прокшино, mobile](../design/v2qa/screenshots/v2-mobile-prices-prokshino-390.png)
- [Каталог Испанских кварталов, desktop](../design/v2qa/screenshots/v2-desktop-prices-ispanskie-1440.png)
- [Каталог Испанских кварталов, mobile](../design/v2qa/screenshots/v2-mobile-prices-ispanskie-390.png)
- [Контакты Прокшино, desktop](../design/v2qa/screenshots/v2-desktop-contacts-prokshino-1440.png)
- [Контакты Прокшино, mobile](../design/v2qa/screenshots/v2-mobile-contacts-prokshino-390.png)
- [Контакты Испанских кварталов, desktop](../design/v2qa/screenshots/v2-desktop-contacts-ispanskie-1440.png)
- [Контакты Испанских кварталов, mobile](../design/v2qa/screenshots/v2-mobile-contacts-ispanskie-390.png)

## V2 — запись и специальное состояние селектора

- [Диалог записи, desktop 1440 px](../design/v2qa/screenshots/v2-booking-modal-desktop-1440.png)
- [Диалог записи Прокшино, mobile 390 px](../design/v2qa/screenshots/v2-booking-modal-mobile-390.png)
- [Диалог записи Испанских кварталов, mobile 390 px](../design/v2qa/screenshots/v2-booking-modal-ispanskie-mobile-390.png)
- [Шаг подтверждения звонка, mobile 390 px](../design/v2qa/screenshots/v2-booking-call-step-mobile-390.png)
- [Выбранный вариант услуги ортодонтии](../design/v2qa/screenshots/v2-selected-orthodontic-variant.png)


## Визуальная отделка после обратной связи

Снимки «до» — сохранённый V2 вариант до последней проходки; «после» — итоговые Chromium-captures из финального девятиширинного прогона.

| Филиал | До · mobile 390 px | После · mobile 390 px |
|---|---|---|
| Прокшино | [PNG до](../design/v2qa/screenshots/polish-before-prokshino-mobile-390.png) | [PNG после](../design/v2qa/screenshots/v2-mobile-home-prokshino-390.png) |
| Испанские кварталы | [PNG до](../design/v2qa/screenshots/polish-before-ispanskie-mobile-390.png) | [PNG после](../design/v2qa/screenshots/v2-mobile-home-ispanskie-390.png) |

**Desktop 1440 px:**

- Прокшино: [до](../design/v2qa/screenshots/polish-before-prokshino-desktop-1440.png) · [после](../design/v2qa/screenshots/v2-desktop-home-prokshino-1440.png)
- Испанские кварталы: [до](../design/v2qa/screenshots/polish-before-ispanskie-desktop-1440.png) · [после](../design/v2qa/screenshots/v2-desktop-home-ispanskie-1440.png)

**Вся мобильная страница, 390 px:** [Прокшино до](../design/v2qa/screenshots/polish-before-prokshino-full-mobile-390.png) · [Прокшино после](../design/v2qa/screenshots/v2-full-home-prokshino-390.png) · [Испанские кварталы до](../design/v2qa/screenshots/polish-before-ispanskie-full-mobile-390.png) · [Испанские кварталы после](../design/v2qa/screenshots/v2-full-home-ispanskie-390.png).

**Цена в селекторе:** [финальный экран направления на 390 px](../design/v2qa/screenshots/v2-mobile-directions-prokshino-390.png); [автоматический отчёт — 168 цен без разрывов](../design/v2qa/polish-currency-results.json).


## Итерация 3 — предыдущая editorial-подача и три способа связи

- [Мобильная панель выбора записи · Прокшино · 390×844](../design/v2qa/screenshots/premium-booking-choice-prokshino-390.png)
- [Мобильная панель выбора записи · Испанские кварталы · 390×844](../design/v2qa/screenshots/premium-booking-choice-ispanskie-390.png)
- [Главная Прокшино в тёмно-изумрудной editorial-подаче · mobile](../design/v2qa/screenshots/v2-mobile-home-prokshino-390.png) · [desktop](../design/v2qa/screenshots/v2-desktop-home-prokshino-1440.png)
- [Главная Испанских кварталов в отдельной тёплой композиции · mobile](../design/v2qa/screenshots/v2-mobile-home-ispanskie-390.png) · [desktop](../design/v2qa/screenshots/v2-desktop-home-ispanskie-1440.png)

Объёмный hover — только лёгкий CSS `perspective`/`rotateY` над проверенными фото клиник. Внешние 3D- и анимационные библиотеки, сгенерированные фотографии и автозапуск связи не добавлялись. По «Записаться» сначала открывается эта панель: DentalPRO, предварительный телефонный шаг или самостоятельный переход в WhatsApp/Telegram.


## Историческая итерация 4 — версия после оценки 3/10, до новых требований 5/10

Это архивное V4-сравнение: «до» — экраны до ответа на оценку 3/10, «после» — V4 до следующей оценки 5/10. Текущий вариант и его доказательства находятся в секции V5 ниже.

| Филиал | До · mobile 390 px | После · mobile 390 px | До · desktop 1440 px | После · desktop 1440 px |
|---|---|---|---|---|
| Прокшино | [До · 3/10](../design/v2qa/screenshots/v4-before-prokshino-mobile-390.png) | [V4 · до 5/10](../design/v2qa/screenshots/v5-before-v4-prokshino-mobile-390.png) | [До](../design/v2qa/screenshots/v4-before-prokshino-desktop-1440.png) | [V4 · до 5/10](../design/v2qa/screenshots/v5-before-v4-prokshino-desktop-1440.png) |
| Испанские кварталы | [До · 3/10](../design/v2qa/screenshots/v4-before-ispanskie-mobile-390.png) | [V4 · до 5/10](../design/v2qa/screenshots/v5-before-v4-ispanskie-mobile-390.png) | [До](../design/v2qa/screenshots/v4-before-ispanskie-desktop-1440.png) | [V4 · до 5/10](../design/v2qa/screenshots/v5-before-v4-ispanskie-desktop-1440.png) |

**Полный mobile-page V4, архив:** [Прокшино](../design/v2qa/screenshots/v5-before-v4-prokshino-full-mobile-390.png) · [Испанские кварталы](../design/v2qa/screenshots/v5-before-v4-ispanskie-full-mobile-390.png). **Сначала выбор способа записи:**

## Итерация 5 — welcome-first · полная ПК-версия

Финальная V5-сборка после обратной связи «5/10»: сначала приветственный экран с пространством клиники; запись — отдельно закреплена снизу справа; команда листается и ведёт к профильным сведениям. Старые V4 «до» сохранены отдельно и не подменяют текущие файлы.

**Начальные mobile-экраны · 390 px:** [Прокшино](../design/v2qa/screenshots/v2-mobile-home-prokshino-390.png) · [Испанские кварталы](../design/v2qa/screenshots/v2-mobile-home-ispanskie-390.png).

**Doctor carousel:** [Прокшино · 390 px](../design/v2qa/screenshots/v2-home-doctors-prokshino-390.png) · [Испанские кварталы · 390 px](../design/v2qa/screenshots/v2-home-doctors-ispanskie-390.png) · [Прокшино · 1440 px](../design/v2qa/screenshots/v2-home-doctors-prokshino-1440.png) · [Испанские кварталы · 1440 px](../design/v2qa/screenshots/v2-home-doctors-ispanskie-1440.png).

**V4 перед правкой V5:** mobile — [Прокшино](../design/v2qa/screenshots/v5-before-v4-prokshino-mobile-390.png) · [Испанские кварталы](../design/v2qa/screenshots/v5-before-v4-ispanskie-mobile-390.png); desktop 1440 — [Прокшино](../design/v2qa/screenshots/v5-before-v4-prokshino-desktop-1440.png) · [Испанские кварталы](../design/v2qa/screenshots/v5-before-v4-ispanskie-desktop-1440.png); полный mobile — [Прокшино](../design/v2qa/screenshots/v5-before-v4-prokshino-full-mobile-390.png) · [Испанские кварталы](../design/v2qa/screenshots/v5-before-v4-ispanskie-full-mobile-390.png).

**Полный ПК-сайт, сверху до footer, 1440 × 4699 px:**

- [ДантистЪ Прокшино — полный desktop PNG](../design/v2qa/screenshots/v2-full-home-prokshino-1440.png)
- [ДантистЪ Испанские кварталы — полный desktop PNG](../design/v2qa/screenshots/v2-full-home-ispanskie-1440.png)

**Канал записи до выхода из сайта:** [Прокшино · 390 px](../design/v2qa/screenshots/premium-booking-choice-prokshino-390.png) · [Испанские кварталы · 390 px](../design/v2qa/screenshots/premium-booking-choice-ispanskie-390.png). **Автотесты:** [`V5 homepage`](../design/v2qa/v5-homepage-check.json) · [`41 маршрута × 9 ширин и 200% текста`](../design/v2qa/layout-metrics.json).
