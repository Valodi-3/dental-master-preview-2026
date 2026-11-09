<?php
/**
 * Template Name: Dental VNext - Испанские кварталы Preview
 * Description: Изолированный шаблон предпросмотра для филиала Испанские кварталы (Dental VNext 2026).
 *
 * @package YourCleanTemplate3Child
 */

if (!defined('ABSPATH')) {
    exit;
}

// 1. Staging Access Guard: require read capability or explicit staging query token
$allow_staging = is_user_logged_in() && current_user_can('read');
if (defined('DENTAL_VNEXT_STAGING_PUBLIC') && DENTAL_VNEXT_STAGING_PUBLIC) {
    $allow_staging = true;
}

if (!$allow_staging) {
    auth_redirect();
    exit;
}

// 2. Strict Search Engine Block
header('X-Robots-Tag: noindex, nofollow, noarchive', true);
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?> class="dental-vnext-root branch-ispanskie">
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <title>ДантистЪ Испанские кварталы — Dental VNext 2026 (Staging Preview)</title>
    <?php wp_head(); ?>
</head>
<body <?php body_class('dental-preview-body vnext-ispanskie'); ?>>
    <div id="vnext-app" class="vnext-wrapper" data-clinic-branch="ispanskie">
        <?php
        // Load custom staging page content or dynamic components
        if (have_posts()) :
            while (have_posts()) : the_post();
                the_content();
            endwhile;
        endif;
        ?>
    </div>
    <?php wp_footer(); ?>
</body>
</html>
