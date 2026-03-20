import random
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# Configuration
BASE_URL = "https://xa.ke.com/xiaoqu/pg{}/"
MAX_PAGES = 50  # Adjust as needed
OUTPUT_FILE = "xian_xiaoqu_with_rent.csv"

# Read existing data if it exists
try:
    existing_data = pd.read_csv("xian_xiaoqu_data.csv")
except:
    existing_data = pd.DataFrame()

# Android device emulation settings
ANDROID_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-S906U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
]

ANDROID_DEVICE = {
    "width": 393,
    "height": 851,
    "deviceScaleFactor": 3,
    "isMobile": True,
    "hasTouch": True,
    "isLandscape": False
}

# Enhanced headers
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

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

def extract_community_details(page, community_link):
    """
    Extract成交均价, 平均租金 and 最近一个月成交数据 from community detail page
    """
    try:
        # Add random delay before navigating
        random_sleep(2, 4)
        
        # Set extra headers for the request
        page.set_extra_http_headers(HEADERS)
        
        # Navigate to community detail page
        page.goto(community_link, wait_until="networkidle", timeout=60000)
        random_sleep(4, 6)
        
        # Simulate human behavior - more realistic
        page.mouse.move(random.randint(100, 300), random.randint(100, 300))
        random_sleep(0.5, 1)
        
        # Scroll down slowly
        for _ in range(3):
            page.mouse.wheel(0, random.randint(150, 250))
            random_sleep(0.8, 1.2)
        
        # Extract 成交均价 (from main page)
        deal_price = "N/A"
        try:
            deal_price_el = page.locator(".xiaoquUnitPrice .xiaoquPrice").first
            if deal_price_el.count() > 0:
                deal_price = deal_price_el.inner_text().strip()
        except Exception as e:
            print(f"Error extracting deal price: {e}")
        
        # Extract 平均租金
        avg_rent = "N/A"
        try:
            # Find and click rent tab using more specific selector
            rent_tab = page.locator("a:has-text('租赁')").first
            if rent_tab.count() > 0:
                # Move to element first
                rent_tab.hover()
                random_sleep(0.5, 1)
                # Click with human-like delay
                rent_tab.click()
                random_sleep(3, 5)
                
                # Simulate human behavior after click
                page.mouse.move(random.randint(100, 300), random.randint(200, 400))
                random_sleep(0.5, 1)
                
                # Extract rent price
                rent_price_el = page.locator(".xiaoquUnitPrice .xiaoquPrice").first
                if rent_price_el.count() > 0:
                    avg_rent = rent_price_el.inner_text().strip()
        except Exception as e:
            print(f"Error extracting rent price: {e}")
        
        # Extract 最近一个月成交数据
        recent_deals = []
        avg_deal_price_month = "N/A"
        
        try:
            # Find and click deal tab using more specific selector
            deal_tab = page.locator("a:has-text('成交')").first
            if deal_tab.count() > 0:
                # Move to element first
                deal_tab.hover()
                random_sleep(0.5, 1)
                # Click with human-like delay
                deal_tab.click()
                random_sleep(4, 6)
                
                # Simulate human behavior after click
                simulate_human_behavior(page)
                
                # Extract recent deals (last month)
                deal_items = page.locator(".chengjiaoList .item").all()
                recent_month_deals = []
                
                for item in deal_items:
                    try:
                        deal_date = item.locator(".dealDate").inner_text().strip() if item.locator(".dealDate").count() > 0 else "N/A"
                        total_price = item.locator(".totalPrice").inner_text().strip() if item.locator(".totalPrice").count() > 0 else "N/A"
                        unit_price = item.locator(".unitPrice").inner_text().strip() if item.locator(".unitPrice").count() > 0 else "N/A"
                        
                        # Check if deal is within last month
                        if deal_date and "天前" in deal_date:
                            days = int(deal_date.replace("天前", ""))
                            if days <= 30:
                                recent_month_deals.append({"date": deal_date, "price": total_price, "unit_price": unit_price})
                        
                    except Exception as e:
                        print(f"Error extracting deal item: {e}")
                
                recent_deals = recent_month_deals
                
                # Calculate average deal price for last month
                if recent_month_deals:
                    try:
                        prices = []
                        for deal in recent_month_deals:
                            if deal['unit_price'] and "元/㎡" in deal['unit_price']:
                                price_str = deal['unit_price'].replace("元/㎡", "").replace(",", "")
                                if price_str.isdigit():
                                    prices.append(int(price_str))
                        if prices:
                            avg_deal_price_month = f"{int(sum(prices)/len(prices))} 元/㎡"
                    except Exception as e:
                        print(f"Error calculating avg deal price: {e}")
        except Exception as e:
            print(f"Error extracting recent deals: {e}")
        
        return deal_price, avg_rent, recent_deals, avg_deal_price_month
    except Exception as e:
        print(f"Error processing community page: {e}")
        return "N/A", "N/A", [], "N/A"

def run():
    with sync_playwright() as p:
        all_data = []
        
        print("Starting crawler...")
        
        for page_num in range(1, MAX_PAGES + 1):
            # Create new browser context for each page to avoid detection
            print(f"Launching browser for page {page_num}...")
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-gpu"
                ]
            )
            
            # Randomly select user agent
            selected_user_agent = random.choice(ANDROID_USER_AGENTS)
            
            context = browser.new_context(
                viewport=ANDROID_DEVICE,
                user_agent=selected_user_agent,
                device_scale_factor=ANDROID_DEVICE['deviceScaleFactor'],
                is_mobile=ANDROID_DEVICE['isMobile'],
                has_touch=ANDROID_DEVICE['hasTouch']
            )
            
            page = context.new_page()
            
            # Set default headers
            page.set_extra_http_headers(HEADERS)
            
            # Enhanced anti-detection script with random user agent
            anti_detection_script = '''
                // Remove webdriver flag
                Object.defineProperty(navigator, 'webdriver', {
                    get: function() { return undefined; }
                });
                
                // Remove Chrome automation extension
                Object.defineProperty(navigator, 'plugins', {
                    get: function() { return [1, 2, 3, 4, 5]; }
                });
                
                // Remove Chrome runtime
                Object.defineProperty(navigator, 'chrome', {
                    get: function() { return undefined; }
                });
                
                // Mock user agent data
                Object.defineProperty(navigator, 'userAgent', {
                    get: function() { return 'USER_AGENT_PLACEHOLDER'; }
                });
                
                // Mock document properties
                Object.defineProperty(document, 'webdriver', {
                    get: function() { return undefined; }
                });
                
                // Mock window properties
                Object.defineProperty(window, 'navigator', {
                    value: navigator
                });
                
                // Mock device memory
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: function() { return 8; }
                });
                
                // Mock hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: function() { return 8; }
                });
                
                // Mock screen properties
                Object.defineProperty(screen, 'width', {
                    get: function() { return 1080; }
                });
                Object.defineProperty(screen, 'height', {
                    get: function() { return 2400; }
                });
                Object.defineProperty(screen, 'colorDepth', {
                    get: function() { return 24; }
                });
                
                // Mock other properties
                Object.defineProperty(navigator, 'language', {
                    get: function() { return 'zh-CN'; }
                });
                Object.defineProperty(navigator, 'languages', {
                    get: function() { return ['zh-CN', 'zh', 'en-US', 'en']; }
                });
            '''
            
            # Replace user agent placeholder
            anti_detection_script = anti_detection_script.replace('USER_AGENT_PLACEHOLDER', selected_user_agent)
            
            # Add the script
            page.add_init_script(anti_detection_script)

            url = BASE_URL.format(page_num)
            print(f"Navigating to page {page_num}: {url}")
            
            try:
                # Add referer if not first page
                if page_num > 1:
                    page.set_extra_http_headers({
                        "Referer": BASE_URL.format(page_num - 1)
                    })
                
                # Random delay before navigation
                random_sleep(2, 4)
                
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Simulate human behavior immediately after load
                simulate_human_behavior(page)
                
                # Check for CAPTCHA
                if "验证" in page.title() or "CAPTCHA" in page.content():
                    print("⚠️ CAPTCHA detected!")
                    print("Please manually solve the CAPTCHA in the browser window.")
                    print("The script will check every 5 seconds if the CAPTCHA is resolved...")
                    
                    start_time = time.time()
                    while "验证" in page.title() or "CAPTCHA" in page.content():
                        if time.time() - start_time > 60:
                            print("⚠️ CAPTCHA timeout, skipping page...")
                            break
                        time.sleep(5)
                        if "验证" not in page.title() and "CAPTCHA" not in page.content():
                            print("CAPTCHA resolved! Resuming...")
                            break
                        print("Waiting for CAPTCHA resolution...")
                    else:
                        # If we broke due to timeout, skip this page
                        browser.close()
                        continue
                
                # Check for Login
                if "登录" in page.title():
                    print("⚠️ Login required. Please login manually.")
                    start_time = time.time()
                    while "登录" in page.title():
                        if time.time() - start_time > 60:
                            print("⚠️ Login timeout, skipping page...")
                            break
                        time.sleep(5)
                        if "登录" not in page.title():
                            print("Login successful! Resuming...")
                            break
                        print("Waiting for Login...")
                    else:
                        # If we broke due to timeout, skip this page
                        browser.close()
                        continue

                # Check for blocked page
                if "访问过于频繁" in page.content() or "您的访问行为异常" in page.content():
                    print("⚠️ Page blocked, changing browser context...")
                    browser.close()
                    # Wait longer before next attempt
                    random_sleep(30, 60)
                    continue

                # Wait for the list to be visible
                try:
                    page.wait_for_selector(".listContent", timeout=15000)
                except:
                    print("List content not found. Checking for no results...")
                    if page.locator(".m-no-result").count() > 0:
                        print("No more results found. Ending crawler.")
                        browser.close()
                        break
                    print("Unknown error or empty page. Skipping page...")
                    browser.close()
                    continue

                # Extract data
                listings = page.locator(".info.clear").all()
                print(f"Found {len(listings)} listings on page {page_num}.")
                
                for listing in listings:
                    try:
                        # Random mouse movements before interacting
                        page.mouse.move(random.randint(100, 300), random.randint(100, 300))
                        random_sleep(0.3, 0.8)
                        
                        title_el = listing.locator(".title a")
                        name = title_el.inner_text().strip() if title_el.count() > 0 else "N/A"
                        link = title_el.get_attribute("href") if title_el.count() > 0 else "N/A"
                        
                        position_info = listing.locator(".positionInfo")
                        if position_info.count() > 0:
                            pos_text = position_info.inner_text().strip()
                            if ' ' in pos_text:
                                parts = pos_text.split(' ')
                                district = parts[0].strip() if len(parts) > 0 else "N/A"
                                street = parts[1].strip() if len(parts) > 1 else "N/A"
                            else:
                                district = pos_text
                                street = "N/A"
                        else:
                            district = "N/A"
                            street = "N/A"
                        
                        house_info_el = listing.locator(".houseInfo")
                        house_info = house_info_el.inner_text().strip() if house_info_el.count() > 0 else "N/A"
                        
                        price_el = listing.locator(".priceInfo .price")
                        price = price_el.inner_text().strip() if price_el.count() > 0 else "N/A"
                        
                        sold_90_days_el = listing.locator(".dealInfo .num")
                        sold_90_days = sold_90_days_el.inner_text().strip() if sold_90_days_el.count() > 0 else "0"
                        
                        # Extract community details (成交均价, 平均租金 and 最近一个月成交数据)
                        deal_price, avg_rent, recent_deals, avg_deal_price_month = "N/A", "N/A", [], "N/A"
                        if link and "xiaoqu" in link:
                            print(f"Extracting details for {name}...")
                            try:
                                deal_price, avg_rent, recent_deals, avg_deal_price_month = extract_community_details(page, link)
                            except Exception as e:
                                print(f"Error extracting details: {e}")
                                # If detail extraction fails, continue with other listings
                                pass
                        
                        data_item = {
                            "name": name,
                            "price": price,
                            "deal_price": deal_price,
                            "avg_rent": avg_rent,
                            "avg_deal_price_month": avg_deal_price_month,
                            "recent_deals_count": len(recent_deals),
                            "district": district,
                            "street": street,
                            "house_info": house_info,
                            "sold_90_days": f"90天成交{sold_90_days}套",
                            "link": link,
                            "scrape_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "page_num": page_num
                        }
                        all_data.append(data_item)
                        
                        # Random delay between listings
                        random_sleep(4, 7)
                        
                    except Exception as e:
                        print(f"Error parsing listing: {e}")
                        continue
                
                # Save incrementally
                if len(all_data) > 0:
                    df = pd.DataFrame(all_data)
                    # Merge with existing data if it exists
                    if not existing_data.empty:
                        df = pd.concat([existing_data, df], ignore_index=True)
                        df = df.drop_duplicates(subset=['link'], keep='last')
                    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                    print(f"Total communities collected: {len(df)}")
                
                # Close current browser context
                browser.close()
                
                # Random delay before next page
                delay = random.uniform(15, 30)
                print(f"Waiting {delay:.1f}s before next page...")
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                browser.close()
                # Wait longer on error
                random_sleep(20, 40)
                continue

        print(f"Crawling finished. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run()