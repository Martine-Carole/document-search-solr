import requests
from bs4 import BeautifulSoup
import json
import os


# Function to extract results from a Google Scholar page
def extract_results(page_number) :
    url = f"https://scholar.google.com/scholar?start={page_number * 10}&q=green+shipping&hl=fr&as_sdt=0,5"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Store raw HTML content
    raw_html_path = f'raw_data_page_{page_number + 1}.html'
    with open(raw_html_path, 'w', encoding='utf-8') as raw_file :
        raw_file.write(response.text)

    results = []
    for item in soup.select('.gs_ri') :
        title = item.select_one('.gs_rt').get_text()
        snippet = item.select_one('.gs_rs').get_text()

        # Prepare the entry for JSONL
        entry = {
            "prompt" : title,
            "completion" : snippet
        }
        results.append(entry)

    return results


# Loop over multiple pages
all_data = []
for page in range(10) :
    print(f"Extracting page {page + 1}...")
    page_data = extract_results(page)
    all_data.extend(page_data)

# Save the processed results in JSON Lines format
with open('training_data.jsonl', 'w', encoding='utf-8') as f :
    for entry in all_data :
        f.write(json.dumps(entry) + '\n')

print("Data extraction complete. Raw data and processed data saved.")
