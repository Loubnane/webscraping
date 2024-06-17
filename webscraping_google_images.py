import hashlib
import io
import requests
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup

options = ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://www.automauritanie.com/petites-annonces-car-Mercedes-Benz-190?page=35#google_vignette")
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")
driver.quit()

def gets_url(classes, location, source):
    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name and name.get(source):
            results.append(name.get(source))
    return results

if __name__ == "__main__":
    returned_results = gets_url("slick-slide slick-current slick-active" , "img", "src")
    for b in returned_results:
        if not b.startswith('data:image'):  # Skip data URIs
            image_content = requests.get(b).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert("RGB")
            file_path = Path("out", hashlib.sha1(image_content).hexdigest()[:10] + ".png")
            image.save(file_path, "PNG", quality=95)
