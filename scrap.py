"""
exemple du cript qui tourne sur mon EC2

"""
import requests, json, logging, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_pokemon_images():
    logger = logging.getLogger(__name__)
    url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
    
    try:
        Path('data').mkdir(exist_ok=True)
        
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; PokemonScraper/1.0)'})
        
        logger.info(f"Fetching: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pokemon_data = []
        
        for table in soup.find_all('table', class_='roundy'):
            for row in table.find_all('tr')[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    try:
                        number = cells[0].get_text(strip=True).replace('#', '')
                        img_tag = cells[1].find('img')
                        name = cells[2].get_text(strip=True)
                        
                        if img_tag and img_tag.get('src') and number.isdigit():
                            img_url = urljoin(url, img_tag['src'])
                            if img_url.startswith('http'):
                                pokemon_data.append({
                                    'number': int(number),
                                    'name': name,
                                    'image_url': img_url
                                })
                    except (IndexError, ValueError, AttributeError):
                        continue
        
        unique_pokemon = {}
        for pokemon in pokemon_data:
            num = pokemon['number']
            if num not in unique_pokemon:
                unique_pokemon[num] = pokemon
        
        result = sorted(unique_pokemon.values(), key=lambda x: x['number'])
        
        with open('data/pokemon_images.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        with open('data/pokemon_images.txt', 'w', encoding='utf-8') as f:
            for pokemon in result:
                f.write(f"{pokemon['image_url']}\n")
        
        logger.info(f"Success: {len(result)} Pokemon images scraped")
        return "OK"
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return "NOK"

def main():
    setup_logging()
    status = scrape_pokemon_images()
    return 0 if status == "OK" else 1

if __name__ == "__main__":
    exit(main())