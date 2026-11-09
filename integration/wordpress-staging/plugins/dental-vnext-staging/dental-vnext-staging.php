<?php
/**
 * Plugin Name: Dental VNext Staging Gate (Isolated Preview)
 * Plugin URI: https://dantist-prokshino.ru/
 * Description: Безопасный изолированный шлюз для согласования черновиков Dental VNext 2026 без воздействия на действующие страницы, активную тему и базу данных production.
 * Version: 1.0.1
 * Author: Dental Master Technical Team
 * License: Proprietary
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('template_redirect', function () {
    // Only trigger if preview parameter is requested
    if (!isset($_GET['vnext_preview'])) {
        return;
    }

    $branch = sanitize_key($_GET['vnext_preview']);
    if (!in_array($branch, ['prokshino', 'ispanskie'], true)) {
        return;
    }

    // Role-based Access Control: require authenticated WordPress user with read permissions,
    // or validate a secure staging token constant if defined in wp-config
    $is_authorized = is_user_logged_in() && current_user_can('read');
    if (!$is_authorized && defined('DENTAL_STAGING_TOKEN') && isset($_GET['token'])) {
        if (hash_equals(DENTAL_STAGING_TOKEN, (string)$_GET['token'])) {
            $is_authorized = true;
        }
    }

    if (!$is_authorized) {
        auth_redirect();
        exit;
    }

    // Strict no-index header for staging security
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Robots-Tag: noindex, nofollow, noarchive, nosnippet', true);

    // Locate preview HTML file within plugin previews/ directory
    $preview_file = plugin_dir_path(__FILE__) . "previews/{$branch}.html";
    if (file_exists($preview_file)) {
        readfile($preview_file);
        exit;
    } else {
        wp_die(
            esc_html("Файл предпросмотра для филиала {$branch} не найден в директории плагина."),
            'Dental VNext Staging Error',
            ['response' => 404]
        );
    }
}, 1);
