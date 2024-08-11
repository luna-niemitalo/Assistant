import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

ParseWebsite_description = {
    "type": "function",
    "function": {
        "name": "parse_website",
        "description": "Extract text content from a specified URL using web scraping.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the webpage to scrape."
                },
            },
            "required": ["url"]
        },
    }
}

def parse_website(url):
    # Set up Selenium WebDriver (make sure to download the correct driver for your browser)

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up Selenium WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    # Load the webpage
    driver.get(url)

    # Wait for the dynamic content to load (you may need to adjust this timeout)
    time.sleep(5)

    # Get the page source
    page_source = driver.page_source

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract text elements (you can adjust the selector to target specific elements)
    text_content = soup.get_text(strip=True, separator='\n')

    # Close the browser
    driver.quit()

    return text_content

if __name__ == "__main__":
    url = "https://www.example.com"  # Replace with the actual URL
    extracted_text = parse_website(url)

    # Print the extracted text
    print(extracted_text)
