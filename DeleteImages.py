
#!/usr/bin/env python3

"""
Script to delete images smaller than 400x400 pixels from a folder.
Supports common image formats: JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP
"""

import os
import sys
from PIL import Image
import argparse
from pathlib import Path

def get_image_dimensions(file_path):
    """
    Get the dimensions of an image file.
    Returns (width, height) tuple or None if file cannot be opened as image.
    """
    try:
        with Image.open(file_path) as img:
            return img.size
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None

def is_image_file(file_path):
    """Check if file is a supported image format."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp'}
    return file_path.suffix.lower() in image_extensions

def delete_small_images(folder_path, min_width=400, min_height=400, dry_run=False):
    """
    Delete images smaller than specified dimensions from folder.
    
    Args:
        folder_path (str): Path to folder containing images
        min_width (int): Minimum width in pixels (default 400)
        min_height (int): Minimum height in pixels (default 400)
        dry_run (bool): If True, only show what would be deleted without actually deleting
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return
    
    deleted_count = 0
    kept_count = 0
    error_count = 0
    
    print(f"Scanning folder: {folder_path}")
    print(f"Minimum size: {min_width}x{min_height} pixels")
    if dry_run:
        print("DRY RUN MODE - No files will actually be deleted")
    print("-" * 50)
    
    # Get all files in the folder
    all_files = [f for f in folder.iterdir() if f.is_file()]
    image_files = [f for f in all_files if is_image_file(f)]
    
    if not image_files:
        print("No image files found in the folder.")
        return
    
    print(f"Found {len(image_files)} image files to process...")
    print()
    
    for file_path in image_files:
        dimensions = get_image_dimensions(file_path)
        
        if dimensions is None:
            error_count += 1
            continue
        
        width, height = dimensions
        
        if width < min_width or height < min_height:
            if dry_run:
                print(f"WOULD DELETE: {file_path.name} ({width}x{height})")
            else:
                try:
                    file_path.unlink()
                    print(f"DELETED: {file_path.name} ({width}x{height})")
                    deleted_count += 1
                except Exception as e:
                    print(f"ERROR deleting {file_path.name}: {e}")
                    error_count += 1
        else:
            kept_count += 1
            print(f"KEPT: {file_path.name} ({width}x{height})")
    
    print()
    print("-" * 50)
    print("SUMMARY:")
    if dry_run:
        print(f"Files that would be deleted: {len(image_files) - kept_count - error_count}")
    else:
        print(f"Files deleted: {deleted_count}")
    print(f"Files kept: {kept_count}")
    if error_count > 0:
        print(f"Files with errors: {error_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Delete images smaller than specified dimensions from a folder"
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing images"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=400,
        help="Minimum width in pixels (default: 400)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=400,
        help="Minimum height in pixels (default: 400)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting files"
    )
    
    args = parser.parse_args()
    
    # Confirmation prompt (skip in dry run mode)
    if not args.dry_run:
        print(f"WARNING: This will permanently delete images smaller than {args.width}x{args.height} pixels")
        print(f"from folder: {args.folder}")
        response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
        if response not in ['yes', 'y']:
            print("Operation cancelled.")
            return
    
    delete_small_images(
        args.folder,
        min_width=args.width,
        min_height=args.height,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()

