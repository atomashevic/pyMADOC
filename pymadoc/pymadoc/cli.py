"""
Command-line interface for pyMADOC.
"""

import argparse
import json
from . import list_available_data, download_file, download_community_pair

# File sizes in MB (approximate)
FILE_SIZES = {
    "bluesky": 449.3,
    "koo": 774.3,
    "reddit": {
        "CringeAnarchy": 951.7,
        "fatpeoplehate": 214.5,
        "funny": 9100,  # 9.1 GB
        "gaming": 7200,  # 7.2 GB
        "gifs": 3100,  # 3.1 GB
        "greatawakening": 179.3,
        "KotakuInAction": 1500,  # 1.5 GB
        "MensRights": 797.8,
        "milliondollarextreme": 170.2,
        "pics": 8300,  # 8.3 GB
        "technology": 2500,  # 2.5 GB
        "videos": 6500,  # 6.5 GB
    },
    "voat": {
        "CringeAnarchy": 0.465,  # 464.9 KB
        "fatpeoplehate": 61.9,
        "funny": 18.8,
        "gaming": 12.7,
        "gifs": 2.8,
        "greatawakening": 76.1,
        "KotakuInAction": 1.8,
        "MensRights": 0.774,  # 773.7 KB
        "milliondollarextreme": 3.5,
        "pics": 5.3,
        "technology": 15.2,
        "videos": 0.1,  # ~100KB
    }
}

def format_size(size_mb):
    """Format size from MB to appropriate unit."""
    if size_mb >= 1000:
        return f"{size_mb/1000:.1f} GB"
    elif size_mb < 1:
        return f"{size_mb*1024:.1f} KB"
    else:
        return f"{size_mb:.1f} MB"

def print_available_data():
    """Print available platforms and communities in a formatted way."""
    data = list_available_data()
    
    print("\n=== MADOC Dataset Available Files ===\n")
    
    # Print standalone platforms
    print("Standalone Platforms:")
    print("-" * 50)
    for platform in ["bluesky", "koo"]:
        size = format_size(FILE_SIZES[platform])
        print(f"{platform:<10} ({size})")
    print()
    
    # Print platforms with communities
    print("Platforms with Communities:")
    print("-" * 50)
    for platform in ["reddit", "voat"]:
        print(f"\n{platform.upper()}:")
        for community in data["communities"]:
            size = format_size(FILE_SIZES[platform][community])
            print(f"  {community:<20} ({size})")
    
    print("\nNote: You can download individual files using:")
    print("  pymadoc download <platform> [--community <community>]")
    print("\nOr download Reddit-Voat pairs using:")
    print("  pymadoc pair <community>")

def main():
    parser = argparse.ArgumentParser(description="Download and manage MADOC dataset files")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available platforms and communities")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download a specific file")
    download_parser.add_argument("platform", help="Platform name (reddit, voat, bluesky, koo)")
    download_parser.add_argument("--community", help="Community name (required for reddit and voat)")
    download_parser.add_argument("--output-dir", default=".", help="Output directory")
    
    # Pair command
    pair_parser = subparsers.add_parser("pair", help="Download Reddit-Voat community pair")
    pair_parser.add_argument("community", help="Community name")
    pair_parser.add_argument("--output-dir", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    if args.command == "list":
        print_available_data()
    
    elif args.command == "download":
        try:
            filepath = download_file(
                args.platform,
                community=args.community,
                output_dir=args.output_dir
            )
            print(f"Downloaded: {filepath}")
        except ValueError as e:
            print(f"Error: {str(e)}")
    
    elif args.command == "pair":
        try:
            reddit_file, voat_file = download_community_pair(
                args.community,
                output_dir=args.output_dir
            )
            print(f"Downloaded Reddit file: {reddit_file}")
            print(f"Downloaded Voat file: {voat_file}")
        except ValueError as e:
            print(f"Error: {str(e)}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 