from selenium import webdriver  
import time  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv 

class Result_Downloader:
    def __init__(self, results_directory, driver_path):
        self.xpath = {
            "district_button" : "/html/body/form/div[5]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/button",
            "district_dropdown_option" : "//*[@id=\"bs-select-1-48\"]",
            "roll_no_textbox" : "//*[@id=\"ctl00_cphBody_txt_RollNumber\"]",
            "viewResult_button" : "//*[@id=\"ctl00_cphBody_btnSubmit\"]",
            "data_table" : "//*[@id=\"ctl00_cphBody_tbl_Result\"]"
        }
        self.driver = webdriver.Firefox(executable_path=driver_path)
        self.driver.maximize_window()
        self.results_directory = results_directory
    
    def downloadResult(self, roll_no):
        roll_no = str(roll_no)

        self.driver.get("https://upmsp.edu.in/ResultHighSchool.aspx")

        self.driver.find_element_by_xpath(self.xpath["district_button"]).click()
        # time.sleep(1)
        self.driver.find_element_by_xpath(self.xpath["district_dropdown_option"]).click()
        time.sleep(1)
        # input rollno
        self.driver.find_element_by_xpath(self.xpath["roll_no_textbox"]).send_keys(roll_no) 

        attempt = 2
        while(self.driver.find_element_by_xpath(self.xpath["roll_no_textbox"]).get_attribute("value") != roll_no):
            # print("attempt=" + str(attempt))
            # time.sleep(attempt)
            text_box = self.driver.find_element_by_xpath(self.xpath["roll_no_textbox"])
            attempt += 1
            for i in range(9):
                text_box.send_keys(Keys.BACKSPACE)
            text_box.send_keys(roll_no) 

        self.driver.find_element_by_xpath(self.xpath["viewResult_button"]).click()        

        table = self.driver.find_element_by_xpath(self.xpath["data_table"])

        with open(self.results_directory + roll_no + '.csv', 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table.find_elements_by_css_selector('tr'):
                # print([d.text for d in row.find_elements_by_css_selector('td')])
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

        # time.sleep(1)

    def close(self):
        self.driver.close()  

