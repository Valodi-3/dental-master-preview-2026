<?php
/**
 * Register Custom Post Type: Dental Doctor
 */
if (!defined('ABSPATH')) { exit; }

add_action('init', function () {
    register_post_type('dental_doctor', [
        'labels' => [
            'name'          => 'Врачи клиники',
            'singular_name' => 'Врач',
            'add_new_item'  => 'Добавить врача'
        ],
        'public'        => true,
        'has_archive'   => false,
        'show_in_rest'  => true,
        'menu_icon'     => 'dashicons-businessperson',
        'supports'      => ['title', 'editor', 'thumbnail', 'custom-fields']
    ]);
});
