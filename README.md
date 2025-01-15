# pyMADOC

Python package to download and combine parts of MADOC dataset from Zenodo (record: 14637314). The MADOC dataset contains social media posts from multiple platforms (Reddit, Voat, Bluesky, and Koo), making it easy to study cross-platform content and community dynamics.

## Features

- Easy download of platform-specific data files
- Automatic pairing of Reddit-Voat community data
- Both Python API and Command Line Interface
- Support for direct DataFrame loading
- Progress bars for downloads
- Efficient parquet file format

## Installation

```bash
pip install pymadoc
```

## Usage

### As a Python Package

```python
from pymadoc import list_available_data, download_file, download_community_pair

# List available platforms and communities
data_info = list_available_data()
print(data_info["platforms"])  # ['reddit', 'voat', 'bluesky', 'koo']
print(data_info["communities"])  # ['CringeAnarchy', 'fatpeoplehate', ...]

# Download a specific file
# For Reddit/Voat, specify both platform and community
file_path = download_file("reddit", community="funny", output_dir="data")
# For Bluesky/Koo, specify only platform
file_path = download_file("bluesky", output_dir="data")

# Load directly as DataFrame
df = download_file("reddit", community="funny", as_dataframeTrue)

# Download and combine Reddit-Voat community pair
# As files
reddit_file, voat_file = download_community_pair("funny", output_dir="data")
# As combined DataFrame
combined_df = download_community_pair("funny", as_dataframe=True)
```

### Command Line Interface

List available platforms and communities:
```bash
pymadoc list
```

Download a specific file:
```bash
# Reddit/Voat (requires community)
pymadoc download reddit --community funny --output-dir data
# Bluesky/Koo
pymadoc download bluesky --output-dir data
```

Download Reddit-Voat community pair:
```bash
pymadoc pair funny --output-dir data
```

## Available Data

### Platforms
- Reddit: Community-specific posts and comments
- Voat: Community-specific posts and comments
- Bluesky: Platform-wide posts
- Koo: Platform-wide posts

### Communities (Reddit/Voat only)
- CringeAnarchy
- fatpeoplehate
- funny
- gaming
- gifs
- greatawakening
- KotakuInAction
- MensRights
- milliondollarextreme
- pics
- technology
- videos

## Data Format

All files are stored in parquet format for efficient storage and fast loading. Each file contains the following columns:
- Platform-specific post/comment IDs
- Content text
- Timestamps
- User information
- Engagement metrics

## Requirements

- Python 3.6 or higher
- pandas
- requests
- tqdm

## Citation

If you use this package or the MADOC dataset in your research, please cite:
```
@dataset{madoc_dataset,
    title = {MADOC: Multi-platform Archive of Digital Online Content},
    author = {Tomašević, Aleksandar},
    year = {2024},
    publisher = {Zenodo},
    doi = {10.5281/zenodo.14637314}
}
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
