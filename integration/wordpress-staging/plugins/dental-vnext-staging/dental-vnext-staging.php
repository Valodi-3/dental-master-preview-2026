<?php
/**
 * Plugin Name: Dental VNext Staging Gate (Isolated Preview)
 * Description: Secure staging preview gate for client review without modifying live WordPress pages, active theme, or database.
 * Version: 1.0.0
 * Author: Dental Master Technical Team
 */
if (!defined('ABSPATH')) { exit; }

add_action('template_redirect', function () {
    if (!isset($_GET['vnext_preview'])) {
        return;
    }

    $branch = sanitize_key($_GET['vnext_preview']);
    if (!in_array($branch, ['prokshino', 'ispanskie'], true)) {
        return;
    }

    // Require logged in user with read capability on staging
    if (!is_user_logged_in() || !current_user_can('read')) {
        auth_redirect();
        exit;
    }

    // Serve isolated HTML preview safely
    $file = plugin_dir_path(__FILE__) . "previews/{$branch}.html";
    if (file_exists($file)) {
        header('Content-Type: text/html; charset=UTF-8');
        header('X-Robots-Tag: noindex, nofollow, noarchive');
        readfile($file);
        exit;
    }
}, 1);
