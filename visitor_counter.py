from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import keras_ocr
import glob
import os

class VisitorCounter:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.service = Service(self.driver_path)
        self.driver = webdriver.Firefox(service=self.service)
        self.url = "https://buchung.hsz.rwth-aachen.de/angebote/aktueller_zeitraum/_Auslastung.html"
        self.wait = WebDriverWait(self.driver, 10)
        self.img_element = None
        if not os.path.exists("images_ss"):
            os.makedirs("images_ss")

    def get_and_save_image(self):
        self.driver.get(self.url)
        self.img_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//img[@alt="Auslastung aktuell"]')))
        screenshot = self.img_element.screenshot_as_png
        formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"./images_ss/screenshot_{formatted_datetime}.png", "wb") as f:
            f.write(screenshot)
        return formatted_datetime

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

        print(recognitions)
        # Extract the recognized text
        recognized_text = recognitions[0][0][0]

        # Replace occurrences of 'o' with '0' in the recognized text
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


        # Extract the recognized number (assuming it's the only number in the text)
        recognized_number = int(''.join(filter(str.isdigit, recognized_text)))

        return recognized_number

    def close_driver(self):
        self.driver.quit()

    def __del__(self):
        self.close_driver()