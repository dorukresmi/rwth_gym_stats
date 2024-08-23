from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from datetime import datetime
import keras_ocr
import glob
import os
import base64

class VisitorCounter:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        profile_path = "/tmp/firefox_profile"
        self.options.set_preference("profile", profile_path)
        self.service = Service(executable_path="/usr/local/bin/geckodriver")
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
        self.url = "https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Auslastung.html"
        self.wait = None
        self.img_element = None
        if not os.path.exists("images_ss"):
            os.makedirs("images_ss")

    def get_and_save_image(self) -> str:
        self.driver.get(self.url)
        self.img_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@alt="Auslastung aktuell"]')))
        screenshot = self.img_element.screenshot_as_png
        iso_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encoded_datetime = self.encode_timestamp(iso_datetime)

        image_path = f"./images_ss/screenshot_{encoded_datetime}.png"

        with open(image_path, "wb") as f:
            f.write(screenshot)
        return image_path, iso_datetime
    
    @staticmethod
    def encode_timestamp(timestamp):
        encoded_bytes = base64.urlsafe_b64encode(timestamp.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        return encoded_str

    def reconnect_driver(self):
        self.driver.quit()
        self.driver = webdriver.Firefox(service=self.service)
        self.wait = WebDriverWait(self.driver, 10)
    
    @staticmethod
    def recognize_number_from_image():

        pipeline = keras_ocr.pipeline.Pipeline()

        latest_image = max(glob.glob("images_ss/screenshot_*.png"), key=os.path.getctime)
        image = keras_ocr.tools.read(latest_image)
        recognitions = pipeline.recognize(images=[image])

        recognized_text = recognitions[0][0][0]

        recognized_text = recognized_text.replace('o', '0')
        recognized_text = recognized_text.replace('O', '0')
        recognized_text = recognized_text.replace('z', '7')
        recognized_text = recognized_text.replace('Z', '7')
        recognized_text = recognized_text.replace('s', '5')
        recognized_text = recognized_text.replace('S', '5')
        recognized_text = recognized_text.replace('B', '8')
        recognized_text = recognized_text.replace('A', '4')
        recognized_text = recognized_text.replace('I', '1')
        recognized_text = recognized_text.replace('l', '1')
        recognized_text = recognized_text.replace('L', '1')
        recognized_text = recognized_text.replace('g', '9')
        recognized_text = recognized_text.replace('G', '6')
        recognized_text = recognized_text.replace('q', '9')


        recognized_number = int(''.join(filter(str.isdigit, recognized_text)))

        return recognized_number

    def close_driver(self):
        self.driver.quit()

    def __del__(self):
        self.close_driver()