import requests
from bs4 import BeautifulSoup
import csv

# List of URLs dynamically generated for pages 1 to 28
# The link is changeable!
URL = [f"https://jplang.tufs.ac.jp/en/nw/{i}/{i}.html" for i in range(1, 29)]

# Open the CSV file to write the scraped data
with open('', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Word", "Kanji", "Translation"])  # Write header row

    # Loop through each URL
    for url in URL:
        page = requests.get(url)

        # Check if the request was successful
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="content")

            # Find all vocab lists on the page
            vocab_lists = results.find_all("ul", class_="new_word_list list-group")

            # Loop through each 'ul' element containing vocabulary
            for vocab_list in vocab_lists:
                vocab_items = vocab_list.find_all("li")

                # Loop through each word entry in 'li'
                for vocab in vocab_items:
                    word = vocab.find("span", class_="word")
                    kanji = vocab.find("span", class_="kanji")
                    translation = vocab.find("span", class_="translation")

                    # Handle cases where word, kanji, or translation might not be available
                    word_text = word.text.strip() if word else "N/A"
                    kanji_text = kanji.text.strip() if kanji else "N/A"
                    translation_text = translation.text.strip() if translation else "N/A"

                    # Write the word, kanji, and translation to the CSV
                    writer.writerow([word_text, kanji_text, translation_text])

        else:
            # Print an error message if the page couldn't be retrieved
            print(f"Failed to retrieve page: {url} (Status code: {page.status_code})")
