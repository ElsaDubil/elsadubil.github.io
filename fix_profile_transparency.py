#!/usr/bin/env python3
"""
Fix profile image to preserve transparency
"""

import os
from PIL import Image

def optimize_with_transparency(input_path, output_dir='assets/optimized'):
    """
    Convert image to WebP while preserving transparency
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    try:
        # Open image
        img = Image.open(input_path)

        print(f"Original mode: {img.mode}")
        print(f"Original size: {img.size}")

        # Preserve RGBA mode for transparency
        if img.mode == 'P':
            img = img.convert('RGBA')
        elif img.mode == 'RGB':
            # If it's RGB, we can't add transparency back
            print("Warning: Image is RGB, no transparency to preserve")

        # Get original dimensions
        original_width, original_height = img.size

        # Define sizes for responsive images
        sizes = [
            (400, 'sm', 90),
            (800, 'md', 90),
            (1200, 'lg', 90),
        ]

        created_files = []

        for target_width, suffix, quality in sizes:
            if target_width < original_width:
                # Calculate proportional height
                ratio = target_width / original_width
                target_height = int(original_height * ratio)

                # Resize image while preserving transparency
                resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # Save as WebP with transparency
                output_path = os.path.join(output_dir, f"{base_name}_{suffix}.webp")
                resized.save(output_path, 'WEBP', quality=quality, method=6)

                file_size_kb = os.path.getsize(output_path) / 1024
                print(f"Created {suffix}: {target_width}x{target_height} ({file_size_kb:.1f} KB)")

                created_files.append(output_path)

        # Create full-size WebP with transparency
        full_output_path = os.path.join(output_dir, f"{base_name}.webp")
        img.save(full_output_path, 'WEBP', quality=90, method=6)

        full_size_kb = os.path.getsize(full_output_path) / 1024
        print(f"Created full: {original_width}x{original_height} ({full_size_kb:.1f} KB)")

        created_files.append(full_output_path)

        # Original file size
        original_size_kb = os.path.getsize(input_path) / 1024
        print(f"Original size: {original_size_kb:.1f} KB")
        print(f"Savings: {((original_size_kb - full_size_kb) / original_size_kb * 100):.1f}%")

        return created_files

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return []

def main():
    print("=" * 60)
    print("FIXING PROFILE IMAGE - PRESERVING TRANSPARENCY")
    print("=" * 60)

    input_path = 'assets/profile.png'

    if os.path.exists(input_path):
        print(f"\nProcessing: {input_path}")
        optimize_with_transparency(input_path)
        print("\n" + "=" * 60)
        print("DONE! Profile image re-optimized with transparency preserved")
        print("=" * 60)
    else:
        print(f"Error: {input_path} not found")

if __name__ == '__main__':
    main()
