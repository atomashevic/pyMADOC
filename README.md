# pyMADOC

Python package to download and combine parts of MADOC dataset from [Zenodo](https://zenodo.org/records/14637314). The MADOC dataset contains social media posts from multiple platforms (Reddit, Voat, Bluesky, and Koo), making it easy to study cross-platform content and community dynamics.

## Features

- Easy download of platform-specific data files
- Automatic pairing of Reddit-Voat community data
- Both Python API and Command Line Interface
- Support for direct DataFrame loading
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

Mitrovic Dankulov, M., Tomašević, A., Maletic, S., Andjelkovic, M., Vranic, A., Cvetkovic, D., Stupovski, B., Vudragovic, D., Major, S., & Bogojević, A. (2025). MADOC: Multi-Platform Aggregated Dataset of Online Communities (1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14637314

Or BibTeX:

```
@MISC{mitrovicDankulov2025madoc,
  title     = "MADOC: Multi-Platform Aggregated Dataset of Online Communities",
  author    = "Mitrovic Dankulov, Marija and Tomašević, Aleksandar and Maletic,
               Slobodan and Andjelkovic, Miroslav and Vranic, Ana and Cvetkovic,
               Darja and Stupovski, Boris and Vudragovic, Dusan and Major, Sara
               and Bogojević, Aleksandar",
  publisher = "Zenodo",
  abstract  = "The Multi-platform Aggregated Dataset of Online Communities
               (MADOC) is a comprehensive dataset that facilitates computational
               social science research by providing a unified, standardized
               dataset for cross-platform analysis of online social dynamics.
               MADOC aggregates and standardizes data from four distinct
               platforms: Bluesky, Koo, Reddit, and Voat, spanning from 2012 to
               2024. The dataset includes 18.9 million posts, 236 million
               comments, and data from 23.1 million unique users across all
               platforms, with a particular focus on understanding community
               dynamics, user migration patterns, and the evolution of toxic
               behavior across platforms. By providing standardized data
               structures and FAIR-compliant access through Zenodo, MADOC
               enables researchers to conduct comparative analyses of user
               behavior, interaction networks, and content sentiment across
               diverse social media environments. The dataset's unique value
               lies in its cross-platform scope, standardized structure, and
               rich metadata, making it particularly suitable for studying
               societal phenomena such as community formation, toxic behavior
               propagation, and user migration patterns in response to platform
               moderation policies.",
  year      =  2025,
  url       = "https://zenodo.org/records/14637314",
  keywords  = "Social Media; Online Social Networking; Social Network Analysis",
  doi       = "10.5281/ZENODO.14637314"
}

```

## License

MIT License