import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict
import time

logger = logging.getLogger(__name__)

# Headers to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


class CarScraper:
    """Scrapes car listings from French car websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.timeout = 10
    
    def scrape_autoscout24(self, max_price: int) -> List[Dict]:
        """Scrape AutoScout24.fr for car listings."""
        try:
            from datetime import datetime
            current_year = datetime.now().year
            url = (
                f"https://www.autoscout24.fr/lst?"
                f"fuel=B%2CH"
                f"&pricefrom=0&priceto={max_price}"
                f"&fregfrom=2023&fregto={current_year}"
                f"&desc=1&size=20&page=1&fc=0&cy=F"
                f"&damaged_listing=exclude"
                f"&powertype=kw&sort=age"
            )
            
            response = self.session.get(url, headers=HEADERS, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            cars = []
            
            # AutoScout24 car listing selector
            listings = soup.find_all('a', {'class': 'ListItem_container__J_mHJ'})
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    link = listing.get('href')
                    if not link.startswith('http'):
                        link = 'https://www.autoscout24.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find('h2')
                    title = title_elem.text.strip() if title_elem else "Unknown Car"
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': 'Price_price__AjG_I'})
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    cars.append({
                        'source': 'AutoScout24',
                        'title': title,
                        'price': price,
                        'link': link
                    })
                except Exception as e:
                    logger.warning(f"Error parsing AutoScout24 listing: {e}")
                    continue
            
            logger.info(f"AutoScout24: Found {len(cars)} cars")
            return cars
            
        except Exception as e:
            logger.error(f"AutoScout24 scraping error: {e}")
            return []
    
    def scrape_leboncoin(self, max_price: int) -> List[Dict]:
        """Scrape Leboncoin.fr for car listings."""
        try:
            url = (
                f"https://www.leboncoin.fr/recherche?"
                f"category=2"
                f"&fuel=1"
                f"&price=min-{max_price}"
                f"&regdate=2023-max"
                f"&vehicle_damage=undamaged"
                f"&sort=time&order=desc"
            )
            
            response = self.session.get(url, headers=HEADERS, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            cars = []
            
            # Leboncoin car listing selector
            listings = soup.find_all('a', {'class': 'styles_cardContainer__LBqKX'})
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    link = listing.get('href')
                    if link and not link.startswith('http'):
                        link = 'https://www.leboncoin.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find('h3')
                    title = title_elem.text.strip() if title_elem else "Unknown Car"
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': 'styles_price__S6BVN'})
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    if link:
                        cars.append({
                            'source': 'Leboncoin',
                            'title': title,
                            'price': price,
                            'link': link
                        })
                except Exception as e:
                    logger.warning(f"Error parsing Leboncoin listing: {e}")
                    continue
            
            logger.info(f"Leboncoin: Found {len(cars)} cars")
            return cars
            
        except Exception as e:
            logger.error(f"Leboncoin scraping error: {e}")
            return []
    
    def scrape_lacentrale(self, max_price: int) -> List[Dict]:
        """Scrape LaCentrale.fr for car listings."""
        try:
            url = (
                f"https://www.lacentrale.fr/listing?"
                f"priceMax={max_price}"
                f"&yearMin=2023"
                f"&energies=essence%2Chybride"
                f"&damaged=non"
            )
            
            response = self.session.get(url, headers=HEADERS, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            cars = []
            
            # LaCentrale car listing selector
            listings = soup.find_all('a', {'class': 'adCard_adCard__link__CjXBA'})
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    link = listing.get('href')
                    if link and not link.startswith('http'):
                        link = 'https://www.lacentrale.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find('h3')
                    title = title_elem.text.strip() if title_elem else "Unknown Car"
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': 'price'})
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    if link:
                        cars.append({
                            'source': 'LaCentrale',
                            'title': title,
                            'price': price,
                            'link': link
                        })
                except Exception as e:
                    logger.warning(f"Error parsing LaCentrale listing: {e}")
                    continue
            
            logger.info(f"LaCentrale: Found {len(cars)} cars")
            return cars
            
        except Exception as e:
            logger.error(f"LaCentrale scraping error: {e}")
            return []
    
    def scrape_all(self, max_price: int) -> Dict[str, List[Dict]]:
        """Scrape all three websites."""
        results = {
            'autoscout24': self.scrape_autoscout24(max_price),
            'leboncoin': self.scrape_leboncoin(max_price),
            'lacentrale': self.scrape_lacentrale(max_price)
        }
        return results
