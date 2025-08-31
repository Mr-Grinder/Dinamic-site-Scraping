import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import string


options = uc.ChromeOptions()
options.add_argument("--start-maximized")  
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)


driver.get("https://www.weforum.org/partners/#search")


csv_file = "weforum_partners.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Partner_URL"])

# Множина для унікальних значень
partner_urls = set()


alphabet = list(string.ascii_uppercase)

wait = WebDriverWait(driver, 15)


# Основний цикл: клацаємо по кожній літері і збираємо посилання
for letter in alphabet:
    try:
        letter_xpath = f"//span[text()='{letter}']"
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, letter_xpath)))
        btn.click()  # клікаємо по літері

        items = driver.find_elements(By.CSS_SELECTOR, "a.organisation-search__list__link")

        new_count = 0
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for item in items:
                url = item.get_attribute("href")
                if url not in partner_urls:
                    partner_urls.add(url)
                    writer.writerow([url])
                    new_count += 1

        # Logs
        print(f"Letter '{letter}': added {new_count} new URLs (total: {len(partner_urls)})")

    except Exception as ex:
        print(f"⚠️ Error on letter '{letter}': {ex}")
        continue

driver.quit()
print(f"✅ Scraping complete: collected {len(partner_urls)} unique partner URLs.")
