#!/usr/bin/env python3
"""
Script to update performingarts.html with optimized WebP images
"""

import re
import os

def create_picture_tag(original_src, alt_text, has_responsive=True):
    """
    Create a picture tag with WebP source and fallback
    """
    # Extract filename from path
    filename = os.path.basename(original_src)
    base_name = os.path.splitext(filename)[0]

    if has_responsive:
        # Use responsive srcset
        return f'''<picture>
                                            <source
                                                type="image/webp"
                                                srcset="assets/optimized/{base_name}_sm.webp 400w,
                                                        assets/optimized/{base_name}_md.webp 800w,
                                                        assets/optimized/{base_name}_lg.webp 1200w,
                                                        assets/optimized/{base_name}.webp"
                                                sizes="(max-width: 576px) 400px, (max-width: 992px) 800px, 1200px">
                                            <img class="img-fluid" src="{original_src}" alt="{alt_text}" loading="lazy" />
                                        </picture>'''
    else:
        # Just WebP fallback
        return f'''<picture>
                                            <source type="image/webp" srcset="assets/optimized/{base_name}.webp">
                                            <img class="img-fluid" src="{original_src}" alt="{alt_text}" loading="lazy" />
                                        </picture>'''

def main():
    input_file = 'performingarts.html'
    output_file = 'performingarts_optimized.html'

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match img tags
    img_pattern = r'<img\s+class="img-fluid"\s+src="([^"]+)"\s+alt="([^"]*)"(?:\s*/>|>)'
    img_pattern2 = r'<img\s+class="img-fluid"\s+src="([^"]+)"\s+alt="([^"]*)"(?:\s*/>|>)'
    img_pattern3 = r'src="(assets/[^"]+)"'

    # Find all image tags that need to be updated
    matches = re.findall(r'<img[^>]+src="assets/([^"]+)"[^>]*>', content, re.IGNORECASE)

    print(f"Found {len(matches)} image references to update")

    # Replace each img tag with picture tag
    def replace_img(match):
        full_match = match.group(0)
        src = re.search(r'src="([^"]+)"', full_match).group(1)

        # Extract alt text if present
        alt_match = re.search(r'alt="([^"]*)"', full_match)
        alt = alt_match.group(1) if alt_match else "Performance art photo"

        # Check if it's a large portfolio image (should have responsive)
        has_responsive = 'Original' in src or 'rope headshot' in src

        return create_picture_tag(src, alt, has_responsive)

    # Replace all img tags
    updated_content = re.sub(
        r'<img[^>]+class="img-fluid"[^>]+src="assets/[^"]+"[^>]*>',
        replace_img,
        content,
        flags=re.IGNORECASE
    )

    # Add defer to scripts
    updated_content = updated_content.replace(
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" defer></script>'
    )
    updated_content = updated_content.replace(
        '<script src="js/scripts.js"></script>',
        '<script src="js/scripts.js" defer></script>'
    )

    # Write to new file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"\nUpdated file saved to: {output_file}")
    print("\nPlease review the changes and then rename to performingarts.html")

if __name__ == '__main__':
    main()
