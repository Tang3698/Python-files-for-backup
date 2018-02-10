from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
import time

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

driver.get(
    "http://w3.huawei.com/ibilling/#!ibilling/docmanage/mydoc/myDocManagement.html")
driver.find_element_by_id("uid").send_keys("twx277448")
driver.find_element_by_id("password").send_keys("True2017@")
driver.find_element_by_name("Submit").click()

sitelist=["CMI2019_A850on900_UPC1","CMI7150_A850on900_UPC1","CMI7508_A850on900_UPC1","CMI7516_A850on900_UPC1","CMI7521_A850on900_UPC1","CMI7524_A850on900_UPC1","CMI7526_A850on900_UPC1","CMI7527_A850on900_UPC1","CMI7528_A850on900_UPC1","CMI7529_A850on900_UPC1","CMI7537_A850on900_UPC1","CMI7547_A850on900_UPC1","CMI7555_A850on900_UPC1","CMI7556_A850on900_UPC1","CMI7565_A850on900_UPC1","CMI7569_A850on900_UPC1","CMI7571_A850on900_UPC1","CMI7577_A850on900_UPC1","CMI7592_A850on900_UPC1","CMI7595_A850on900_UPC1","CMI7599_A850on900_UPC1","CMI7607_A850on900_UPC1","CMI7619_A850on900_UPC1","CMI7621_A850on900_UPC1","CMI7633_A850on900_UPC1","CMI7640_A850on900_UPC1","CMI7642_A850on900_UPC1","CMI7643_A850on900_UPC1","CMI7646_A850on900_UPC1","CMI7660_A850on900_UPC1","CMI7661_A850on900_UPC1","CMI7676_A850on900_UPC1","CMI7677_A850on900_UPC1","CMI7679_A850on900_UPC1","CMI8531_A850on900_UPC1","CMI8533_A850on900_UPC1","CMI8562_A850on900_UPC1","CMI8565_A850on900_UPC1","CMI8592_A850on900_UPC1","CMI8779_A850on900_UPC1","CMI8782_A850on900_UPC1","CMI8832_A850on900_UPC1","CMI8836_A850on900_UPC1"]


for site in sitelist:
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "siteCode")))
    if element:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "siteCode")))
        dnno = driver.find_element_by_id("siteCode")
        try:
           dnno.clear()
           dnno.send_keys(site)
        except:
           print(site+"query error"+"/n")
        else:
           driver.find_element_by_id("btnSearch").click()
           WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID,"myDocGridTable")))
           driver.find_element_by_xpath("//table[@id='myDocGridHeader']/tbody[2]/tr/td[2]/div/span").click()
           driver.find_element_by_xpath("//span[@id='btnGenerateBillingDoc']/label").click()
           time.sleep(2)

           WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".jalor-button.default")))
           link = driver.find_element_by_css_selector(".jalor-dialog-content > a:nth-child(1)")
           ActionChains(driver).click(link).perform()
           time.sleep(2)
           print(site + " query done" + "/n")
           driver.find_element_by_id("leftSiteMapTree_14_span").click()