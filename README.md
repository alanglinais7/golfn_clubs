# GolfN Clubs Data Management

This repository contains tools and scripts for managing golf club data, including brand information, club specifications, and associated images. The project focuses on data collection, cleaning, and organization for golf equipment information.

## Project Structure

```
.
├── brand_logos/           # Directory containing brand logo images
├── Archive/              # Archive directory for historical data
├── golfn_clubs_updated.xlsx  # Main database of golf clubs
├── golfn-app-brands.csv     # Brand information database
├── golfn_clubs.csv          # Raw club data
├── club_additions.xlsx      # Additional club data
├── extract_club_year.py     # Script to extract club years from images
├── brand_images.py         # Script to download and manage brand logos
├── club_cleaning.py        # Script for cleaning club data
├── brand_cleaning.py       # Script for cleaning brand data
├── conforming_clubs.py     # Script for managing conforming clubs
└── clubs_scraping_old.ipynb # Historical notebook for club data scraping
```

## Features

- **Club Data Management**: Comprehensive database of golf clubs with detailed specifications
- **Brand Management**: Organized collection of golf equipment brands with associated logos
- **Image Processing**: Automated tools for managing club and brand images
- **Data Cleaning**: Scripts for cleaning and standardizing club and brand information
- **Year Extraction**: Automated extraction of club manufacturing years from image metadata

## Setup

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install required dependencies:
```bash
pip install pandas openpyxl requests python-dotenv serpapi-python
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
(Only needed if you want to download club_images, which currently does not work)
```
SERPAPI_KEY=your_serpapi_key_here
```

## Usage

### Download all clubs from USGA
To ping the internal API and grab every club:
```bash
python conforming_clubs.py
```

### Club Year Extraction
To extract manufacturing years from club images:
```bash
python extract_club_year.py
```

### Data Cleaning
To clean club or brand data:
```bash
python club_cleaning.py
python brand_cleaning.py
```

## Data Files

- `golfn_clubs_updated.xlsx`: Main database containing comprehensive golf club information
- `golfn-app-brands.csv`: Database of golf equipment brands
- `golfn_clubs.csv`: Raw club data
- `club_additions.xlsx`: Additional club information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Contact

@alanglinais7 on Twitter/X