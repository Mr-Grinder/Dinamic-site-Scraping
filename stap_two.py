import json
import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CSV_FILE = "weforum_partners.csv"

# Get urls
with open(CSV_FILE, "r") as f:
    reader = csv.reader(f)
    next(reader)
    profile_urls = [row[0] for row in reader]

# Browser setup
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

results = []

for url in profile_urls:  
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "organization__profile")))
        time.sleep(2)

        try:
            full_name = driver.find_element(By.CSS_SELECTOR, "h1.organization__name").text
        except:
            full_name = ""

        try:
            website = driver.find_element(By.CLASS_NAME, "organization__website--dark").get_attribute("href")
        except:
            website = ""

        try:
            logo = driver.find_element(By.CSS_SELECTOR, "figure.organization__logo img").get_attribute("src")
        except:
            logo = ""

        results.append({
            "Partner name": full_name,
            "Website partner": website,
            "Partner logo": logo
        })

        print(f"✅ Зібрано: {full_name}")

    except Exception as e:
        print(f"⚠️ Помилка з профілем: {url} — {e}")

driver.quit()

# Saving in file
if results:
    with open("weforum_partners_details.csv", "w", newline="", encoding="utf-8") as csvfile:
        filednames = ["Partner name", "Website partner", "Partner logo"]
        writer = csv.DictWriter(csvfile, fieldnames=filednames)
        writer.writeheader()
        writer.writerows(results)
    print(f"🎉 Збережено {len(results)} партнерів у weforum_partners_details.csv")
else:
    print("🚫 Нічого не зібрано")
