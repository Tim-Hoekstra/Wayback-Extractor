import requests
from tqdm import tqdm
import argparse
import sys
import concurrent.futures
# Check if an argument is passed
if len(sys.argv) < 2:
    print("Please provide a target URL as an argument.")
    print("Example: python validate.py www.example.com")
    sys.exit(1)

# Create an argument parser
parser = argparse.ArgumentParser(description='URL Validation Tool')

# Add the target URL argument
parser.add_argument('-u', '--url', metavar='URL', type=str, help='Target URL to validate')

# Add an optional output file argument
parser.add_argument('-o', '--output', metavar='FILE', type=str, help='Output file to save valid URLs')

# Add an optional output file argument
parser.add_argument('-t', '--threads', metavar='FILE', type=str, help='How many threads to use for processing URLs')

# Parse the command line arguments
args = parser.parse_args()

target = args.url
output_file = args.output
threads = int(args.threads)

url = f'http://web.archive.org/cdx/search/cdx?url={target}&output=json'

response = requests.get(url)
data = response.json()

item_list = [item[2] for item in data[1:]]
item_list = list(set(item_list))
print(item_list)
exit(0)
def check_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return url

# Create a list to store the valid URLs
valid_urls = []

# Use concurrent.futures to process the URLs concurrently with 5 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
    # Submit the URL checking tasks to the executor
    futures = [executor.submit(check_url, url) for url in item_list]

    # Use tqdm to track the progress of the futures
    with tqdm(total=len(futures), desc="Processing URLs") as pbar:
        # Iterate over the completed futures
        for future in concurrent.futures.as_completed(futures):
            # Get the result from the future
            result = future.result()
            if result:
                valid_urls.append(result)
                print("\033[92m[+]\033[0m", result)
            pbar.update(1)  # Update the progress bar

# Save the valid URLs to a file if output file is provided
if output_file:
    with open(output_file, "w") as file:
        for url in valid_urls:
            file.write(url + "\n")

    print("Valid URLs saved to", output_file)
