<?php
/**
 * WP-CLI Command / Standalone Script to Import Master Catalog (254 items)
 * Usage: wp eval-file import-services-cli.php
 */
if (!defined('ABSPATH')) {
    echo "This script must be run within a WordPress environment (e.g. via wp eval-file).\n";
    exit(1);
}

$dataFile = dirname(__DIR__, 2) . '/data/wp_services_import.json';
if (!file_exists($dataFile)) {
    echo "Data file not found: $dataFile\n";
    exit(1);
}

$services = json_decode(file_get_contents($dataFile), true);
echo "Importing " . count($services) . " dental services into WordPress...\n";

$imported = 0;
foreach ($services as $svc) {
    // Check if service already exists by SKU
    $sku = $svc['meta_input']['_service_sku'];
    $existing = get_posts([
        'post_type' => 'dental_service',
        'meta_key' => '_service_sku',
        'meta_value' => $sku,
        'posts_per_page' => 1
    ]);

    if ($existing) {
        $postId = $existing[0]->ID;
        wp_update_post([
            'ID' => $postId,
            'post_title' => $svc['post_title'],
            'post_content' => $svc['post_content']
        ]);
    } else {
        $postId = wp_insert_post([
            'post_type' => 'dental_service',
            'post_title' => $svc['post_title'],
            'post_content' => $svc['post_content'],
            'post_status' => 'publish'
        ]);
    }

    // Update categories
    if (!empty($svc['tax_input']['dental_category'])) {
        wp_set_object_terms($postId, $svc['tax_input']['dental_category'], 'dental_category', false);
    }

    // Update meta fields
    foreach ($svc['meta_input'] as $metaKey => $metaVal) {
        update_post_meta($postId, $metaKey, $metaVal);
    }
    $imported++;
}

echo "Successfully imported/updated $imported services.\n";
