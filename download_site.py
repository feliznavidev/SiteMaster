# New function: scrape_visible_content
def scrape_visible_content(url, output_path, cookies):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    
    # First navigate to the domain to set cookies
    driver.get(SITE_URL)
    time.sleep(2)
    
    # Add cookies from login (filter for valid domain)
    for cookie in cookies:
        try:
            # Only add cookies that match the domain
            if 'domain' not in cookie or SITE_URL.split('/')[2] in cookie['domain']:
                driver.add_cookie(cookie)
        except Exception as e:
            print(f'Skipping cookie: {e}')
    
    # Now navigate to the target URL
    driver.get(url)
    time.sleep(5)  # Wait for content to load
    
    # Extract main content (Canvas uses id='content')
    try:
        content = driver.find_element(By.ID, 'content').get_attribute('innerHTML')
    except Exception:
        try:
            # Try to get the main content area
            content = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
        except Exception:
            content = driver.page_source
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    driver.quit()
import os
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import urllib.parse
import shutil

load_dotenv()
SITE_URL = os.getenv('site_url').strip("'")
SITE_LOGIN = os.getenv('site_login').strip("'")
SITE_PASSWORD = os.getenv('site_password').strip("'")

SESSION = requests.Session()

# Selenium setup
def get_logged_in_cookies():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Remove this line if you want to see the browser
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # You may need to specify the path to chromedriver.exe if not in PATH
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SITE_URL)
    time.sleep(2)
    # Wait for redirect to Microsoft login
    try:
        # Microsoft login: username/email
        username_input = driver.find_element(By.NAME, 'loginfmt')
        username_input.send_keys(SITE_LOGIN)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)
        # Microsoft login: password
        password_input = driver.find_element(By.NAME, 'passwd')
        password_input.send_keys(SITE_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete
        # If prompted for 'Stay signed in?', click 'Yes' or 'No'
        try:
            stay_signed_in = driver.find_element(By.ID, 'idBtn_Back')
            stay_signed_in.click()
            time.sleep(2)
        except Exception:
            pass
    except Exception as e:
        print('Could not find Microsoft login form. You may need to adjust the selectors.')
        driver.quit()
        raise e
    # Get cookies
    cookies = driver.get_cookies()
    driver.quit()
    return cookies

# You may need to adjust this for your site's login form
LOGIN_URL = SITE_URL + '/login'
DOWNLOAD_DIR = 'offline_site'


# Step 1: Log in using Selenium and transfer cookies to requests
def login():
    cookies = get_logged_in_cookies()
    for cookie in cookies:
        SESSION.cookies.set(cookie['name'], cookie['value'])

# Step 2: Download a page and its assets
def download_page(url, base_url, visited):
    if url in visited:
        return
    visited.add(url)
    print(f'Downloading: {url}')
    # Custom handling for file downloads
    parsed_url = urllib.parse.urlparse(url)
    if '/files/' in parsed_url.path and ('?wrap=1' in url or '?download' in url):
        # This is a direct file download
        try:
            resp = SESSION.get(url, stream=True)
            resp.raise_for_status()
            # Try to get filename from Content-Disposition header
            filename = None
            cd = resp.headers.get('Content-Disposition')
            if cd and 'filename=' in cd:
                filename = cd.split('filename=')[1].strip('"')
            if not filename:
                filename = os.path.basename(parsed_url.path)
            file_path = os.path.join(DOWNLOAD_DIR, 'files', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(resp.raw, f)
            print(f'File saved: {file_path}')
        except Exception as e:
            print(f'Failed to download file {url}: {e}')
        return
    elif '/files' in parsed_url.path and '/files/' not in parsed_url.path:
        # Skip file listing pages
        print(f'Skipping file listing page: {url}')
        return
    else:
        resp = SESSION.get(url)
        try:
            resp.raise_for_status()
        except Exception as e:
            print(f'Failed to download page {url}: {e}')
            return
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Save HTML
        rel_path = parsed_url.path.strip('/') or 'index.html'
        # Always save HTML files with .html extension
        if not rel_path.endswith('.html'):
            if rel_path == '' or rel_path.endswith('/'):
                rel_path = rel_path.rstrip('/') + 'index.html'
            else:
                rel_path = rel_path + '.html'
        file_path = os.path.join(DOWNLOAD_DIR, rel_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(resp.text)
    # Download assets (images, css, js)
    for tag in soup.find_all(['img', 'script', 'link']):
        src = tag.get('src') or tag.get('href')
        if src and not src.startswith('data:'):
            asset_url = urllib.parse.urljoin(base_url, src)
            asset_path = os.path.join(DOWNLOAD_DIR, urllib.parse.urlparse(asset_url).path.strip('/'))
            os.makedirs(os.path.dirname(asset_path), exist_ok=True)
            try:
                asset_resp = SESSION.get(asset_url, stream=True)
                asset_resp.raise_for_status()
                with open(asset_path, 'wb') as af:
                    shutil.copyfileobj(asset_resp.raw, af)
            except Exception as e:
                print(f'Failed to download asset {asset_url}: {e}')
    # Find internal links to follow
    for a in soup.find_all('a', href=True):
        link = urllib.parse.urljoin(base_url, a['href'])
        if link.startswith(base_url):
            download_page(link, base_url, visited)

def main():
    print('Logging in with Selenium and scraping content...')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    
    # Log in once
    driver.get(SITE_URL)
    time.sleep(2)
    # Microsoft login: username/email
    try:
        username_input = driver.find_element(By.NAME, 'loginfmt')
        username_input.send_keys(SITE_LOGIN)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)
        # Microsoft login: password
        password_input = driver.find_element(By.NAME, 'passwd')
        password_input.send_keys(SITE_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete
        # If prompted for 'Stay signed in?', click 'Yes' or 'No'
        try:
            stay_signed_in = driver.find_element(By.ID, 'idBtn_Back')
            stay_signed_in.click()
            time.sleep(2)
        except Exception:
            pass
    except Exception as e:
        print(f'Login failed: {e}')
        driver.quit()
        return
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Now scrape content from various pages using the authenticated session
    pages_to_scrape = [
        '/courses/21350/pages/critical-worksheet-example-et-poster-the-primary-text',
        '/courses/21350/assignments/syllabus',
        '/courses/21350/assignments',
        '/courses/21350/modules',
        '/courses/21350/pages',
        '/courses/21716/assignments/syllabus',
        '/courses/21716/assignments',
        '/courses/22126/assignments/syllabus',
        '/courses/22126/assignments'
    ]
    
    for page_path in pages_to_scrape:
        full_url = SITE_URL + page_path
        print(f'Scraping {full_url}...')
        driver.get(full_url)
        time.sleep(3)  # Wait for content to load
        
        # Extract main content
        try:
            # Try different content selectors
            content_element = None
            for selector in ['#content', '.ic-Layout-contentMain', 'main', 'body']:
                try:
                    content_element = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if content_element:
                content = content_element.get_attribute('innerHTML')
            else:
                content = driver.page_source
                
        except Exception as e:
            print(f'Error extracting content from {full_url}: {e}')
            content = driver.page_source
        
        # Save content
        filename = page_path.replace('/', '_').replace('%20', '_') + '.html'
        output_path = os.path.join(DOWNLOAD_DIR, 'scraped_' + filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Saved content to {output_path}')
    
    driver.quit()
    print('Rendered content scraping complete. Check the offline_site folder.')

if __name__ == '__main__':
    main()
