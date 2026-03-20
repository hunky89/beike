import random
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# Configuration
BASE_URL = "https://xa.ke.com/ershoufang/pg{}/"
MAX_PAGES = 50  # Adjust as needed
OUTPUT_FILE = "xian_ershoufang_playwright.csv"

def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))

def simulate_human_behavior(page):
    """
    Simulates human behavior like scrolling and mouse movements.
    """
    # Random mouse movement
    page.mouse.move(random.randint(0, 500), random.randint(0, 500))
    random_sleep(0.5, 1.5)
    
    # Scroll down slowly
    for _ in range(5):
        page.mouse.wheel(0, random.randint(100, 300))
        random_sleep(0.5, 1.5)
    
    # Scroll back up a bit
    page.mouse.wheel(0, -random.randint(50, 150))
    random_sleep(0.5, 1)

def run():
    with sync_playwright() as p:
        print("Launching browser...")
        # Launch browser in headful mode
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        
        # Anti-detection script
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        all_data = []
        
        print("Starting crawler...")
        
        for page_num in range(1, MAX_PAGES + 1):
            url = BASE_URL.format(page_num)
            print(f"Navigating to page {page_num}: {url}")
            
            try:
                # Add referer if not first page
                if page_num > 1:
                    page.set_extra_http_headers({
                        "Referer": BASE_URL.format(page_num - 1)
                    })
                
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Simulate human behavior immediately after load
                simulate_human_behavior(page)
                
                # Check for CAPTCHA
                if "验证" in page.title() or "CAPTCHA" in page.content():
                    print("⚠️ CAPTCHA detected!")
                    print("Please manually solve the CAPTCHA in the browser window.")
                    print("The script will check every 5 seconds if the CAPTCHA is resolved...")
                    
                    while "验证" in page.title() or "CAPTCHA" in page.content():
                        time.sleep(5)
                        if "验证" not in page.title() and "CAPTCHA" not in page.content():
                            print("CAPTCHA resolved! Resuming...")
                            break
                        print("Waiting for CAPTCHA resolution...")
                
                # Check for Login
                if "登录" in page.title():
                    print("⚠️ Login required. Please login manually.")
                    while "登录" in page.title():
                        time.sleep(5)
                        if "登录" not in page.title():
                            print("Login successful! Resuming...")
                            break
                        print("Waiting for Login...")

                # Wait for the list to be visible
                try:
                    page.wait_for_selector(".sellListContent", timeout=10000)
                except:
                    print("List content not found. Checking for no results...")
                    if page.locator(".m-no-result").count() > 0:
                        print("No more results found. Ending crawler.")
                        break
                    print("Unknown error or empty page. Retrying page...")
                    continue

                # Extract data
                listings = page.locator(".info.clear").all()
                print(f"Found {len(listings)} listings on page {page_num}.")
                
                for listing in listings:
                    try:
                        title_el = listing.locator(".title a")
                        title = title_el.inner_text().strip() if title_el.count() > 0 else "N/A"
                        link = title_el.get_attribute("href") if title_el.count() > 0 else "N/A"
                        
                        position_info = listing.locator(".positionInfo")
                        if position_info.count() > 0:
                            pos_text = position_info.inner_text().strip()
                            if '-' in pos_text:
                                parts = pos_text.split('-')
                                community = parts[0].strip()
                                region = parts[1].strip()
                            else:
                                community = pos_text
                                region = "N/A"
                        else:
                            community = "N/A"
                            region = "N/A"
                        
                        house_info_el = listing.locator(".houseInfo")
                        house_info = house_info_el.inner_text().strip() if house_info_el.count() > 0 else "N/A"
                        
                        total_price_el = listing.locator(".totalPrice")
                        total_price = total_price_el.inner_text().strip() if total_price_el.count() > 0 else "N/A"
                        
                        unit_price_el = listing.locator(".unitPrice")
                        unit_price = unit_price_el.inner_text().strip() if unit_price_el.count() > 0 else "N/A"
                        
                        data_item = {
                            "title": title,
                            "community": community,
                            "region": region,
                            "house_info": house_info,
                            "total_price": total_price,
                            "unit_price": unit_price,
                            "link": link
                        }
                        all_data.append(data_item)
                        
                    except Exception as e:
                        print(f"Error parsing listing: {e}")
                        continue
                
                # Save incrementally
                if len(all_data) > 0:
                    pd.DataFrame(all_data).to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                    print(f"Total listings collected: {len(all_data)}")
                
                # Random delay before next page
                delay = random.uniform(5, 10)
                print(f"Waiting {delay:.1f}s before next page...")
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                continue

        browser.close()
        print(f"Crawling finished. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run()
