<?php
/**
 * WP-CLI / Standalone CLI Script to Import Dental Master Catalog (254 items)
 *
 * Usage:
 *   wp eval-file import-services-cli.php
 *   wp eval-file import-services-cli.php --dry-run
 *   wp eval-file import-services-cli.php --file=/path/to/wp_services_import.json
 *   wp eval-file import-services-cli.php --dry-run --skip-existing
 *
 * @package DentalVNext
 */

// 1. Environment check: must run inside WordPress (e.g. WP-CLI)
if (!defined('ABSPATH')) {
    fwrite(STDERR, "Error: This script must be executed within WordPress environment (e.g. via 'wp eval-file').\n");
    exit(1);
}

// 2. Parse command-line options ($args / $argv)
$options = [
    'dry_run'       => false,
    'skip_existing' => false,
    'file'          => null,
    'verbose'       => false
];

$cli_args = isset($argv) ? $argv : (isset($args) ? $args : []);
foreach ($cli_args as $arg) {
    if ($arg === '--dry-run' || $arg === '-d') {
        $options['dry_run'] = true;
    } elseif ($arg === '--skip-existing') {
        $options['skip_existing'] = true;
    } elseif ($arg === '--verbose' || $arg === '-v') {
        $options['verbose'] = true;
    } elseif (strpos($arg, '--file=') === 0) {
        $options['file'] = substr($arg, 7);
    }
}

// 3. Resolve path to wp_services_import.json
$candidate_paths = [];
if (!empty($options['file'])) {
    $candidate_paths[] = $options['file'];
}
if (getenv('DENTAL_SERVICES_IMPORT_FILE')) {
    $candidate_paths[] = getenv('DENTAL_SERVICES_IMPORT_FILE');
}

// Candidate 1: 3 levels up from scripts dir (repo root: integration/wordpress-staging/scripts -> repo root/data/...)
$candidate_paths[] = dirname(__DIR__, 3) . '/data/wp_services_import.json';
// Candidate 2: 2 levels up
$candidate_paths[] = dirname(__DIR__, 2) . '/data/wp_services_import.json';
// Candidate 3: In wp-content dental-data
if (defined('WP_CONTENT_DIR')) {
    $candidate_paths[] = WP_CONTENT_DIR . '/dental-data/wp_services_import.json';
}
// Candidate 4: Current working directory
$candidate_paths[] = getcwd() . '/data/wp_services_import.json';
$candidate_paths[] = __DIR__ . '/wp_services_import.json';

$data_file = null;
foreach ($candidate_paths as $cand) {
    if (file_exists($cand) && is_readable($cand)) {
        $data_file = realpath($cand);
        break;
    }
}

if (!$data_file) {
    fwrite(STDERR, "[ERROR] Services data file (wp_services_import.json) not found.\n");
    fwrite(STDERR, "Tried the following locations:\n");
    foreach ($candidate_paths as $cand) {
        fwrite(STDERR, "  - {$cand}\n");
    }
    fwrite(STDERR, "Provide file location via '--file=/path/to/wp_services_import.json' or set DENTAL_SERVICES_IMPORT_FILE environment variable.\n");
    exit(1);
}

echo "=== DENTAL SERVICES IMPORT TOOL ===\n";
echo "Resolved catalog file: {$data_file}\n";
echo "Mode: " . ($options['dry_run'] ? "[DRY-RUN - NO DB CHANGES]" : "[LIVE IMPORT]") . "\n";
if ($options['skip_existing']) {
    echo "Duplicate policy: Skip existing posts\n";
}
echo "------------------------------------\n";

// 4. Read and validate JSON
$raw_json = file_get_contents($data_file);
if ($raw_json === false) {
    fwrite(STDERR, "[ERROR] Failed to read catalog file: {$data_file}\n");
    exit(1);
}

$services = json_decode($raw_json, true);
$json_err = json_last_error();
if ($json_err !== JSON_ERROR_NONE) {
    fwrite(STDERR, "[ERROR] Invalid JSON syntax: " . json_last_error_msg() . "\n");
    exit(1);
}

if (!is_array($services) || empty($services)) {
    fwrite(STDERR, "[ERROR] Catalog JSON must be a non-empty array of service objects.\n");
    exit(1);
}

$total_count = count($services);
echo "Loaded {$total_count} services from JSON.\n";

// 5. Schema Validation & Duplicate SKU check
$validation_errors = [];
$seen_skus = [];
$valid_services = [];

foreach ($services as $idx => $svc) {
    $errs = [];
    if (empty($svc['post_title']) || !is_string($svc['post_title'])) {
        $errs[] = "Missing or invalid 'post_title'";
    }
    if (!isset($svc['post_content'])) {
        $errs[] = "Missing 'post_content'";
    }
    if (empty($svc['meta_input']['_service_sku'])) {
        $errs[] = "Missing 'meta_input._service_sku'";
    } else {
        $sku = (string)$svc['meta_input']['_service_sku'];
        if (isset($seen_skus[$sku])) {
            $errs[] = "Duplicate SKU '{$sku}' in JSON (first seen at index {$seen_skus[$sku]})";
        } else {
            $seen_skus[$sku] = $idx;
        }
    }
    // Check price in either _price_prokshino or _service_price_rub
    $has_price = false;
    if (isset($svc['meta_input']['_price_prokshino']) && is_numeric($svc['meta_input']['_price_prokshino'])) {
        $has_price = true;
    } elseif (isset($svc['meta_input']['_service_price_rub']) && is_numeric($svc['meta_input']['_service_price_rub'])) {
        $has_price = true;
    }
    if (!$has_price) {
        $errs[] = "Missing or non-numeric price ('_price_prokshino' or '_service_price_rub')";
    }

    if (empty($svc['tax_input']['dental_category'])) {
        $errs[] = "Missing 'tax_input.dental_category'";
    }

    if (!empty($errs)) {
        $validation_errors[$idx] = [
            'title'  => isset($svc['post_title']) ? $svc['post_title'] : "Item #{$idx}",
            'sku'    => isset($svc['meta_input']['_service_sku']) ? $svc['meta_input']['_service_sku'] : 'N/A',
            'errors' => $errs
        ];
    } else {
        $valid_services[] = $svc;
    }
}

if (!empty($validation_errors)) {
    fwrite(STDERR, "[VALIDATION FAILED] " . count($validation_errors) . " items have schema errors:\n");
    foreach (array_slice($validation_errors, 0, 10, true) as $idx => $err_info) {
        fwrite(STDERR, "  - Item #{$idx} (SKU: {$err_info['sku']}): " . implode(', ', $err_info['errors']) . "\n");
    }
    if (count($validation_errors) > 10) {
        fwrite(STDERR, "  ... and " . (count($validation_errors) - 10) . " more items.\n");
    }
    exit(1);
}

echo "Schema validation: PASS (All {$total_count} records valid).\n";

// 6. Processing Services (Dry-run or Live)
$stats = [
    'total'   => $total_count,
    'created' => 0,
    'updated' => 0,
    'skipped' => 0,
    'failed'  => 0
];

foreach ($valid_services as $svc) {
    $sku = $svc['meta_input']['_service_sku'];
    $category = $svc['tax_input']['dental_category'];

    // Check if service post already exists by SKU
    $existing = get_posts([
        'post_type'      => 'dental_service',
        'meta_key'       => '_service_sku',
        'meta_value'     => $sku,
        'posts_per_page' => 1,
        'post_status'    => 'any'
    ]);

    if ($existing) {
        $post_id = $existing[0]->ID;
        if ($options['skip_existing']) {
            $stats['skipped']++;
            if ($options['verbose']) {
                echo "[SKIP] Existing SKU '{$sku}' (Post ID: {$post_id})\n";
            }
            continue;
        }

        if ($options['dry_run']) {
            $stats['updated']++;
            continue;
        }

        // Live Update
        $update_result = wp_update_post([
            'ID'           => $post_id,
            'post_title'   => sanitize_text_field($svc['post_title']),
            'post_content' => wp_kses_post($svc['post_content'])
        ], true);

        if (is_wp_error($update_result)) {
            $stats['failed']++;
            fwrite(STDERR, "[ERROR] Failed updating SKU '{$sku}': " . $update_result->get_error_message() . "\n");
            continue;
        }

        // Update taxonomy & meta
        wp_set_object_terms($post_id, (array)$category, 'dental_category', false);
        foreach ($svc['meta_input'] as $meta_k => $meta_v) {
            $meta_val = is_array($meta_v) ? wp_json_encode($meta_v) : (string)$meta_v;
            update_post_meta($post_id, sanitize_key($meta_k), sanitize_text_field($meta_val));
        }
        $stats['updated']++;
    } else {
        // New post
        if ($options['dry_run']) {
            $stats['created']++;
            continue;
        }

        // Live Insert
        $new_id = wp_insert_post([
            'post_type'    => 'dental_service',
            'post_title'   => sanitize_text_field($svc['post_title']),
            'post_content' => wp_kses_post($svc['post_content']),
            'post_status'  => 'publish'
        ], true);

        if (is_wp_error($new_id)) {
            $stats['failed']++;
            fwrite(STDERR, "[ERROR] Failed creating SKU '{$sku}': " . $new_id->get_error_message() . "\n");
            continue;
        }

        // Assign taxonomy & meta
        wp_set_object_terms($new_id, (array)$category, 'dental_category', false);
        foreach ($svc['meta_input'] as $meta_k => $meta_v) {
            $meta_val = is_array($meta_v) ? wp_json_encode($meta_v) : (string)$meta_v;
            update_post_meta($new_id, sanitize_key($meta_k), sanitize_text_field($meta_val));
        }
        $stats['created']++;
    }
}

echo "------------------------------------\n";
echo "IMPORT SUMMARY:\n";
echo "  Total Services : {$stats['total']}\n";
echo "  Created (New)  : {$stats['created']}\n";
echo "  Updated        : {$stats['updated']}\n";
echo "  Skipped        : {$stats['skipped']}\n";
echo "  Failed / Errors: {$stats['failed']}\n";

if ($options['dry_run']) {
    echo "Result: DRY-RUN COMPLETED SUCCESSFULLY. No database modifications made.\n";
} else {
    echo "Result: LIVE IMPORT COMPLETED.\n";
}

if ($stats['failed'] > 0) {
    exit(1);
}
exit(0);
