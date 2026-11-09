<?php
/**
 * Register Custom Post Type: Dental Service
 */
if (!defined('ABSPATH')) { exit; }

add_action('init', function () {
    $labels = [
        'name'               => 'Стоматологические услуги',
        'singular_name'      => 'Услуга',
        'add_new'            => 'Добавить услугу',
        'add_new_item'       => 'Добавить новую услугу',
        'edit_item'          => 'Редактировать услугу',
        'new_item'           => 'Новая услуга',
        'view_item'          => 'Просмотр услуги',
        'search_items'       => 'Искать услугу',
        'not_found'          => 'Услуг не найдено',
        'menu_name'          => 'Прайс-лист'
    ];

    register_post_type('dental_service', [
        'labels'             => $labels,
        'public'             => true,
        'has_archive'        => false,
        'show_in_rest'       => true,
        'menu_icon'          => 'dashicons-editor-ul',
        'supports'           => ['title', 'editor', 'custom-fields'],
        'taxonomies'         => ['dental_category']
    ]);

    // Taxonomy: Category
    register_taxonomy('dental_category', 'dental_service', [
        'hierarchical'       => true,
        'labels'             => [
            'name'           => 'Категории услуг',
            'singular_name'  => 'Категория',
            'menu_name'      => 'Категории'
        ],
        'show_in_rest'       => true,
        'show_admin_column'  => true,
        'rewrite'            => ['slug' => 'dental-category']
    ]);
});
