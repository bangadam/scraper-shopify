import csv
import json 
import time
import urllib.request
from urllib.error import HTTPError
from optparse import OptionParser

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

def fix_url(url):
    fixed_url = url.strip()
    if not fixed_url.startswith('http://') and \
        not fixed_url.startswith('https://'):
        fixed_url = 'http://' + fixed_url
    
    return fixed_url.rstrip('/')

def get_page_collections(url):
    full_url = url + '/collections.json'
    page = 1
    while True:
        req = urllib.request.Request(
            full_url + '?page={}'.format(page), 
            data=None,
            headers={'User-Agent': USER_AGENT}
        )
        while True:
            try:
                data = urllib.request.urlopen(req).read()
                break
            except HTTPError as e:
                print('Error: ', e)
                time.sleep(5)
                print('Retrying...')
        
        cols = json.loads(data.decode())['collections']
        if not cols:
            break
        for col in cols:
            yield col
        page += 1

def check_shopify(url):
    try:
        get_page(url, 1)
        return True
    except HTTPError as e:
        return False
    
def get_page(url, page, collection_handle=None):
    full_url = url
    if collection_handle:
        full_url = url + '/collections/{}'.format(collection_handle)
    full_url += '/products.json'
    req = urllib.request.Request(
        full_url + '?page={}'.format(page), 
        data=None,
        headers={'User-Agent': USER_AGENT}
    )
    while True:
        try:
            data = urllib.request.urlopen(req).read()
            break
        except HTTPError as e:
            print('Error: ', e)
            time.sleep(5)
            print('Retrying...')
    
    products = json.loads(data.decode())['products']
    return products

def extract_product_collection(url, col):
    page = 1
    products = get_page(url, page, col)
    while products:
        for product in products:
            yield product
        page += 1
        products = get_page(url, page, col)

def get_base_url(url):
    # Remove path components to get base URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def extract_products_from_urls(collection_urls, output_path):
    with open(output_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Code", "Title", "Category", "Name", "Variant Name", "Price", "In Stock", "URL"])
        seen_variants = set()
        
        for collection_url in collection_urls:
            base_url = get_base_url(collection_url)
            if not check_shopify(base_url):
                print(f"Not a Shopify store: {base_url}")
                continue
                
            for col in get_page_collections(base_url):
                handle = col['handle']
                title = col['title']
                for product in extract_product_collection(base_url, handle):
                    variant_id = product['id']
                    if variant_id in seen_variants:
                        continue
                    
                    seen_variants.add(variant_id)
                    code = product['handle']
                    name = product['title']
                    category = title
                    price = product['variants'][0]['price']
                    in_stock = product['variants'][0]['available']
                    variant_name = product['variants'][0]['title']
                    product_url = base_url + '/products/' + code
                    writer.writerow([code, title, category, name, variant_name, price, in_stock, product_url])

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        '--list-collections', 
        dest='list_collections', 
        action='store_true', 
        help='List all collections',
        default=False
    )
    
    parser.add_option(
        "--collections",
        '-c',
        dest='collections',
        default=None,
        help="download products from collections (comma-separated URLs)"
    )
    
    (options, args) = parser.parse_args()
    if len(args) > 0:
        if options.list_collections:
            url = fix_url(args[0])
            for col in get_page_collections(url):
                print(col['handle'])
        else:
            collection_urls = []
            if options.collections:
                collection_urls = [fix_url(url) for url in options.collections.split(',')]
            else:
                collection_urls = [fix_url(args[0])]
            extract_products_from_urls(collection_urls, "products.csv")

