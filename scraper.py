import requests
from bs4 import BeautifulSoup
import csv

def upgraded_scraper(url, tag, class_name=None, output_file="scraped_data.csv"):
    # Add Headers to look like a real browser (prevents getting blocked)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Scraping {url} for <{tag}> tags...")
        # Send the request with our "fake" browser headers
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the elements
        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)
            
        print(f"Found {len(elements)} elements. Saving to {output_file}...")
        
        # Save to a CSV file instead of just printing
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Create the column headers in the spreadsheet
            writer.writerow(['Index', 'Text Content', 'Link/Attribute']) 
            
            # Loop through all elements and save them to the file
            for i, element in enumerate(elements):
                text = element.get_text(strip=True)
                # If it's a link, grab the URL. Otherwise, mark as N/A.
                link = element.get('href') if element.name == 'a' else 'N/A'
                
                # Write the row to the CSV
                writer.writerow([i + 1, text, link])
                
        print("🎉 Scraping complete! Check your files for 'scraped_data.csv'.")

    except requests.exceptions.RequestException as e:
        print(f"Connection Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- Upgraded Web Scraper ---")
    url = input("Enter the URL to scrape (include http(s)://): ")
    tag = input("Enter the HTML tag to find (e.g. h1, a, p, div): ")
    class_name = input("Enter a class name to filter by (optional, press Enter to skip): ")
    
    class_name = class_name if class_name else None
    upgraded_scraper(url, tag, class_name)
