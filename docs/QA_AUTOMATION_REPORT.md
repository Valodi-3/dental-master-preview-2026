# Отчёт автоматизированного тестирования верстки (QA Automation Report)

**Дата проведения тестов:** 9 ноября 2026 г.  
**Тестовый движок:** Playwright Headless Chromium  
**Базовый URL:** \`http://127.0.0.1:8765\` (локальный превью-сервер) / \`https://valodi-3.github.io/dental-master-preview-2026/\`  
**Итоговый результат:** **27 тестов пройдено (PASS)**, **3 замечания выявлено (DEFECTS FOUND)** из 30 проверок.

---

## 1. Матрица проверки горизонтального переполнения (Overflow Matrix)

| Разрешение | Устройство / Профиль | ДантистЪ Прокшино (\`prokshino.html\`) | ДантистЪ Испанские кварталы (\`ispanskie.html\`) |
|:---:|---|:---:|:---:|
| **320 px** | iPhone SE (1-е поколение, самый узкий экран) | **PASS** (0 px) | **PASS** (0 px) |
| **360 px** | Android Compact (Galaxy A-series) | **PASS** (0 px) | **PASS** (0 px) |
| **375 px** | iPhone SE / iPhone 8 | **PASS** (0 px) | **PASS** (0 px) |
| **390 px** | iPhone 12 / 13 / 14 (базовый стандарт iOS) | **PASS** (0 px) | **PASS** (0 px) |
| **430 px** | iPhone 14 / 15 Pro Max | **PASS** (0 px) | **PASS** (0 px) |
| **768 px** | iPad Portrait (планшетная ориентация) | **PASS** (0 px) | **PASS** (0 px) |
| **1024 px**| iPad Landscape / ноутбуки малого формата | **FAIL (+36 px переполнение)** | **PASS** (0 px) |
| **1440 px**| Desktop Standard | **PASS** (0 px) | **PASS** (0 px) |
| **1920 px**| Desktop Full HD | **PASS** (0 px) | **PASS** (0 px) |

---

## 2. Детальный разбор выявленных дефектов для передачи Manus

### Дефект №1: Горизонтальный скролл на 1024 px в Прокшино
* **Файл:** \`prokshino.html\` / \`prokshino.css\`
* **Ширина экрана:** \`1024 px\`
* **Величина вылета:** \`1060 px\` (переполнение на **+36 px**)
* **Координаты и виновные элементы:**
  1. \`.header-actions\` (\`tag: div\`, правая граница \`1060 px\`, ширина \`299 px\`, вылет \`+36 px\`).  
     *Причина:* на брейкпоинте \`1024 px\` в шапке одновременно рендерятся и текстовые пункты навигации, и номер телефона с широкой кнопкой \`.btn-primary.btn-glow\`, что выталкивает блок за пределы контейнера.  
     *Рекомендация для Manus:* в \`prokshino.css\` для \`@media (max-width: 1100px)\` скрыть блок телефона или перевести навигацию в компактный вид (либо уменьшить \`gap\` между ссылками с 28px до 16px).
  2. \`.hero-ambient-glow\` (правая граница \`1144 px\`, вылет \`+120 px\`).  
     *Причина:* декоративное свечение позиционируется с \`right: -100px\` без \`overflow: hidden\` на родительской секции \`.hero-section\`.  
     *Рекомендация для Manus:* добавить \`overflow: hidden;\` в правило \`.hero-section\` в \`prokshino.css\`.

---

### Дефект №2: Ошибки 404 по 2 портретам врачей в Испанских кварталах
* **Файл:** \`ispanskie.html\`
* **Селектор:** \`.doctor-card-horizontal img\`
* **Проблемные URL:**
  1. \`https://stomatolog-ispanskie-kvartaly.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/anna-karapetyan-960.jpg\` (HTTP 404)
  2. \`https://stomatolog-ispanskie-kvartaly.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-01.webp\` (HTTP 404)
* **Причина:** На боевом сервере \`stomatolog-ispanskie-kvartaly.ru\` данные изображения отсутствуют в теме, но они физически размещены и отдаются с HTTP 200 на головном домене сети:
  * Рабочий URL 1: \`https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/anna-karapetyan-960.jpg\` (**200 OK**)
  * Рабочий URL 2: \`https://dantist-prokshino.ru/wp-content/themes/your-clean-template-3/studio-staff/portraits/portrait-01.webp\` (**200 OK**)
* *Рекомендация для Manus:* в карточках врачей Карапетян А.А. и Машрабовой А.М. заменить домен в \`src\` на \`dantist-prokshino.ru\` либо использовать локальные ассеты.

---

### Дефект №3: Селектор триггера модального окна в Прокшино
* **Файл:** \`prokshino.html\`
* **Суть:** В \`ispanskie.html\` кнопки записи снабжены атрибутом \`data-booking-trigger\`, благодаря чему модальное окно открывается надежно из любой точки страницы. В \`prokshino.html\` в некоторых кнопках используется устаревший класс \`.btn.book\` без \`data-booking-trigger\`.
* *Рекомендация для Manus:* добавить \`data-booking-trigger\` на главную кнопку записи первого экрана и в шапке Прокшино.

---

## 3. Функциональные тесты, завершившиеся успехом (PASS)

1. **Отсутствие localhost / 127.0.0.1 в опубликованном DOM:**
   * Прокшино: **PASS** (0 совпадений).
   * Испанские кварталы: **PASS** (0 совпадений).
   * Все ссылки между клиниками строго относительные (\`prokshino.html\` <-> \`ispanskie.html\`).

2. **Мобильное меню (Drawer Navigation):**
   * Прокшино: **PASS** (меню корректно открывается по гамбургеру, блокирует фоновый скролл, закрывается по клику на пункт).
   * Испанские кварталы: **PASS** (меню открывается, содержит относительную ссылку на второй филиал).

3. **Модальное окно записи и доступность по Escape:**
   * Испанские кварталы: **PASS** (открывается по клику, закрывается по клавише Escape, закрывается по клику на оверлей и крестик).

4. **Zero Fake Forms (Честность записи):**
   * Прокшино: **PASS** (отсутствуют симуляции с фальшивым \`setTimeout\`).
   * Испанские кварталы: **PASS** (представлены 3 реальных канала: DentalPRO, WhatsApp, Телефон).

---

## 4. Инструкция для Manus по запуску тестов

Manus может запускать данный автотест в любой момент после внесения изменений в верстку одной командой:

\`\`\`bash
node tests/run-qa-suite.cjs
\`\`\`

При тестировании опубликованного GitHub Pages достаточно передать переменную:
\`\`\`bash
TEST_URL=https://valodi-3.github.io/dental-master-preview-2026 node tests/run-qa-suite.cjs
\`\`\`
Отчёт со всеми координатами элементов сохраняется в \`tests/qa-report.json\`.
