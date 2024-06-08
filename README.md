Titre du Projet : url_to_wordlist

## Description

Ce projet est un outil conçu pour générer une wordlist personnalisée à partir d'un site web donné. Cette wordlist est ensuite utilisée pour tenter de bruteforcer les répertoires de cette même application web en ciblant des mots-clés liés au site. L'objectif est d'améliorer l'efficacité et la pertinence des attaques de bruteforce en se concentrant sur des mots-clés spécifiques au site ciblé.

## Fonctionnalités

- **Extraction de mots-clés** : L'outil analyse le contenu du site web pour extraire les mots-clés les plus pertinents.
- **Génération de wordlist** : À partir des mots-clés extraits, l'outil génère une wordlist personnalisée.
- **Bruteforce de répertoires** : La wordlist générée est ensuite améliorée par l'IA pour ajouter des terminaisons aux mots, ajouter des synonymes ou des mots du même champ lexical.

## Prérequis

- Python 3.x
- Clé API Codestral (Pour la verion avec IA)

## Installation

1. Clonez le dépôt sur votre machine locale :

```bash
git clone https://github.com/NotCorpe/url_to_wordlist.git
```

2. Accédez au répertoire du projet :

```bash
cd url_to_wordlist
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Installer les modèles de langue SpaCy pour l'anglais et le français :

```bash
python -m spacy download en_core_web_sm
python -m spacy download fr_core_news_sm
#  Autre modèles de langue 
python -m spacy download de_core_news_sm
python -m spacy download es_core_news_sm
python -m spacy download it_core_news_sm
python -m spacy download pt_core_news_sm
python -m spacy download nl_core_news_sm
```

## Utilisation

1. Exécutez le script en fournissant l'URL du site web ciblé :

```bash
python url_to_wordlist.py --url https://exemple.com --language (en/fr/it/de)
```

2. Le script générera une wordlist dans le répertoire du projet.

3. Utilisez la wordlist générée pour tenter de bruteforcer les répertoires de l'application web ciblée.

## Contribution

Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

1. Fork du dépôt
2. Créez une branche pour votre fonctionnalité : `git checkout -b feature/nouvelle-fonctionnalité`
3. Commit de vos modifications : `git commit -m 'Ajout de la nouvelle fonctionnalité'`
4. Push vers la branche : `git push origin feature/nouvelle-fonctionnalité`
5. Ouvrez une pull request

## Licence

Ce projet est sous licence MIT. Pour plus de détails, veuillez consulter le fichier [LICENSE](LICENSE).
