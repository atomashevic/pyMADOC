"""
pyMADOC - Python package to download and combine parts of MADOC dataset.
"""

import os
import sys
import requests
from tqdm import tqdm
import pandas as pd

# Direct download URLs for each file
FILE_URLS = {
    "bluesky": "https://zenodo.org/records/14637314/files/bluesky_madoc.parquet",
    "koo": "https://zenodo.org/records/14637314/files/koo_madoc.parquet",
    "reddit": {
        "CringeAnarchy": "https://zenodo.org/records/14637314/files/reddit_CringeAnarchy_madoc.parquet",
        "fatpeoplehate": "https://zenodo.org/records/14637314/files/reddit_fatpeoplehate_madoc.parquet",
        "funny": "https://zenodo.org/records/14637314/files/reddit_funny_madoc.parquet",
        "gaming": "https://zenodo.org/records/14637314/files/reddit_gaming_madoc.parquet",
        "gifs": "https://zenodo.org/records/14637314/files/reddit_gifs_madoc.parquet",
        "greatawakening": "https://zenodo.org/records/14637314/files/reddit_greatawakening_madoc.parquet",
        "KotakuInAction": "https://zenodo.org/records/14637314/files/reddit_KotakuInAction_madoc.parquet",
        "MensRights": "https://zenodo.org/records/14637314/files/reddit_MensRights_madoc.parquet",
        "milliondollarextreme": "https://zenodo.org/records/14637314/files/reddit_milliondollarextreme_madoc.parquet",
        "pics": "https://zenodo.org/records/14637314/files/reddit_pics_madoc.parquet",
        "technology": "https://zenodo.org/records/14637314/files/reddit_technology_madoc.parquet",
        "videos": "https://zenodo.org/records/14637314/files/reddit_videos_madoc.parquet"
    },
    "voat": {
        "CringeAnarchy": "https://zenodo.org/records/14637314/files/voat_CringeAnarchy_madoc.parquet",
        "fatpeoplehate": "https://zenodo.org/records/14637314/files/voat_fatpeoplehate_madoc.parquet",
        "funny": "https://zenodo.org/records/14637314/files/voat_funny_madoc.parquet",
        "gaming": "https://zenodo.org/records/14637314/files/voat_gaming_madoc.parquet",
        "gifs": "https://zenodo.org/records/14637314/files/voat_gifs_madoc.parquet",
        "greatawakening": "https://zenodo.org/records/14637314/files/voat_greatawakening_madoc.parquet",
        "KotakuInAction": "https://zenodo.org/records/14637314/files/voat_KotakuInAction_madoc.parquet",
        "MensRights": "https://zenodo.org/records/14637314/files/voat_MensRights_madoc.parquet",
        "milliondollarextreme": "https://zenodo.org/records/14637314/files/voat_milliondollarextreme_madoc.parquet",
        "pics": "https://zenodo.org/records/14637314/files/voat_pics_madoc.parquet",
        "technology": "https://zenodo.org/records/14637314/files/voat_technology_madoc.parquet",
        "videos": "https://zenodo.org/records/14637314/files/voat_videos_madoc.parquet"
    }
}

PLATFORMS = list(FILE_URLS.keys())
COMMUNITIES = list(FILE_URLS["reddit"].keys())  # Same communities for reddit and voat

def list_available_data():
    """List available platforms and communities in the MADOC dataset."""
    return {
        "platforms": PLATFORMS,
        "communities": COMMUNITIES
    }

def download_with_progress(url, filename):
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(block_size):
            size = f.write(data)
            pbar.update(size)

def download_file(platform, community=None, as_dataframe=False, output_dir="."):
    """
    Download a specific file from the MADOC dataset.
    
    Args:
        platform (str): Platform name ('reddit', 'voat', 'bluesky', 'koo')
        community (str, optional): Community name (required for reddit and voat)
        as_dataframe (bool): If True, returns pandas DataFrame instead of saving file
        output_dir (str): Directory to save the downloaded file
        
    Returns:
        Union[str, pd.DataFrame]: Path to downloaded file or pandas DataFrame
    """
    if platform not in PLATFORMS:
        raise ValueError(f"Platform must be one of {PLATFORMS}")
        
    if platform in ["reddit", "voat"]:
        if not community or community not in COMMUNITIES:
            raise ValueError(f"Community must be one of {COMMUNITIES} for {platform}")
        filename = f"{platform}_{community}_madoc.parquet"
        url = FILE_URLS[platform][community]
    else:
        if community:
            raise ValueError(f"Community should not be specified for {platform}")
        filename = f"{platform}_madoc.parquet"
        url = FILE_URLS[platform]
    
    # Create output directory if it doesn't exist
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)
    
    # Set the full path for the file
    filepath = os.path.join(output_dir, filename)
    
    try:
        # Download the file with progress bar
        download_with_progress(url, filepath)
        
        if as_dataframe:
            df = pd.read_parquet(filepath)
            os.remove(filepath)  # Clean up the downloaded file
            return df
        else:
            return filename
    except Exception as e:
        # Clean up partially downloaded file if it exists
        if os.path.exists(filepath):
            os.remove(filepath)
        raise RuntimeError(f"Failed to download file: {str(e)}")

def download_community_pair(community, as_dataframe=False, output_dir="."):
    """
    Download and optionally combine Reddit and Voat data for a specific community.
    
    Args:
        community (str): Community name
        as_dataframe (bool): If True, returns combined pandas DataFrame
        output_dir (str): Directory to save the downloaded files
        
    Returns:
        Union[tuple[str, str], pd.DataFrame]: Tuple of file paths or combined DataFrame
    """
    if community not in COMMUNITIES:
        raise ValueError(f"Community must be one of {COMMUNITIES}")
    
    reddit_df = download_file("reddit", community, as_dataframe=True)
    voat_df = download_file("voat", community, as_dataframe=True)
    
    if as_dataframe:
        return pd.concat([reddit_df, voat_df], ignore_index=True)
    else:
        reddit_file = download_file("reddit", community, output_dir=output_dir)
        voat_file = download_file("voat", community, output_dir=output_dir)
        return reddit_file, voat_file 