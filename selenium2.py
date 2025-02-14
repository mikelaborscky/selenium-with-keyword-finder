from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Konfigurasi GeckoDriver
gecko_path = "lokasi folder geckodriver.exe"  # Ubah path ke lokasi GeckoDriver di sistem Anda
base_url = "url target"  # Bagian tetap dari URL
start_page = 1  # Halaman awal untuk memulai pemindaian
keyword_target = "target keyword"  # Keyword yang ingin dicari

# Inisialisasi WebDriver
service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Aktifkan mode headless
driver = webdriver.Firefox(service=service, options=options)

def search_keyword_in_table(driver, keyword_target):
    """
    Fungsi untuk mencari keyword (teks) dalam elemen <a> pada tabel di halaman saat ini.
    """
    try:
        # Tunggu hingga tabel selesai dimuat
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        print(f"Ditemukan {len(rows)} baris di tabel.")

        for row in rows:
            # Cari elemen <td> di dalam baris
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                # Cari elemen <a> di dalam <td>
                links = cell.find_elements(By.TAG_NAME, "a")
                for link in links:
                    # Cek jika teks di dalam <a> mengandung keyword_target
                    if keyword_target.lower() in link.text.lower():
                        print(f"Keyword '{keyword_target}' ditemukan di link: {link.text}")
                        return True  # Berhenti setelah menemukan keyword
        print(f"Keyword '{keyword_target}' tidak ditemukan di tabel pada halaman ini.")
        return False
    except TimeoutException:
        print("Tabel atau data dalam tabel tidak ditemukan.")
        return False
    except NoSuchElementException:
        print("Tabel tidak ditemukan di halaman ini.")
        return False

try:
    current_page = start_page  # Mulai dari halaman awal
    found = False

    while True:
        # Format URL untuk halaman saat ini
        current_url = f"{base_url}{current_page}"
        print(f"Memindai halaman: {current_url}")
        driver.get(current_url)

        # Panggil fungsi pencarian
        if search_keyword_in_table(driver, keyword_target):
            found = True
            break

        # Update ke halaman berikutnya
        current_page += 1
        time.sleep(3)  # Tunggu halaman berikutnya dimuat

    if not found:
        print(f"Keyword '{keyword_target}' tidak ditemukan di semua halaman.")

finally:
    driver.quit()
