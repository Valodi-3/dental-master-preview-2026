# Техническая архитектура интеграции Dental VNext в WordPress

**Дата разработки:** 9 ноября 2026 г.  
**Целевая CMS:** WordPress (Classic Editor / PHP 7.4–8.2).  
**Базовая активная тема на production:** `your-clean-template-3`.  
**Сайты:** `dantist-prokshino.ru` и `stomatolog-ispanskie-kvartaly.ru`.

---

## 1. Констатация ограничений окружения (Staging Constraint Note)

* На локальной рабочей станции отсутствует установленный стек MySQL / Apache / Nginx / LocalWP.
* Доступ к боевым серверам хостинга по протоколам SSH / SFTP / cPanel в рамках текущей сессии ограничен политикой безопасности: **произвольная установка плагинов и изменение production строго запрещены**.
* Для безопасного развёртывания подготовлен автономный пакет интеграции:
  1. Дочерняя тема `your-clean-template-3-child` (не затрагивает обновления родительской темы).
  2. Изолированный плагин предпросмотра `dental-vnext-staging.php` (активируется только на staging-поддомене либо по защищённому GET-параметру для авторизованных врачей/клиентов).
  3. Скрипты импорта каталога (254 позиции) в нативные Custom Post Types WordPress.

---

## 2. Архитектура дочерней темы (Child Theme)

Вместо прямой перезаписи файлов темы `your-clean-template-3`, все наработки Manus переносятся через дочернюю тему:

```
wp-content/themes/
├── your-clean-template-3/            # Родительская тема (без изменений)
└── your-clean-template-3-child/      # Дочерняя тема VNext
    ├── style.css                     # Заголовок дочерней темы + импорт
    ├── functions.php                 # Регистрация CPT, таксономий, ассетов
    ├── template-prokshino-vnext.php  # Шаблон страницы филиала Прокшино
    ├── template-ispanskie-vnext.php  # Шаблон страницы филиала Испанские кварталы
    ├── assets/
    │   ├── css/
    │   │   ├── prokshino.css         # Дизайн-система Прокшино
    │   │   └── ispanskie.css         # Дизайн-система Испанские кварталы
    │   ├── js/
    │   │   └── app.js                # Интерактивный контроллер модалок и поиска
    │   └── img/                      # Локализованные изображения клиник
    └── templates/
        ├── part-services-catalog.php # Динамический рендерер каталога (254 услуги)
        ├── part-doctors-grid.php     # Динамический рендерер карточек врачей
        └── part-booking-modal.php    # Модальное окно записи с реальными каналами
```

---

## 3. Модель данных (Custom Post Types & Taxonomies)

### 3.1. Каталог медицинских услуг (`dental_service`)
Услуги больше не хранятся статичным текстом в HTML. Они заводятся как Custom Post Type:

* **Post Type:** `dental_service`
* **Таксономия:** `dental_category` (10 рубрик: `consultations`, `diagnostics`, `anesthesia`, `hygiene`, `treatment`, `endodontics`, `surgery`, `implantation`, `prosthetics`, `orthodontics`).
* **Кастомные поля (Post Meta):**
  * `_service_sku` (string) — уникальный код, например `svc_orthodontics_178`.
  * `_price_prokshino` (int) — цена для Прокшино в рублях.
  * `_price_ispanskie` (int) — цена для Испанских кварталов в рублях.
  * `_branches` (array) — доступность в филиалах (`['prokshino', 'ispanskie']`).
  * `_is_featured` (bool) — вывод в промо-блоке на первом экране.

### 3.2. Доктора клиники (`dental_doctor`)
* **Post Type:** `dental_doctor`
* **Кастомные поля:**
  * `_doctor_branch` (`prokshino` / `ispanskie` / `both`).
  * `_doctor_role` — клиническая должность (напр. «Главный врач филиала»).
  * `_doctor_experience_years` — стаж (напр. 14).
  * `_doctor_quote` — прямая речь доктора о миссии и заботе о пациенте.
  * `_doctor_certs` (array) — галерея сканов дипломов и сертификатов.
  * `_featured_image` — портрет врача.

---

## 4. Обновление каталога без ручного редактирования HTML

Для администраторов клиник предусмотрено три безопасных способа актуализации цен:

1. **Через админку WordPress:**
   В меню появляется раздел «Стоматологические услуги». Администратор открывает услугу, меняет поле `Цена (Прокшино)` или `Цена (Испанские кварталы)` и нажимает «Обновить». HTML страниц пересобирается автоматически.

2. **Пакетный импорт через JSON/CSV:**
   Скрипт `import-services-cli.php` (или интеграция с плагином WP All Import) позволяет за одну секунду синхронизировать все 254 позиции из подготовленного файла `data/services_master.json`.

3. **Синхронизация с 1С / DentalPRO API:**
   Поскольку у каждой услуги зафиксирован `_service_sku`, REST API эндпоинт `POST /wp-json/dental/v1/update-price` принимает JSON с парами `sku: new_price` и обновляет базу данных без участия верстальщика.

---

## 5. Интеграция виджета DentalPRO

* В филиале **Прокшино**: виджет DentalPRO подключается через шорткод `[dentalpro_widget branch="prokshino"]` на странице `/online-zapis/`.
* В филиале **Испанские кварталы**: в связи с тем, что лицензионный токен выдан на головной домен, переход организуется на подтверждённый адрес `https://dantist-prokshino.ru/online-zapis/` с передачей GET-параметра филиала: `?branch=ispanskie`. Если DentalPRO активирует второй токен, шорткод переключается в панели управления.

---

## 6. Резервное копирование и стратегия отката (Rollback SOP)

Перед активацией темы на staging или production выполняется строгий регламент:

1. **Создание снапшота базы данных:**
   \`\`\`bash
   wp db export backup_pre_vnext_\$(date +%Y%m%d_%H%M%S).sql --add-drop-table
   \`\`\`
2. **Архивация каталога `wp-content`:**
   \`\`\`bash
   tar -czf wp-content-backup-\$(date +%Y%m%d).tar.gz wp-content/
   \`\`\`
3. **План экстренного отката (1 клик):**
   В случае непредвиденных сбоев достаточно в консоли WP-CLI переключить активную тему обратно:
   \`\`\`bash
   wp theme activate your-clean-template-3
   \`\`\`
   Родительская тема не модифицируется, поэтому возврат в исходное состояние занимает менее 10 секунд.
