import os
import requests
import json
import argparse
from bs4 import BeautifulSoup
import spacy
from collections import Counter
from urllib.parse import urljoin
from mistralai.client import MistralClient

class WebsiteSpider:
    def __init__(self, start_url, language, max_depth=3):
        self.start_url = start_url
        self.max_depth = max_depth
        self.language = language
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
        if self.language == 'fr':
            nlp = spacy.load("fr_core_news_sm")
        elif self.language == 'en':
            nlp = spacy.load("en_core_web_sm")
        else:
            print(f"Language '{self.language}' not supported.")
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

def get_enhanced_wordlist(wordlist, prompt):
    api_key = "y6wOHPVEwhFdEhU5el0l0JkutKpFskmL"
    client = MistralClient(api_key=api_key)
    model = "codestral-latest"
    response = client.completion(
        model=model,
        prompt=prompt,
        suffix=f"\n{wordlist}",
    )
    enhanced_wordlist = response.choices[0].message.content.split("\n")
    return enhanced_wordlist

def main():
    parser = argparse.ArgumentParser(description='Website Spider')
    parser.add_argument('--url', '-u', required=True, help='Start URL for the spider')
    parser.add_argument('--language', '-l', default='fr', help='Language of the website (default: fr)')
    args = parser.parse_args()
    start_url = args.url
    language = args.language
    max_depth = 2
    spider = WebsiteSpider(start_url, language, max_depth)
    spider.parse(start_url)
    spider.close()

    # Enhance the wordlist
    prompt = "Voici une liste de mots-clés scrapée sur le site : (site). Je souhaite utiliser cette liste de mots-clés pour bruteforcer les répertoires de ce site. Pour chaque mot de la liste, ajoute des variations, des synonymes ou des mots de la même famille et formate la liste pour pouvoir trouver des répertoires. Si il y'a une virgule dans un mot-clé, arrange-toi pour l'enlever pour que le mot-clé soit compatible avec le nom d'un potentiel répertoire."
    enhanced_keywords = get_enhanced_wordlist(spider.keywords, prompt)
    sorted_enhanced_keywords = sorted(set(enhanced_keywords))
    with open('enhanced_keywords.txt', 'w') as f:
        for keyword in sorted_enhanced_keywords:
            f.write(f"{keyword.replace(',', '')}\n")

if __name__ == '__main__':
    main()
