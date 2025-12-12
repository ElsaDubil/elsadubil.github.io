#!/usr/bin/env python3
"""
Image Optimization Script for elsadubil.github.io
Converts images to WebP format and creates multiple sizes for responsive images
"""

import os
from PIL import Image
import glob

def optimize_image(input_path, output_dir='assets/optimized'):
    """
    Convert image to WebP and create multiple sizes
    Returns dict with paths to different sizes
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    try:
        # Open image
        img = Image.open(input_path)

        # Convert RGBA to RGB if necessary (WebP supports both but this ensures compatibility)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Get original dimensions
        original_width, original_height = img.size

        # Define sizes for responsive images
        # Format: (width, suffix, quality)
        sizes = [
            (400, 'sm', 80),   # Small (mobile)
            (800, 'md', 85),   # Medium (tablet)
            (1200, 'lg', 85),  # Large (desktop)
        ]

        # Only create sizes smaller than original
        created_files = []

        for target_width, suffix, quality in sizes:
            if target_width < original_width:
                # Calculate proportional height
                ratio = target_width / original_width
                target_height = int(original_height * ratio)

                # Resize image
                resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # Save as WebP
                output_path = os.path.join(output_dir, f"{base_name}_{suffix}.webp")
                resized.save(output_path, 'WEBP', quality=quality, method=6)

                created_files.append({
                    'path': output_path,
                    'width': target_width,
                    'suffix': suffix
                })

                file_size_kb = os.path.getsize(output_path) / 1024
                print(f"  Created {suffix}: {target_width}x{target_height} ({file_size_kb:.1f} KB)")

        # Also create a full-size WebP (but optimized)
        full_output_path = os.path.join(output_dir, f"{base_name}.webp")
        img.save(full_output_path, 'WEBP', quality=85, method=6)
        full_size_kb = os.path.getsize(full_output_path) / 1024
        print(f"  Created full: {original_width}x{original_height} ({full_size_kb:.1f} KB)")

        created_files.append({
            'path': full_output_path,
            'width': original_width,
            'suffix': 'full'
        })

        # Get original file size for comparison
        original_size_kb = os.path.getsize(input_path) / 1024
        print(f"  Original size: {original_size_kb:.1f} KB")
        print(f"  Savings: {((original_size_kb - full_size_kb) / original_size_kb * 100):.1f}%")

        return created_files

    except Exception as e:
        print(f"  Error processing {input_path}: {e}")
        return []

def main():
    """Main function to process all images"""

    # Priority images to optimize first
    priority_images = [
        'assets/profile.png',              # 20 MB - CRITICAL
        'assets/rope headshot.jpg',        # 544 KB
        'assets/paper.PNG',                # 210 KB
        'assets/kymograph.png',            # 57 KB
        'assets/ec engr 88s.PNG',          # 112 KB
    ]

    print("="*60)
    print("OPTIMIZING PRIORITY IMAGES")
    print("="*60)

    for img_path in priority_images:
        if os.path.exists(img_path):
            print(f"\nProcessing: {img_path}")
            optimize_image(img_path)
        else:
            print(f"\nSkipping (not found): {img_path}")

    print("\n" + "="*60)
    print("OPTIMIZING PORTFOLIO IMAGES")
    print("="*60)

    # Process all portfolio images
    portfolio_patterns = [
        'assets/Straps/*.JPG',
        'assets/Straps/*.jpg',
        'assets/Straps/*.PNG',
        'assets/Straps/*.png',
        'assets/Silks/*.JPG',
        'assets/Silks/*.jpg',
        'assets/Silks/*.PNG',
        'assets/Silks/*.png',
        'assets/Pole/*.JPG',
        'assets/Pole/*.jpg',
    ]

    portfolio_images = []
    for pattern in portfolio_patterns:
        portfolio_images.extend(glob.glob(pattern))

    print(f"\nFound {len(portfolio_images)} portfolio images to optimize")

    for i, img_path in enumerate(portfolio_images, 1):
        print(f"\n[{i}/{len(portfolio_images)}] Processing: {os.path.basename(img_path)}")
        optimize_image(img_path)

    print("\n" + "="*60)
    print("OPTIMIZATION COMPLETE!")
    print("="*60)
    print("\nOptimized images saved to: assets/optimized/")
    print("\nNext steps:")
    print("1. Update HTML files to use new WebP images")
    print("2. Add lazy loading attributes")
    print("3. Add srcset for responsive images")

if __name__ == '__main__':
    main()
