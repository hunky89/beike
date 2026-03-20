import random
import time
import pandas as pd
import logging
import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# --- Configuration ---
# District mapping: English code -> Chinese name (for logging/file naming if needed)
DISTRICTS = {
    "yanta": "雁塔",
    "changan": "长安",
    "lianhu": "莲湖",
    "beilin": "碑林",
    "weiyang": "未央",
    "xixianxinquxian": "西咸新区"
}
BASE_URL_TEMPLATE = "https://xa.ke.com/xiaoqu/{}/pg{}/"
MAX_PAGES = 100  # Set a safe upper limit per district
OUTPUT_FILE = "xian_xiaoqu_data.csv"
LOG_FILE = "spider_xiaoqu.log"
HEADLESS = False  # Set to False to see the browser and handle login manually
USER_DATA_DIR = "./user_data"  # Directory to store browser profile

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Helper Functions ---
def random_sleep(min_seconds=0.2, max_seconds=1.0):
    """Sleep for a random amount of time."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def simulate_human_behavior(page):
    """Simulates human behavior like scrolling and mouse movements."""
    try:
        # Reduced movement for speed
        page.mouse.move(random.randint(0, 500), random.randint(0, 500))
        
        # Fast scroll
        page.mouse.wheel(0, 500)
        time.sleep(0.2)
    except Exception as e:
        logger.warning(f"Error simulating human behavior: {e}")

def check_login_captcha(page):
    """Checks for login or captcha and waits for manual resolution."""
    try:
        if "登录" in page.title() or "login" in page.url:
            logger.warning("⚠️ Login page detected! Please login manually in the browser.")
            while "登录" in page.title() or "login" in page.url:
                time.sleep(5)
                if "登录" not in page.title() and "login" not in page.url:
                    logger.info("Login successful! Resuming...")
                    random_sleep(2, 4)
                    break
        
        if "验证" in page.title() or "CAPTCHA" in page.content():
            logger.warning("⚠️ CAPTCHA detected! Please solve it manually.")
            while "验证" in page.title() or "CAPTCHA" in page.content():
                time.sleep(5)
                if "验证" not in page.title() and "CAPTCHA" not in page.content():
                    logger.info("CAPTCHA resolved! Resuming...")
                    random_sleep(2, 4)
                    break
    except Exception as e:
        logger.error(f"Error checking login/captcha: {e}")

def extract_data(page, page_num):
    """Extracts community data from the current page."""
    data_list = []
    
    # Select all community list items
    # Note: Selectors are based on standard Lianjia xiaoqu page structure.
    # Adjust if the website structure changes.
    items = page.locator(".xiaoquListItem").all()
    
    if not items:
        logger.warning(f"No items found on page {page_num}. Selectors might be wrong or page is empty.")
        # Debug: Save page content if empty
        with open(f"debug_page_{page_num}.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        return []

    logger.info(f"Found {len(items)} items on page {page_num}.")
    
    for item in items:
        try:
            # 1. Name
            # Try multiple selectors for title
            title_el = item.locator(".title .maxtitle")
            if title_el.count() == 0:
                title_el = item.locator(".title a") # Fallback
            
            name = title_el.first.inner_text().strip() if title_el.count() > 0 else "N/A"
            link = title_el.first.get_attribute("href") if title_el.count() > 0 else "N/A"
            
            # 2. Price (Average Price)
            # Try multiple selectors for price
            price_el = item.locator(".xiaoquListItemPrice .totalPrice span")
            if price_el.count() == 0:
                 price_el = item.locator(".totalPrice span") # Fallback
            
            price = price_el.first.inner_text().strip() if price_el.count() > 0 else "N/A"
            
            # 3. Info (Year, Type)
            # Example text: "2015年建成 \n 塔板结合"
            info_el = item.locator(".positionInfo")
            info_text = info_el.inner_text().strip().replace("\n", " ") if info_el.count() > 0 else "N/A"
            
            # Extract Year if possible
            year = "N/A"
            if "年建成" in info_text:
                parts = info_text.split()
                for part in parts:
                    if "年建成" in part:
                        year = part.replace("年建成", "")
                        break
            
            # 4. District/Area
            # Usually in .districtTitle
            district_el = item.locator(".positionInfo") # Sometimes district is here too or separate
            # Let's try .tagList for specific tags or .houseInfo for other stats
            
            # 5. Sold Count (90 days)
            # Use .first to avoid strict mode violation if multiple links exist
            sold_el = item.locator(".houseInfo a").first
            sold_count = sold_el.inner_text().strip() if sold_el.count() > 0 else "N/A"
            
            # 6. Listings Count (Currently selling)
            selling_el = item.locator(".xiaoquListItemSellCount a span")
            if selling_el.count() == 0:
                 selling_el = item.locator(".xiaoquListItemSellCount span") # Fallback without link

            selling_count = selling_el.first.inner_text().strip() if selling_el.count() > 0 else "N/A"

            item_data = {
                "name": name,
                "price": price,
                "year": year,
                "info": info_text,
                "sold_90_days": sold_count,
                "selling_count": selling_count,
                "link": link,
                "scrape_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "page_num": page_num,
                # We will add district later in the main loop or pass it here
            }
            data_list.append(item_data)
            
        except Exception as e:
            logger.error(f"Error parsing item: {e}")
            continue
            
    return data_list

def run():
    # --- Resume Logic (Simplified for Multi-district) ---
    # We will check if the specific district+page exists in the CSV to decide where to start for EACH district.
    # But since all data goes to one file, it's safer to just check the last scraped district and page.
    # For robustness, we will iterate all districts and check if we have enough data or just append.
    # To keep it simple: We will iterate through the list. If data for a district/page exists, we skip it.
    
    existing_records = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            df = pd.read_csv(OUTPUT_FILE)
            if not df.empty and 'link' in df.columns:
                 # Use link as unique identifier to avoid duplicates
                 existing_records = set(df['link'].tolist())
            logger.info(f"Loaded {len(existing_records)} existing records.")
        except Exception as e:
            logger.error(f"Error reading existing file: {e}")

    with sync_playwright() as p:
        logger.info("Attempting to connect to existing Chrome browser...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            if len(context.pages) > 0:
                page = context.pages[0]
            else:
                page = context.new_page()
            logger.info("Successfully connected to Chrome!")
        except Exception as e:
            logger.error(f"Could not connect to Chrome: {e}")
            logger.info("Please make sure you started Chrome with: --remote-debugging-port=9222")
            return

        try:
            for district_code, district_name in DISTRICTS.items():
                logger.info(f"--- Starting scraping for district: {district_name} ({district_code}) ---")
                
                for page_num in range(1, MAX_PAGES + 1):
                    url = BASE_URL_TEMPLATE.format(district_code, page_num)
                    logger.info(f"Navigating to {district_name} page {page_num}: {url}")
                    
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=60000)
                        
                        # Handle Login/Captcha (Still needed even in CDP mode if session expires)
                        check_login_captcha(page)
                        
                        # Simulate human behavior
                        simulate_human_behavior(page)
                        
                        # Wait for list to load
                        try:
                            page.wait_for_selector(".xiaoquListItem", timeout=10000)
                        except PlaywrightTimeoutError:
                            logger.warning("List items not found. Checking for 'No Results' or end of pagination.")
                            if page.locator(".no-result-wrapper").count() > 0 or "没有找到" in page.content():
                                logger.info(f"No more results for {district_name}. Moving to next district.")
                                break
                            else:
                                logger.warning("Page might not have loaded correctly. Retrying...")
                                check_login_captcha(page)
                                page.reload()
                                time.sleep(5)
                                if page.locator(".xiaoquListItem").count() == 0:
                                    logger.error("Still no items. Assuming end of district.")
                                    break

                        # Extract Data
                        data = extract_data(page, page_num)
                        
                        if data:
                            # Add district info
                            for item in data:
                                item['district'] = district_name
                                item['district_code'] = district_code

                            # Filter out duplicates
                            new_data = [item for item in data if item['link'] not in existing_records]
                            
                            if new_data:
                                df = pd.DataFrame(new_data)
                                if not os.path.exists(OUTPUT_FILE):
                                    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                                else:
                                    df.to_csv(OUTPUT_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
                                
                                # Update memory set
                                existing_records.update([item['link'] for item in new_data])
                                logger.info(f"Saved {len(new_data)} new records from {district_name} page {page_num}.")
                            else:
                                logger.info(f"Page {page_num} for {district_name} already scraped. Skipping save.")
                                continue
                        else:
                            logger.warning(f"No data extracted from {district_name} page {page_num}. Assuming end of district.")
                            break
                        
                        # Adaptive delay
                        random_sleep(0.5, 1.5)
                        if page_num % 20 == 0:
                            long_sleep = random.uniform(2, 5)
                            logger.info(f"Taking a short break ({long_sleep:.1f}s)...")
                            time.sleep(long_sleep)
                            
                    except Exception as e:
                        logger.error(f"Error processing {district_name} page {page_num}: {e}")
                        continue
                
                logger.info(f"--- Finished scraping for district: {district_name} ---")
                time.sleep(5) # Pause between districts

        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            logger.info("Disconnected from browser. Scraping finished/stopped.")

if __name__ == "__main__":
    run()
