from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
import re
from datetime import datetime

def extract_car_data(car_text):
    """
    Extract car details from the text content.
    Returns a dictionary with the extracted data.
    """
    lines = car_text.strip().split('\n')
    
    data = {
        'Car_Name': '',
        'Year': '',
        'Kilometers_Driven': '',
        'Fuel_Type': '',
        'Transmission': '',
        'Price': ''
    }
    
    try:
        # First line usually contains year and car name
        first_line = lines[0].strip()
        year_match = re.search(r'\b(19|20)\d{2}\b', first_line)
        if year_match:
            data['Year'] = year_match.group(0)
            data['Car_Name'] = first_line
        
        # Parse through other lines
        for line in lines[1:]:
            line = line.strip()
            
            # Kilometers driven (e.g., "34.11k km" or "96.90k km")
            if 'km' in line.lower() and ('k' in line.lower() or re.search(r'\d', line)):
                data['Kilometers_Driven'] = line
            
            # Fuel type
            elif any(fuel in line.lower() for fuel in ['petrol', 'diesel', 'cng', 'electric', 'hybrid']):
                data['Fuel_Type'] = line
            
            # Transmission
            elif any(trans in line.lower() for trans in ['manual', 'auto', 'automatic']):
                data['Transmission'] = line
            
            # Price (looking for lakh pattern)
            elif 'lakh' in line.lower() and '₹' in line:
                # Extract the main price (e.g., "₹3.35 lakh")
                price_match = re.search(r'₹[\d.]+\s*lakh', line)
                if price_match:
                    data['Price'] = price_match.group(0)
    
    except Exception as e:
        print(f"Error parsing data: {e}")
    
    return data


# Initialize Chrome driver
driver = webdriver.Chrome()

try:
    # Navigate to the website
    driver.get("https://www.cars24.com/buy-used-car/?f=make%3A%3D%3Ahyundai&search=hyundai&listingSource=Search_HP&storeCityId=2378")
    time.sleep(5)  # Wait for page to load completely
    
    # Scroll and click "Load More" or similar buttons to load all cars
    print("Loading all car listings...")
    print(f"URL: {driver.current_url}\n")
    
    previous_count = 0
    no_change_iterations = 0
    max_iterations = 100  # Maximum number of scroll attempts
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Get current count of car elements
        current_elems = driver.find_elements(By.CLASS_NAME, "styles_outer__NTVth")
        current_count = len(current_elems)
        
        print(f"Iteration {iteration}: Found {current_count} cars")
        
        # Try different scrolling methods
        # Method 1: Scroll in increments
        for i in range(5):
            driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(0.2)
        
        # Method 2: Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Method 3: Try scrolling within specific containers
        try:
            containers = driver.find_elements(By.CSS_SELECTOR, "div[class*='container'], div[class*='list'], div[class*='grid']")
            for container in containers[:3]:  # Try first 3 containers
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
        except:
            pass
        
        time.sleep(1)
        
        # Try to find and click various types of load more buttons
        button_clicked = False
        button_selectors = [
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more')]",
            "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show')]",
            "//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load')]",
            "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more')]",
            "//*[contains(@class, 'load')]",
            "//*[contains(@class, 'more')]",
            "//*[contains(@class, 'pagination')]//button",
            "//*[contains(@class, 'next')]",
        ]
        
        for selector in button_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        try:
                            # Scroll to button
                            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                            time.sleep(0.5)
                            # Try clicking
                            button.click()
                            print(f"  → Clicked button: {button.text[:50]}")
                            button_clicked = True
                            time.sleep(2)
                            break
                        except:
                            # Try JavaScript click
                            try:
                                driver.execute_script("arguments[0].click();", button)
                                print(f"  → JS-clicked button: {button.text[:50]}")
                                button_clicked = True
                                time.sleep(2)
                                break
                            except:
                                pass
                if button_clicked:
                    break
            except:
                continue
        
        time.sleep(1)
        
        # Check if new cars were loaded
        new_elems = driver.find_elements(By.CLASS_NAME, "styles_outer__NTVth")
        new_count = len(new_elems)
        
        if new_count > current_count:
            print(f"  ✓ Loaded {new_count - current_count} more cars (Total: {new_count})")
            no_change_iterations = 0
        else:
            no_change_iterations += 1
            print(f"  → No new cars loaded (attempt {no_change_iterations}/8)")
        
        # If no new content loaded for 8 consecutive iterations, stop
        if no_change_iterations >= 8:
            print("\n" + "="*60)
            print("No more cars to load. This appears to be all available cars.")
            print("="*60 + "\n")
            break
        
        previous_count = new_count
    
    print("Finished loading. Collecting all car listings...\n")
    
    # Find all car listing elements after loading everything
    elems = driver.find_elements(By.CLASS_NAME, "styles_outer__NTVth")
    
    print(f"Total cars found: {len(elems)}")
    print("Extracting data...\n")
    
    # Collect data from all elements
    all_cars_data = []
    
    for idx, elem in enumerate(elems, 1):
        try:
            # Get the text content of each car listing
            car_text = elem.text
            car_data = extract_car_data(car_text)
            all_cars_data.append(car_data)
            print(f"✓ Car #{idx}: {car_data['Car_Name']}")
        except Exception as e:
            print(f"✗ Error extracting Car #{idx}: {str(e)}")
    
    # Save to CSV file
    if all_cars_data:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_filename = f"cars24_data_{timestamp}.csv"
        
        fieldnames = ['Car_Name', 'Year', 'Kilometers_Driven', 'Fuel_Type', 'Transmission', 'Price']
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_cars_data)
        
        print(f"\n{'='*60}")
        print(f"✓ Data successfully saved to '{csv_filename}'")
        print(f"✓ Total records: {len(all_cars_data)}")
        print(f"{'='*60}")
    else:
        print("No data found to write to CSV")

finally:
    # Close the browser
    time.sleep(2)
    driver.close()
    print("\nBrowser closed.")