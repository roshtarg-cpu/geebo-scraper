"""
Geebo Scraper - Extract classifieds listings from Geebo.com
"""
from datetime import datetime, timezone
from apify import Actor
import httpx
from bs4 import BeautifulSoup
import re


async def main():
    async with Actor:
        Actor.log.info('Geebo Scraper starting...')
        
        # Get input
        actor_input = await Actor.get_input()
        if not actor_input:
            actor_input = {}
        
        # Get proxy configuration
        proxy_config = actor_input.get('proxyConfiguration', {})
        proxy_url = None
        if proxy_config and proxy_config.get('useApifyProxy'):
            # SDK 3.x: get proxy password from environment
            import os
            proxy_password = os.getenv('APIFY_PROXY_PASSWORD')
            if proxy_password:
                proxy_url = f'http://auto:{proxy_password}@proxy.apify.com:8000'
                Actor.log.info('Using Apify proxy')
        
        category = actor_input.get('category', 'jobs')
        location = actor_input.get('location', '')
        max_items = actor_input.get('maxItems', 10)
        
        Actor.log.info(f'Category: {category}, Location: {location}, Max: {max_items}')
        
        # Build URL - geebo.com/jobs-online/list/ works
        if category == 'jobs':
            base_url = 'https://geebo.com/jobs-online/list/'
        else:
            base_url = f'https://geebo.com/{category}/list/'
        
        results_count = 0
        
        try:
            # Fetch with httpx (with proxy if configured)
            Actor.log.info(f'Fetching {base_url}')
            
            client_kwargs = {
                'timeout': 30.0,
                'follow_redirects': True
            }
            if proxy_url:
                client_kwargs['proxies'] = {'http://': proxy_url, 'https://': proxy_url}
            
            async with httpx.AsyncClient(**client_kwargs) as client:
                response = await client.get(
                    base_url,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                
                Actor.log.info(f'HTTP {response.status_code}')
                
                if response.status_code != 200:
                    Actor.log.error(f'Failed to fetch: HTTP {response.status_code}')
                    return
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find job listings - geebo uses <table class="element">
                listings = soup.find_all('table', class_='element')
                
                Actor.log.info(f'Found {len(listings)} listings')
                
                for listing in listings[:max_items]:
                    if results_count >= max_items:
                        break
                    
                    try:
                        # Extract title - <a class="title">
                        title_elem = listing.find('a', class_='title')
                        title = title_elem.get_text().strip() if title_elem else None
                        if not title:
                            continue
                        
                        # Extract URL
                        url = title_elem['href'] if title_elem and title_elem.get('href') else None
                        
                        # Extract location - <span class="location">
                        location_elem = listing.find('span', class_='location')
                        job_location = location_elem.get_text().strip() if location_elem else None
                        
                        # Extract company - <div class="company">
                        company_elem = listing.find('div', class_='company')
                        company = company_elem.get_text().strip() if company_elem else None
                        
                        # Extract description - <div class="brief">
                        brief_elem = listing.find('div', class_='brief')
                        description = brief_elem.get_text().strip() if brief_elem else None
                        
                        # Clean up description (remove company if duplicated)
                        if description and company:
                            description = description.replace(company, '').strip()
                        
                        result = {
                            'url': url,
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'description': description,
                            'category': category,
                            'scrapedAt': datetime.now(timezone.utc).isoformat()
                        }
                        
                        await Actor.push_data(result)
                        results_count += 1
                        
                    except Exception as e:
                        Actor.log.error(f'Error processing listing: {e}')
                        continue
                
                Actor.log.info(f'Successfully scraped {results_count} items')
                
        except Exception as e:
            Actor.log.error(f'Failed to scrape: {e}')
            raise
