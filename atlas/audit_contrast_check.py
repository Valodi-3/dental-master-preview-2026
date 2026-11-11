def luminance(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r_adj, g_adj, b_adj = adjust(r), adjust(g), adjust(b)
    return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj

def contrast_ratio(hex1, hex2):
    l1 = luminance(hex1)
    l2 = luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

editorial_pairs = [
    ("Title / Loud Ink on Surface", "#1c1917", "#ffffff"),
    ("Title / Loud Ink on Travertine BG", "#1c1917", "#faf7f2"),
    ("Body Ink on Surface", "#44403c", "#ffffff"),
    ("Body Ink on Travertine BG", "#44403c", "#faf7f2"),
    ("Muted Ink on Surface", "#78716c", "#ffffff"),
    ("Muted Ink on Travertine BG", "#78716c", "#faf7f2"),
    ("Accent Bronze on Surface", "#926b2b", "#ffffff"),
    ("Accent Bronze on Accent BG", "#926b2b", "#f9f5ed"),
    ("Primary Button White on Dark Ink", "#ffffff", "#1c1917"),
    ("Procedure Price Bronze on Surface", "#926b2b", "#ffffff"),
]

clinical_pairs = [
    ("Title / Loud Ink on Dark Surface", "#ffffff", "#101c18"),
    ("Title / Loud Ink on Mineral BG", "#ffffff", "#09120f"),
    ("Platinum Body Ink on Dark Surface", "#cbd5e1", "#101c18"),
    ("Platinum Body Ink on Mineral BG", "#cbd5e1", "#09120f"),
    ("Muted Sage on Dark Surface", "#8ea59b", "#101c18"),
    ("Muted Sage on Mineral BG", "#8ea59b", "#09120f"),
    ("Optical Emerald Accent on Dark Surface", "#10b981", "#101c18"),
    ("Mint Price on Dark Surface", "#34d399", "#101c18"),
    ("Primary Button Ink on Emerald", "#05130e", "#10b981"),
    ("Secondary Button White on Alt Surface", "#ffffff", "#0c1613"),
]

print("=== EDITORIAL THEME CONTRAST RATIOS ===")
for label, c1, c2 in editorial_pairs:
    cr = contrast_ratio(c1, c2)
    # WCAG AA requires 4.5:1 for normal text, 3:1 for large text (>=18pt or 14pt bold)
    pass_normal = cr >= 4.5
    pass_large = cr >= 3.0
    status = "PASS AAA" if cr >= 7.0 else ("PASS AA" if pass_normal else ("PASS AA Large" if pass_large else "FAIL"))
    print(f"[{status}] {label} ({c1} on {c2}): {cr:.2f}:1")

print("\n=== CLINICAL THEME CONTRAST RATIOS ===")
for label, c1, c2 in clinical_pairs:
    cr = contrast_ratio(c1, c2)
    pass_normal = cr >= 4.5
    pass_large = cr >= 3.0
    status = "PASS AAA" if cr >= 7.0 else ("PASS AA" if pass_normal else ("PASS AA Large" if pass_large else "FAIL"))
    print(f"[{status}] {label} ({c1} on {c2}): {cr:.2f}:1")
