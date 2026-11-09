<?php
/**
 * Child Theme functions for Dental VNext 2026
 *
 * Designed for isolated staging preview and future production migration
 * without affecting parent theme 'your-clean-template-3'.
 */
if (!defined('ABSPATH')) {
    exit;
}

// 1. Safely load Custom Post Types (Services & Doctors)
$child_includes = [
    get_stylesheet_directory() . '/includes/cpt-services.php',
    get_stylesheet_directory() . '/includes/cpt-doctors.php'
];

foreach ($child_includes as $inc_file) {
    if (file_exists($inc_file)) {
        require_once $inc_file;
    }
}

// 2. Enqueue Styles and Scripts for VNext Templates
add_action('wp_enqueue_scripts', function () {
    // Parent theme styling
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css', [], '3.0.0');

    // Child theme override stylesheet
    wp_enqueue_style('child-style', get_stylesheet_uri(), ['parent-style'], '1.0.0');

    // Conditional enqueuing based on active clinic branch template
    if (is_page_template('template-prokshino-vnext.php')) {
        $prokshino_css = get_stylesheet_directory() . '/assets/css/prokshino.css';
        $ver = file_exists($prokshino_css) ? filemtime($prokshino_css) : '20261109';
        wp_enqueue_style('dental-prokshino-vnext', get_stylesheet_directory_uri() . '/assets/css/prokshino.css', ['child-style'], $ver);

        $app_js = get_stylesheet_directory() . '/assets/js/app.js';
        $ver_js = file_exists($app_js) ? filemtime($app_js) : '20261109';
        wp_enqueue_script('dental-app-vnext', get_stylesheet_directory_uri() . '/assets/js/app.js', [], $ver_js, true);
    } elseif (is_page_template('template-ispanskie-vnext.php')) {
        $ispanskie_css = get_stylesheet_directory() . '/assets/css/ispanskie.css';
        $ver = file_exists($ispanskie_css) ? filemtime($ispanskie_css) : '20261109';
        wp_enqueue_style('dental-ispanskie-vnext', get_stylesheet_directory_uri() . '/assets/css/ispanskie.css', ['child-style'], $ver);

        $app_js = get_stylesheet_directory() . '/assets/js/app.js';
        $ver_js = file_exists($app_js) ? filemtime($app_js) : '20261109';
        wp_enqueue_script('dental-app-vnext', get_stylesheet_directory_uri() . '/assets/js/app.js', [], $ver_js, true);
    }
});

// 3. Staging Security Header: Prevent Search Indexing on Staging Templates
add_action('send_headers', function () {
    if (is_page_template('template-prokshino-vnext.php') || is_page_template('template-ispanskie-vnext.php')) {
        header('X-Robots-Tag: noindex, nofollow, noarchive', true);
    }
});
