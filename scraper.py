import requests
from bs4 import BeautifulSoup
import logging
import os
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

# Enhanced headers to avoid being blocked (French user)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cache-Control': 'max-age=0',
}

# Check if scraper APIs are available
SCRAPINGBEE_API_KEY = os.environ.get("SCRAPINGBEE_API_KEY")
SCRAPERAPI_KEY = os.environ.get("SCRAPERAPI_KEY")

if SCRAPINGBEE_API_KEY:
    logger.info("✅ ScrapingBee API enabled - Tier 1 (Primary)")
if SCRAPERAPI_KEY:
    logger.info("✅ ScraperAPI enabled - Tier 2 (Fallback)")
if not SCRAPINGBEE_API_KEY and not SCRAPERAPI_KEY:
    logger.info("⚠️ No scraper APIs configured - Using basic scraper (limited)")


class CarScraper:
    """Scrapes car listings from French car websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.timeout = 10
        self.scrapingbee_key = SCRAPINGBEE_API_KEY
        self.scraperapi_key = SCRAPERAPI_KEY
        self.scrapingbee_base = "https://api.scrapingbee.com/api/v1"
        self.scraperapi_base = "https://api.scraperapi.com"
    
    def _scrape_with_scrapingbee(self, url: str, site_name: str) -> str:
        """Scrape using ScrapingBee API (Tier 1)."""
        try:
            response = requests.get(
                self.scrapingbee_base,
                params={
                    'api_key': self.scrapingbee_key,
                    'url': url,
                    'render_js': 'true',  # Handle JavaScript
                    'timeout': 30000
                },
                timeout=40
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {site_name}: ScrapingBee API successful")
                return response.content
            else:
                logger.warning(f"⚠️ {site_name}: ScrapingBee returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ {site_name}: ScrapingBee error: {e}")
            return None
    
    def _scrape_with_scraperapi(self, url: str, site_name: str) -> str:
        """Scrape using ScraperAPI (Tier 2 - Fallback)."""
        try:
            response = requests.get(
                self.scraperapi_base,
                params={
                    'api_key': self.scraperapi_key,
                    'url': url,
                    'render': 'true',  # Handle JavaScript
                    'premium': 'true',  # Use premium proxy for anti-bot sites
                    'device_type': 'desktop'  # Desktop user agent
                },
                timeout=90  # Increased from 40s to 90s for heavy JS sites
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {site_name}: ScraperAPI successful")
                return response.content
            else:
                logger.warning(f"⚠️ {site_name}: ScraperAPI returned status {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"⚠️ {site_name}: ScraperAPI timeout (90s) - too many JS requests")
            return None
        except Exception as e:
            logger.error(f"❌ {site_name}: ScraperAPI error: {e}")
            return None
    
    def _scrape_basic(self, url: str, site_name: str) -> str:
        """Scrape using basic requests with enhanced headers (Tier 3 - Last resort)."""
        try:
            # Add referrer based on site
            headers = HEADERS.copy()
            if 'autoscout24' in url:
                headers['Referer'] = 'https://www.autoscout24.fr/'
            elif 'leboncoin' in url:
                headers['Referer'] = 'https://www.leboncoin.fr/'
            elif 'lacentrale' in url:
                headers['Referer'] = 'https://www.lacentrale.fr/'
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"✅ {site_name}: Basic scraper successful")
            return response.content
            
        except Exception as e:
            logger.error(f"❌ {site_name}: Basic scraper error: {e}")
            return None
    
    def _get_html(self, url: str, site_name: str) -> str:
        """Get HTML using API tiers: ScrapingBee -> ScraperAPI -> Basic Scraper."""
        # Tier 1: Try ScrapingBee API
        if self.scrapingbee_key:
            html = self._scrape_with_scrapingbee(url, site_name)
            if html:
                return html
            logger.warning(f"⚠️ {site_name}: ScrapingBee failed, trying ScraperAPI...")
        
        # Tier 2: Try ScraperAPI
        if self.scraperapi_key:
            html = self._scrape_with_scraperapi(url, site_name)
            if html:
                return html
            logger.warning(f"⚠️ {site_name}: ScraperAPI failed, falling back to basic scraper...")
        
        # Tier 3: Fall back to basic scraper
        return self._scrape_basic(url, site_name)
    
    def _find_listings_resilient(self, soup: BeautifulSoup, site_name: str) -> List:
        """Find listings with resilient selectors that handle CSS changes."""
        listings = []
        
        if site_name == "AutoScout24":
            # Try primary selector (current hashed class)
            listings = soup.find_all('a', {'class': 'ListItem_container__J_mHJ'})
            if listings:
                return listings
            
            # Try by data-testid attribute
            listings = soup.find_all('a', {'data-testid': 'result-item'})
            if listings:
                return listings
            
            # Try by partial class match
            listings = soup.find_all('a', {'class': lambda x: x and 'ListItem' in x})
            if listings:
                return listings
            
            # Try article tag with listing class
            listings = soup.find_all('article', {'class': lambda x: x and 'listing' in x.lower()})
            if listings:
                return listings
            
            # Last resort: find all links with href containing listing IDs
            all_links = soup.find_all('a', href=lambda x: x and 'autoscout24.fr' in x)
            if all_links:
                return all_links[:20]
        
        elif site_name == "Leboncoin":
            # Try by data-testid
            listings = soup.find_all('a', {'data-testid': 'adCard_adCard__link__CjXBA'})
            if listings:
                return listings
            
            # Try by class containing 'card'
            listings = soup.find_all('a', {'class': lambda x: x and 'card' in x})
            if listings:
                return listings
            
            # Try item class
            listings = soup.find_all('div', {'class': lambda x: x and 'item' in x.lower()})
            if listings:
                return listings
            
            # Try article tag
            listings = soup.find_all('article')
            if listings:
                return listings
        
        elif site_name == "LaCentrale":
            # Try by class containing 'ad'
            listings = soup.find_all('a', {'class': lambda x: x and 'ad' in x})
            if listings:
                return listings
            
            # Try by card class
            listings = soup.find_all('div', {'class': lambda x: x and 'card' in x})
            if listings:
                return listings
            
            # Try listing wrapper
            listings = soup.find_all('div', {'class': lambda x: x and 'listing' in x.lower()})
            if listings:
                return listings
            
            # Try article tag
            listings = soup.find_all('article')
            if listings:
                return listings
        
        return listings
    
    def scrape_autoscout24(self, max_price: int) -> List[Dict]:
        """Scrape AutoScout24.fr for car listings."""
        try:
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
            
            html = self._get_html(url, "AutoScout24")
            if not html:
                logger.warning("AutoScout24: Failed to retrieve HTML")
                return []
            
            soup = BeautifulSoup(html, 'lxml')
            cars = []
            
            # Use resilient selector logic
            listings = self._find_listings_resilient(soup, "AutoScout24")
            logger.info(f"AutoScout24: Found {len(listings)} potential listings")
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    link = listing.get('href')
                    if not link:
                        continue
                    if not link.startswith('http'):
                        link = 'https://www.autoscout24.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find('h2')
                    if not title_elem:
                        title_elem = listing.find('a')
                    if not title_elem:
                        # Try to get from any text content
                        title = listing.get_text(strip=True)[:100]
                    else:
                        title = title_elem.text.strip()
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': lambda x: x and 'Price' in x})
                    if not price_elem:
                        # Try to find price in any span
                        price_elem = listing.find('span', string=lambda x: x and '€' in str(x))
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    if title and title != "Unknown Car":
                        cars.append({
                            'source': 'AutoScout24',
                            'title': title,
                            'price': price,
                            'link': link
                        })
                except Exception as e:
                    logger.warning(f"Error parsing AutoScout24 listing: {e}")
                    continue
            
            logger.info(f"AutoScout24: Successfully extracted {len(cars)} cars")
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
            
            html = self._get_html(url, "Leboncoin")
            if not html:
                logger.warning("Leboncoin: Failed to retrieve HTML")
                return []
            
            soup = BeautifulSoup(html, 'lxml')
            cars = []
            
            # Use resilient selector logic
            listings = self._find_listings_resilient(soup, "Leboncoin")
            logger.info(f"Leboncoin: Found {len(listings)} potential listings")
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    # Try to find link
                    link = None
                    if listing.name == 'a':
                        link = listing.get('href')
                    else:
                        link_elem = listing.find('a')
                        link = link_elem.get('href') if link_elem else None
                    
                    if not link:
                        link = listing.get('href')
                    
                    if link and not link.startswith('http'):
                        link = 'https://www.leboncoin.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find(['h2', 'h3', 'a'])
                    if not title_elem:
                        title = listing.get_text(strip=True)[:100]
                    else:
                        title = title_elem.text.strip()
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': lambda x: x and 'price' in x.lower()})
                    if not price_elem:
                        price_elem = listing.find(string=lambda x: x and '€' in str(x))
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    if link and title and title != "Unknown Car":
                        cars.append({
                            'source': 'Leboncoin',
                            'title': title,
                            'price': price,
                            'link': link
                        })
                except Exception as e:
                    logger.warning(f"Error parsing Leboncoin listing: {e}")
                    continue
            
            logger.info(f"Leboncoin: Successfully extracted {len(cars)} cars")
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
            
            html = self._get_html(url, "LaCentrale")
            if not html:
                logger.warning("LaCentrale: Failed to retrieve HTML")
                return []
            
            soup = BeautifulSoup(html, 'lxml')
            cars = []
            
            # Use resilient selector logic
            listings = self._find_listings_resilient(soup, "LaCentrale")
            logger.info(f"LaCentrale: Found {len(listings)} potential listings")
            
            for listing in listings[:10]:  # Limit to 10 results
                try:
                    link = None
                    if listing.name == 'a':
                        link = listing.get('href')
                    else:
                        link_elem = listing.find('a')
                        link = link_elem.get('href') if link_elem else None
                    
                    if not link:
                        link = listing.get('href')
                    
                    if link and not link.startswith('http'):
                        link = 'https://www.lacentrale.fr' + link
                    
                    # Extract car title
                    title_elem = listing.find(['h2', 'h3', 'a'])
                    if not title_elem:
                        title = listing.get_text(strip=True)[:100]
                    else:
                        title = title_elem.text.strip()
                    
                    # Extract price
                    price_elem = listing.find('span', {'class': lambda x: x and 'price' in x.lower()})
                    if not price_elem:
                        price_elem = listing.find(string=lambda x: x and '€' in str(x))
                    price = price_elem.text.strip() if price_elem else "N/A"
                    
                    if link and title and title != "Unknown Car":
                        cars.append({
                            'source': 'LaCentrale',
                            'title': title,
                            'price': price,
                            'link': link
                        })
                except Exception as e:
                    logger.warning(f"Error parsing LaCentrale listing: {e}")
                    continue
            
            logger.info(f"LaCentrale: Successfully extracted {len(cars)} cars")
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
