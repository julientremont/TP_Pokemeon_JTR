# Pokemon Image Scraper & S3 Uploader

Script Python pour récupérer les liens ET télécharger les images Pokemon directement vers S3.

## Installation

### Environnement virtuel
```bash
sudo apt install python3.12-venv -y
python3 -m venv pokemon_env
source pokemon_env/bin/activate
pip install requests beautifulsoup4 lxml boto3
```


## Déploiement sur EC2 Ubuntu

```bash
# Connexion SSH
# Transfert du script
# Installation environnement
sudo apt install python3.12-venv -y
python3 -m venv pokemon_env
source pokemon_env/bin/activate
pip install requests beautifulsoup4 lxml boto3

# Configuration AWS (voir section Configuration AWS)

# Exécution
python3 pokemon_scraper.py
```

## Structure S3

Le script upload automatiquement vers le bucket `jtrpokemonbucket` :

### URLs et métadonnées
```
jtrpokemonbucket/pokemon/URL/pokemon_images.json
jtrpokemonbucket/pokemon/URL/pokemon_images.txt
```

### Images Pokemon
```
jtrpokemonbucket/pokemon/image/001_Bulbasaur.png
jtrpokemonbucket/pokemon/image/002_Ivysaur.png
jtrpokemonbucket/pokemon/image/003_Venusaur.png
...
```

## Permissions S3 Requises

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:HeadObject"
            ],
            "Resource": "arn:aws:s3:::jtrpokemonbucket/pokemon/*"
        }
    ]
}
```

## Fonctionnalités

### Phase 1 - Scraping et Upload URLs
- Extraction de 900+ liens Pokemon depuis Bulbapedia
- Déduplication automatique par numéro
- Tri par numéro de Pokédex
- Upload direct JSON + TXT vers S3

### Phase 2 - Téléchargement et Upload Images
- Téléchargement automatique des images
- Nommage intelligent : `001_Bulbasaur.png`
- Évite re-téléchargements (vérification S3)
- Upload direct vers S3 (pas de stockage local)
- Content-Type automatique selon extension
- Limite configurable (défaut: tous les Pokemon)

### Optimisations S3
- Streaming direct mémoire vers S3
- Vérification existence S3 avant téléchargement
- Content-Type automatique (image/png, image/jpeg, etc.)
- Pas de fichiers temporaires locaux
- Session HTTP réutilisée
- Gestion d'erreurs complète

## Vérification S3

```bash
# Lister les URLs uploadées
aws s3 ls s3://jtrpokemonbucket/pokemon/URL/

# Lister les images uploadées
aws s3 ls s3://jtrpokemonbucket/pokemon/image/

# Compter les images
aws s3 ls s3://jtrpokemonbucket/pokemon/image/ | wc -l

# Voir la taille totale
aws s3 ls s3://jtrpokemonbucket/pokemon/ --recursive --summarize
```
## Source
[Bulbapedia - Liste officielle des Pokemon](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number)
