import requests
from bs4 import BeautifulSoup
import json

# Base URL for Google Scholar search
base_url = "https://scholar.google.com/scholar?start={}&q=green+shipping&hl=fr&as_sdt=0,5"

# Initialize a list to hold training data
training_data = []

# Loop through the first 10 pages (adjust the range as needed)
for page in range(0, 10):  # 0, 10, 20, ..., 90
    # Construct the full URL
    url = base_url.format(page)
    print(f"Fetching: {url}")

    # Send the request and get the response
    response = requests.get(url)

    # Check for request success
    if response.status_code != 200:
        print(f"Failed to fetch page {page // 10 + 1}. Status code: {response.status_code}")
        continue

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the articles (this may vary based on Google Scholar's HTML structure)
    articles = soup.find_all('div', class_='gs_ri')

    for article in articles:
        # Extract the title and snippet/summary of the article
        title = article.find('h3', class_='gs_rt').text
        snippet = article.find('div', class_='gs_rs').text

        # Create a JSON object in the required format
        training_data.append({
            "prompt": f"What is the article titled '{title}' about?",
            "completion": snippet
        })

# Write to a JSON Lines file
with open('training_data.jsonl', 'w', encoding='utf-8') as f:
    for entry in training_data:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

print("Data extraction complete. Training data saved to 'training_data.jsonl'.")
