import requests
from bs4 import BeautifulSoup
import spacy
import langdetect
from collections import Counter
from urllib.parse import urljoin
import argparse

class WebsiteSpider:
    def __init__(self, start_url, api_key, max_depth=3):
        self.start_url = start_url
        self.max_depth = max_depth
        self.api_key = api_key
        self.total_words = 0
        self.keywords = []
        self.visited_urls = set()

    def parse(self, url, depth=0):
        if depth > self.max_depth:
            return

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        self.total_words += len(text.split())
        print(f"Number of words found on {url}: {len(text.split())}")

        language = langdetect.detect(text)

        if language == 'fr':
            nlp = spacy.load("fr_core_news_sm")
        elif language == 'en':
            nlp = spacy.load("en_core_web_sm")
        else:
            return

        doc = nlp(text)
        words = [token.text for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        word_counts = Counter(words)
        self.keywords.extend(word_counts.keys())

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith(self.start_url):
                url = urljoin(self.start_url, href)
                if url not in self.visited_urls:
                    self.visited_urls.add(url)
                    self.parse(url, depth + 1)

    def close(self):
        print(f"Total number of words found: {self.total_words}")
        print(f"Total number of keywords extracted: {len(self.keywords)}")

        sorted_keywords = sorted(set(self.keywords))

        with open('keywords.txt', 'w') as f:
            for keyword in sorted_keywords:
                f.write(f"{keyword}\n")

        print("Visited pages:")
        for url in self.visited_urls:
            print(url)

def main():
    parser = argparse.ArgumentParser(description='Website Spider')
    parser.add_argument('--url', '-u', required=True, help='Start URL for the spider')
    args = parser.parse_args()

    start_url = args.url
    max_depth = 2

    with open('api_key.txt', 'r') as f:
        api_key = f.read().strip()

    spider = WebsiteSpider(start_url, api_key, max_depth)
    spider.parse(start_url)
    spider.close()

if __name__ == '__main__':
    main()
