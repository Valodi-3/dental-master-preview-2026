# V2 — источники и проверенные ограничения

Дата проверки: 9 ноября 2026 года. Ветка дизайна на старте задачи — `design/manus-dental-master-2026`, commit `c21058beb6e146d8f689502f8f565b30452f30e7`.

## Клиники и онлайн-запись

- [ДантистЪ Прокшино](https://dantist-prokshino.ru/) — официальная главная, опубликованные услуги и команда.
- [Прайс Прокшино](https://dantist-prokshino.ru/%D1%86%D0%B5%D0%BD%D1%8B/) — официальный источник названий процедур и цен.
- [DentalPRO](https://dantist-prokshino.ru/online-zapis/) — подтверждённый общий URL онлайн-записи сети.
- [Испанские кварталы](https://stomatolog-ispanskie-kvartaly.ru/) — официальный источник контактов, команды и услуг филиала.
- [Прайс Испанских кварталов](https://stomatolog-ispanskie-kvartaly.ru/prices/) — официальный источник каталога этого филиала.

Официальная страница Испанских кварталов прямо подписывает действующую онлайн-запись как филиал Прокшино. В Antigravity [`BOOKING_LINK_AUDIT.md`](https://github.com/Valodi-3/dental-master-preview-2026/blob/tech/dental-master-foundation-2026/docs/BOOKING_LINK_AUDIT.md) указано, что `/online-zapis/` на домене Испанских кварталов возвращает 404, а официальный сайт направляет онлайн-запись на DentalPRO Прокшино. Поэтому обе ветви V2 используют именно подтверждённый URL DentalPRO, честно указывая, что выбранное направление показано только в интерфейсе preview и не передаётся в CRM.

Официально опубликованный единый номер регистратуры: `+7 (904) 519-96-97`, E.164 ссылка `tel:+79045199697`. Также опубликованы WhatsApp `https://wa.me/message/2WBFWCZJGHQDG1` и Telegram `https://t.me/Stomatologiya1108`; дополнительный мессенджер не должен подменять онлайн-запись.

## Каталог из Antigravity PR #1

PR [#1, `feat(tech): Dental Master Technical Foundation 2026`](https://github.com/Valodi-3/dental-master-preview-2026/pull/1) при проверке оставался открытым; его не объединяли. Данные прочитаны из remote branch `tech/dental-master-foundation-2026`, commit `a1607f79c28aafb7d2ee73818cdd5d996f7f5d3f`.

Источники в этой ветке: `data/services_master.json`, `data/services_prokshino.json`, `data/services_ispanskie.json`, `data/categories_summary.json` и `docs/BOOKING_LINK_AUDIT.md`. В master и в каждом филиальном списке по 254 уникальных SKU; десять категорий имеют количества 6, 2, 3, 11, 25, 19, 24, 18, 66 и 80. Сервисный ID уникален. Два списка филиалов используют одинаковый порядок, ID и названия; число отличающихся цен — 0. При сопоставлении всех 254 строк с каталогами, уже полученными в локальной V1-ветке с официальных сайтов, нормализованные название и сумма каждой позиции совпали, ошибок — 0 для каждого филиала.

Важно: в полях `description` всех 254 записей описание пустое. V2 не сочиняет обещания результата, длительности, материалы, показания или медицинские рекомендации. В карточке показывается точное опубликованное название процедуры, категория и цена; дополнительный текст ограничивается подтверждённым пояснением клиники, что конкретные этапы и индивидуальный план обсуждаются со стоматологом.

## Ориентир REGINA

Референс: [agrrbeauty.com](https://agrrbeauty.com/). Страница загружена через публичную выдачу и осмотрена в подключённом браузере; раскрыта одна позиция прейскуранта, никаких записей или форм не отправляли.

Первоначальная V2-итерация использовала REGINA лишь как функциональную подсказку: отдельные tab-переключатели, категорийные фильтры, раскрываемые строки и видимая цена. Тогда визуальная система референса ещё не была частью задачи. Этот исторический scope superseded последующим прямым запросом владельца сайта.

## Визуальный референс AGRR Beauty — итерация 6

Публичная страница [AGRR Beauty](https://agrrbeauty.com/) повторно загружена и визуально осмотрена в браузере 9 ноября 2026 года по запросу пользователя. На первом desktop-экране видна тёплая поверхность цвета бумаги/песка вместо белого холста, тёмная типографика и крупный выразительный serif-заголовок с курсивным акцентом. Компактная шапка оставляет воздуху больше места; hero соединяет крупный текст и настоящее фото фасада салона. При прокрутке страница переходит в пронумерованные направления услуг, а дальше в самостоятельную визуальную сцену с интерактивным определением длины волос. В нижних частях, увиденных текстовым чтением страницы, есть галереи, прайс, SPA, первый визит и способы связи. Это осмотренный UX/design reference, а не источник стоматологических фактов.

В текущем запросе пользователь явно попросил строить визуальную подачу примерно по AGRR и отказался от посредственного чисто-белого фона. Поэтому выполненная V6-итерация берёт из референса тёплую палитру бумаги и дерева, большие редакционные заголовки, визуальные паузы, крупные фотографии и разнообразный ритм разделов. Она не переносит салонный текст, чужие изображения, названия или услуги. Все стоматологические данные и фотографии остаются локальными и подтверждёнными по данным клиник; лёгкая глубина реализуется CSS без 3D-библиотеки и генерации новых изображений.

## Безопасная публикация

Текущая GitHub Pages репозитория публична, опубликована из `main`/корня. Безопасного отдельного Pages-preview на этом же настроенном target не обнаружено. Переключать source/build этой Pages-сборки небезопасно: это заменило бы действующий preview. PR Antigravity остаётся независимым и открытым. До отдельного изолированного hosting-проекта результат готовится как self-contained V2 static build; публичная ссылка на новый живой сайт не будет заявляться без изолированного origin.

## QA re-check and responsive/asset regression context

On 9 November 2026, the current tech branch was fetched read-only and verified at commit `72ad9a3` (the preceding branch commit is `a1607f7`). Its 30-case runner and existing `tests/qa-report.json` are available at [the tech branch](https://github.com/Valodi-3/dental-master-preview-2026/tree/tech/dental-master-foundation-2026/tests); the committed report states **27 passed / 3 failed**. It reports a 36px Prokshino overflow at 1024px, absent booking trigger, and three external Spanish doctor-photo paths.

The design branch's first direct Playwright geometry pass recorded `documentElement.scrollWidth === window.innerWidth` on both root pages at 390, 768, 1024, 1440 and 1920px (no horizontal overflow). Its Spanish roster already points to five local files under `design/assets/doctors/`, all of which exist and are sourced from clinic-published portraits. The first run of the unchanged foundation test runner against the actual local design branch produced **25/30**: all 18 viewport tests passed; the design branch lacked the required root booking modal/trigger on both pages and a root-page quick-search control, and the runner counted below-fold lazy local portraits as broken because it did not scroll them into view. No technical test or `app.js` change is part of this repair; the final unmodified-suite run is recorded separately.

## Final root-page regression run

The exact unchanged 30-case suite from tech commit `72ad9a3de2668eb2fa7e3f3034a844f0d085fe69` now passes **30/30** on the design branch. Its 18 viewport assertions cover 320/360/375/390/430/768/1024/1440/1920 px on both branch homepages; the 12 remaining functional assertions confirm no localhost links, successful image rendering, modal open/Escape close, no fake form flow, three live search results per branch, and mobile navigation. The report is saved as [`tech-root-qa-30-30.json`](../design/v2qa/tech-root-qa-30-30.json).

A separate smoke record checks both root pages at 390/768/1024/1440/1920 px (**10/10**, zero overflow), both exact DentalPRO dialog targets and phone links (**2/2**), six search states, and all five locally served clinic portraits. Mobile menus expose the correct official online URL on both branches; Spanish Quarters labels the Prokshino destination explicitly. See [`regression-validation.json`](../design/v2qa/regression-validation.json) and [`regression-comparison.json`](../design/v2qa/regression-comparison.json).

The tech branch's existing 27/30 report called the three below-fold portraits broken. The failure is **not reproducible as an HTTP 404**: in a read-only browser/API replay on 2026-11-09, all three exact official image URLs returned HTTP 200 with `image/webp`/`image/jpeg`, and forcing them into view produced nonzero `naturalWidth`. Thus the old check treats not-yet-loaded `loading="lazy"` images as broken. The design branch nevertheless keeps five verified official portraits as local project assets, removing runtime reliance on WordPress; the five local images are loaded deterministically at low priority and verified at 5/5. The report does not characterize those three URLs as 404.

The 36px Prokshino overflow **was** reproduced in the untouched tech commit at 1024px (`scrollWidth=1060`, viewport 1024). The separate design branch already fixed it before this regression patch: pre-patch DOM checks and the final runner both measure 0px at 1024px and the other requested widths. This repair therefore preserves its responsive CSS instead of applying a no-op rewrite. Baseline and final screenshots are in `design/v2qa/screenshots/`.

## Final review and publication boundary

GitHub API/CLI verification confirms [PR #2](https://github.com/Valodi-3/dental-master-preview-2026/pull/2) is `OPEN · Draft`, base `main`, head `design/manus-dental-master-2026`, merge timestamp `null`. After the final push, the local `HEAD` and remote design branch were verified equal with `git rev-parse` and `git ls-remote`; the exact current revision is visible in the linked PR. Remote `main` stayed at `9a99dc7baa6484bbec8b1823152f60a59bdbae2e`; remote tech stayed at `72ad9a3de2668eb2fa7e3f3034a844f0d085fe69`. Original PR #1 remains open, draft and unmerged. The PR diff and staged/committed change set contain no `app.js` or tech-test changes; no production site, GitHub Pages setting or deployment was touched.

## Реализация V6 по визуальной обратной связи

Пользователь попросил приблизить общую визуальную подачу к [AGRR Beauty](https://agrrbeauty.com/), отказаться от посредственного белого фона и завершить всю систему целиком без промежуточного согласования каждого экрана. V6 следует визуальным принципам референса, не копируя его тексты, фотографии, брендинг и бизнес-услуги.

Фактические материалы двух стоматологических филиалов остались локальными в `design/assets/`; новые изображения не генерировались. Основная визуальная система — CSS: локальные переходы, небольшая глубина/perspective и плавная прокрутка с `prefers-reduced-motion`; внешняя 3D/runtime/font-библиотека не подключалась. Кнопка записи сохранила исходный проверенный 4-канальный выбор; main, production и Pages не развертывались.

Финальная route-check: 41 V2 route × 9 размеров, без горизонтального переполнения; применимость темы, локальные изображения и точные контрастные палитры также проверялись автоматически. Скриншоты полных PC-сайтов 1440×4855 и 1440×4780 и их мобильные версии содержатся в разделе V6 [`V2_SCREENSHOT_INDEX.md`](V2_SCREENSHOT_INDEX.md#итерация-6--текущий-дизайн-черновик).
