from selenium import webdriver
from time import sleep
import re
search = (input("Pesquisar por: ")).replace(" ","+")
import pygsheets
import pandas as pd

# To put the result in Google Sheets
gc = pygsheets.authorize(service_file='/path/to/file/creds.json')

df = pd.DataFrame()
sh = gc.open('Leads Bot')
wks = sh[0]
group = []
sites = []

dvalid = ['11','12', '13', '14', '15', '16', '17', '18','19','21', '22', '24','27','28','31', '32', '33', '34', '35', '37', '38','41', '42', '43', '44', '45', '46','47', '48', '49',
          '51', '53', '54', '55','61','63','62','64','65','66','67','68','69','71', '73', '74', '75', '77','79','81','82','83','84','85','86','87','88','89','91','92','93','94','95','96','97','98','99']

class LeadBot:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/path/to/file')

    def get_leads(self):
        while True:
            def backpls():
                return self.driver.execute_script("window.history.go(-1)")

            pattern = '(\(0?([1-9][0-9])?[1-9]\d\) ?|0?([1-9][0-9])?[1-9]\d[ .-]?)?(9|9[ .-])?[2-9]\d{3}[ .-]?\d{4}|(\(0?([1-9][0-9])?[1-9]\d\) ?|0?([1-9][0-9])?[1-9]\d[ .-]?)?(9|9[ .-])?[2-9]\d{4}[ .-]?\d{3}'

            def start(st):
                self.driver.get("https://www.google.com/search?q="+search+"&start="+str(st))
                st += 10
                
                def searchpage(i):
                    nb_pages = len(self.driver.find_elements_by_class_name("LC20lb.MBeuO.DKV0Md"))

                    if i < nb_pages:
                        if self.driver.current_url[:23] == 'https://www.google.com/':
                            try:
                                self.driver.find_elements_by_class_name("LC20lb.MBeuO.DKV0Md")[i]\
                                    .click()
                                
                                if {"site": self.driver.current_url, "start": st} in sites:
                                    backpls()

                                elif self.driver.current_url[:23] != 'https://www.google.com/':
                                    body = self.driver.find_elements_by_tag_name("body")
                                    p = self.driver.find_elements_by_tag_name("p")
                                    ho = self.driver.find_elements_by_tag_name("h1")
                                    ht = self.driver.find_elements_by_tag_name("h2")
                                    hth = self.driver.find_elements_by_tag_name("h3")
                                    span = self.driver.find_elements_by_tag_name("span")
                                    ahref = self.driver.find_elements_by_tag_name("a")
                                    button = self.driver.find_elements_by_tag_name("button") #new

                                    sites.append({"site": self.driver.current_url, "start": st})
                                    i += 1

                                    def set_info(tag):
                                        for x in range(len(tag)):
                                            whats = re.search(pattern, tag[x].get_attribute("innerHTML"))

                                            if whats != None and (''.join(re.sub('\D', '', whats.group()))) not in group:
                                                numberf = ''.join(re.sub('\D', '', whats.group()))

                                                if (len(numberf) == 12 or len(numberf) == 13) and str(numberf[:2]) == '55':
                                                    group.append(numberf)
                                                    print(self.driver.current_url,numberf,(st-10))
                                                    df['site'] = [self.driver.current_url]
                                                    df['phone'] = [numberf]
                                                    ind = len(wks.get_values('A1','A1000',returnas='cell')) + 1
                                                    wks.set_dataframe(df,(ind,1),copy_head=False)

                                                elif (len(numberf) == 10 or len(numberf) == 11) and (str(numberf[:2]) in dvalid):
                                                    group.append(numberf)
                                                    print(self.driver.current_url,numberf,(st-10))
                                                    df['site'] = [self.driver.current_url]
                                                    df['phone'] = [numberf]
                                                    ind = len(wks.get_values('A1','A1000',returnas='cell')) + 1
                                                    wks.set_dataframe(df,(ind,1),copy_head=False)

                                    def set_infohref(tag):
                                        sleep(5)
                                        for x in range(len(tag)):
                                            whats = re.search(pattern, tag[x].get_attribute("href"))

                                            if whats != None and (''.join(re.sub('\D', '', whats.group()))) not in group:
                                                numberf = ''.join(re.sub('\D', '', whats.group()))

                                                if (len(numberf) == 12 or len(numberf) == 13) and str(numberf[:2]) == '55':
                                                    group.append(numberf)
                                                    print("href",self.driver.current_url,numberf,(st-10))
                                                    df['site'] = [self.driver.current_url]
                                                    df['phone'] = [numberf]
                                                    ind = len(wks.get_values('A1','A1000',returnas='cell')) + 1
                                                    wks.set_dataframe(df,(ind,1),copy_head=False)

                                                elif (len(numberf) == 10 or len(numberf) == 11) and (str(numberf[:2]) in dvalid):
                                                    group.append(numberf)
                                                    print("href",self.driver.current_url,numberf,(st-10))
                                                    df['site'] = [self.driver.current_url]
                                                    df['phone'] = [numberf]
                                                    ind = len(wks.get_values('A1','A1000',returnas='cell')) + 1
                                                    wks.set_dataframe(df,(ind,1),copy_head=False)

                                    set_info(body)
                                    set_info(p)
                                    set_info(ho)
                                    set_info(ht)
                                    set_info(hth)
                                    set_info(span)
                                    set_info(ahref)
                                    set_info(button) #new
                                    set_infohref(ahref)
                                    set_infohref(button) #new

                            except Exception as e:
                                if str(e)[:8] == "Message:":
                                    print(e)
                                    i += 1
                                    if self.driver.current_url[:23] == 'https://www.google.com/':
                                        searchpage(i) #loop i

                            backpls()

                    else:
                        sleep(5)
                        start(st) #loop start

                    if self.driver.current_url[:23] == 'https://www.google.com/':
                        sleep(1)
                        searchpage(i) #loop i

                i = 0
                searchpage(i) #initial i
            
            st = 0
            start(st) #initial start
    
LeadBot().get_leads()