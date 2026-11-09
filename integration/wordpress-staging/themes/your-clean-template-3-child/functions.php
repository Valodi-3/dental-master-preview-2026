<?php
/**
 * Child Theme functions for Dental VNext
 */
if (!defined('ABSPATH')) { exit; }

require_once get_stylesheet_directory() . '/includes/cpt-services.php';
require_once get_stylesheet_directory() . '/includes/cpt-doctors.php';

add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');

    // Conditional enqueuing based on active clinic branch or page template
    if (is_page_template('template-prokshino-vnext.php')) {
        wp_enqueue_style('dental-prokshino-vnext', get_stylesheet_directory_uri() . '/assets/css/prokshino.css', [], '20261109');
        wp_enqueue_script('dental-app-vnext', get_stylesheet_directory_uri() . '/assets/js/app.js', [], '20261109', true);
    } elseif (is_page_template('template-ispanskie-vnext.php')) {
        wp_enqueue_style('dental-ispanskie-vnext', get_stylesheet_directory_uri() . '/assets/css/ispanskie.css', [], '20261109');
        wp_enqueue_script('dental-app-vnext', get_stylesheet_directory_uri() . '/assets/js/app.js', [], '20261109', true);
    }
});
