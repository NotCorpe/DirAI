import requests
import spacy
from bs4 import BeautifulSoup

def get_internal_links(url, domain_name):
    # Fonction pour récupérer les pages principal d'un site   
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return [link for link in links if link.startswith(f'https://{domain_name}') or link.startswith(f'http://{domain_name}')]

def extract_keywords_from_content(content):
    # Fonction pour extraire les mots clés à partir du contenu d'une page web, en utilisant spaCy
    nlp = spacy.load('en_core_web_sm')  # Charge le modèle de langue anglaise
    doc = nlp(content)  # Traite le contenu de la page web avec le modèle de langue
    keywords = [token.text for token in doc if token.is_alpha and token.is_stop != True and token.is_punct != True]  # Extrait les mots clés pertinents
    return keywords

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]  # Récupère l'URL en paramètre
    domain_name = url.split('//')[-1].split('/')[0]  # Extrait le nom de domaine de l'URL
    links = get_internal_links(url, domain_name)  # Récupère les liens internes de la première page

    # Récupère le contenu des pages web trouvées et extrait les mots clés pertinents
    all_keywords = []
    for link in links:
        print(link)
        try:
            response = requests.get(link)
            response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
            keywords = extract_keywords_from_content(content)
            all_keywords.extend(keywords)

    # Supprime les doublons et enregistre les mots clés pertinents dans un fichier
    keywords = list(set(all_keywords))
    with open('keywords.txt', 'w') as f:
        for keyword in keywords:
            f.write(f'{keyword}\n')

    print("Mots clés pertinents enregistrés dans le fichier 'keywords.txt'.")
