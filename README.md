# Pokemon Image Scraper & S3 Uploader

Script Python (120 lignes) pour récupérer les liens ET télécharger les images Pokemon directement vers S3.

## Installation

### Environnement virtuel
```bash
sudo apt install python3.12-venv -y
python3 -m venv pokemon_env
source pokemon_env/bin/activate
pip install requests beautifulsoup4 lxml boto3
```

### Configuration AWS
```bash
# Option A - Variables d'environnement
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Option B - AWS CLI (si installé)
aws configure

# Option C - IAM Role (si sur EC2)
# Attacher un rôle IAM avec permissions S3 à votre instance
```

## Déploiement

### Local
```bash
source pokemon_env/bin/activate
python3 pokemon_scraper.py
```

### EC2 Ubuntu
```bash
# Connexion SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Transfert du script
scp -i your-key.pem pokemon_scraper.py ubuntu@your-ec2-ip:~/

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

## Exemple d'exécution

```bash
2025-09-04 11:30:00 - INFO - Phase 1: Fetching Pokemon links
2025-09-04 11:30:02 - INFO - Phase 1 Success: 905 Pokemon links uploaded to S3
2025-09-04 11:30:02 - INFO - Phase 2: Downloading and uploading 905 Pokemon images to S3
2025-09-04 11:30:03 - INFO - SUCCESS 001_Bulbasaur.png (15234 bytes) uploaded to S3
2025-09-04 11:30:04 - INFO - SUCCESS 002_Ivysaur.png (18456 bytes) uploaded to S3
...
2025-09-04 11:45:00 - INFO - Phase 2 Complete: 905 uploaded to S3, 0 failed
2025-09-04 11:45:00 - INFO - Both phases completed successfully - All data in S3
```

## Dépannage

**Erreur AWS credentials**
```bash
# Vérifier la configuration
aws sts get-caller-identity

# Ou tester avec variables d'environnement
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**Erreur permissions S3**
```bash
# Tester l'accès au bucket
aws s3 ls s3://jtrpokemonbucket/pokemon/
```

**Erreur "bucket does not exist"**
Créer le bucket au préalable :
```bash
aws s3 mb s3://jtrpokemonbucket --region us-east-1
```

**CORRECTION - Erreur 404 S3 "Not Found"**
Version corrigée qui gère correctement la vérification d'existence des fichiers S3. L'erreur "An error occurred (404) when calling the HeadObject operation: Not Found" est maintenant résolue.

## Statut

- Script testé et fonctionnel sur EC2 avec rôle IAM
- Gestion d'erreur S3 corrigée (v1.1)
- Upload direct vers S3 sans stockage local
- 1025+ Pokemon téléchargés et uploadés avec succès

## Source
[Bulbapedia - Liste officielle des Pokemon](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number)