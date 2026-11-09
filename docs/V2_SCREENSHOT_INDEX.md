# Dental Master V2 — screenshot index

Все скриншоты сделаны локальным Chromium/Playwright; PNG лежат в `design/v2qa/screenshots/`. Полные размеры и browser metrics: [`layout-metrics.json`](../design/v2qa/layout-metrics.json). Регрессионные проверки: [`regression-validation.json`](../design/v2qa/regression-validation.json), [`regression-comparison.json`](../design/v2qa/regression-comparison.json); точный 30/30 результат неизменённого tech-набора: [`tech-root-qa-30-30.json`](../design/v2qa/tech-root-qa-30-30.json).

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
