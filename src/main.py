"""
Geebo Scraper - Extract classifieds listings from Geebo.com
"""
from datetime import datetime, timezone
from apify import Actor
from camoufox.async_api import AsyncCamoufox
import re


async def main():
    async with Actor:
        Actor.log.info('Geebo Scraper starting...')
        
        # Get input
        actor_input = await Actor.get_input()
        if not actor_input:
            actor_input = {}
        
        category = actor_input.get('category', 'jobs')
        location = actor_input.get('location', 'New York')
        min_price = actor_input.get('minPrice', 0)
        max_price = actor_input.get('maxPrice', 999999)
        max_results = actor_input.get('maxResults', 3)
        proxy_config = actor_input.get('proxyConfiguration', {
            'useApifyProxy': True,
            'apifyProxyGroups': ['RESIDENTIAL']
        })
        
        Actor.log.info(f'Category: {category}, Location: {location}, Max: {max_results}')
        
        # Get proxy configuration for Camoufox
        proxy_config_dict = None
        if proxy_config and proxy_config.get('useApifyProxy'):
            proxy_password = Actor.config.proxy_password
            if proxy_password:
                proxy_config_dict = {
                    'server': 'http://proxy.apify.com:8000',
                    'username': 'auto',
                    'password': proxy_password
                }
        
        # Build search URL - Geebo uses simple URL structure
        location_slug = location.lower().replace(' ', '-').replace(',', '')
        category_slug = category.lower().replace(' ', '-')
        search_url = f'https://www.geebo.com/{location_slug}/{category_slug}'
        
        Actor.log.info(f'Search URL: {search_url}')
        
        results_count = 0
        
        # Launch browser with Camoufox
        async with AsyncCamoufox(
            headless=True,
            proxy=proxy_config_dict
        ) as browser:
            page = await browser.new_page()
            
            try:
                await page.goto(search_url, timeout=60000)
                await page.wait_for_timeout(3000)
                
                # Extract listings using multiple selector strategies
                listings = await page.query_selector_all('article')
                if not listings:
                    listings = await page.query_selector_all('div[class*="listing"]')
                if not listings:
                    listings = await page.query_selector_all('div[class*="item"]')
                if not listings:
                    listings = await page.query_selector_all('li')
                
                Actor.log.info(f'Found {len(listings)} potential listings')
                
                for listing in listings[:max_results]:
                    if results_count >= max_results:
                        break
                    
                    try:
                        # Extract title
                        title_elem = await listing.query_selector('h1, h2, h3, h4, a')
                        title = await title_elem.inner_text() if title_elem else None
                        if not title:
                            continue
                        title = title.strip()
                        
                        # Extract URL
                        link_elem = await listing.query_selector('a[href]')
                        url = await link_elem.get_attribute('href') if link_elem else None
                        if url and not url.startswith('http'):
                            url = f'https://www.geebo.com{url}'
                        
                        # Extract price
                        price_text = await listing.inner_text()
                        price_match = re.search(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)', price_text)
                        price = price_match.group(0) if price_match else None
                        
                        # Extract location
                        loc_elem = await listing.query_selector('[class*="location"], [class*="city"]')
                        loc = await loc_elem.inner_text() if loc_elem else location
                        
                        # Extract description
                        desc_elem = await listing.query_selector('p')
                        description = await desc_elem.inner_text() if desc_elem else None
                        if description:
                            description = description.strip()[:500]
                        
                        # Extract image
                        img_elem = await listing.query_selector('img[src]')
                        image = await img_elem.get_attribute('src') if img_elem else None
                        if image and not image.startswith('http'):
                            if image.startswith('//'):
                                image = f'https:{image}'
                            elif image.startswith('/'):
                                image = f'https://www.geebo.com{image}'
                        
                        # Build result
                        result = {
                            'url': url or search_url,
                            'title': title,
                            'price': price,
                            'currency': 'USD' if price else None,
                            'location': loc.strip() if loc else None,
                            'description': description,
                            'image': image,
                            'category': category,
                            'scrapedAt': datetime.now(timezone.utc).isoformat()
                        }
                        
                        # Push result immediately
                        await Actor.push_data(result)
                        results_count += 1
                        Actor.log.info(f'Scraped: {title[:50]}')
                        
                    except Exception as e:
                        Actor.log.warning(f'Failed to extract listing: {e}')
                        continue
                
            except Exception as e:
                Actor.log.error(f'Error during scraping: {e}')
            
            finally:
                await page.close()
        
        Actor.log.info(f'Scraping completed. Total items: {results_count}')
        
        # Save task metadata
        env = Actor.get_env()
        await Actor.set_value('SAVED-TASK', {
            'actorId': env.get('actor_id'),
            'actorRunId': env.get('actor_run_id'),
            'defaultDatasetId': env.get('default_dataset_id'),
            'startedAt': env.get('started_at'),
            'input': actor_input,
            'stats': {'itemsScraped': results_count}
        })
