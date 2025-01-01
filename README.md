# Shopify Store Scraper

A Python script to scrape product data from Shopify stores. This tool allows you to extract product information from multiple collections and save it to a CSV file.

## Features

- Extract products from multiple Shopify store collections
- Save product data to CSV format
- Support for multiple collections from different stores
- Handles pagination automatically
- Prevents duplicate products

## Installation

1. Clone this repository:

```bash
git clone https://github.com/bangadam/scraper-shopify.git
cd scraper-shopify
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

To scrape products from a single store:

```bash
python shopify.py https://example-store.com
```

### Scrape Specific Collections

To scrape products from specific collections:

```bash
python shopify.py -c "https://store1.com/collections/summer,https://store1.com/collections/winter"
```

### List Available Collections

To see all available collections in a store:

```bash
python shopify.py --list-collections https://example-store.com
```

## Output Format

The script generates a `products.csv` file with the following columns:

- Code: Product handle/slug
- Title: Collection title
- Category: Product category
- Name: Product name
- Variant Name: Variant title
- Price: Product price
- In Stock: Availability status
- URL: Product URL

## Notes

- Respects rate limiting and includes retry logic
- Uses User-Agent headers to avoid blocking
- Skips duplicate products based on variant ID

## License

MIT License

## Contributing

Feel free to open issues and pull requests for any improvements.
