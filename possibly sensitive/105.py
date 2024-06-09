import os
import time
import datetime
import math
from threading import Timer
import csv
import pandas as pd
import hashlib

class Linkedin:
    
    def __init__(self):
        print("Running...")
        options = Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(firefox_options=options)
        WebDriverWait(self.driver, timeout=10)
        self.driver.get("https://www.linkedin.com/uas/login?")
        username = ''
        password = ''
        with open('credentials.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['Username']
                password = row['Password']
        self.driver.find_element_by_name('session_key').send_keys(username)
        self.driver.find_element_by_name('session_password').send_keys(password)
        self.driver.find_element_by_name('signin').click()
        self.scrap()
    
        
    def scrap(self):
        profiles_list=[]
        data_list = []
        new_data = []
        
        with open('profiles.csv', 'r', newline='') as file:
            profiles_dict = csv.DictReader(file)
            for profile in profiles_dict:
                p_dict = {}
                p_dict['Name'] = profile['Name']
                p_dict['Surname'] = profile['Surname']
                p_dict['Linkedin_profile'] = profile['Linkedin_profile']
                profiles_list.append(p_dict)
            
        
\        for i in range(0 , len(profiles_list)):
            profile = profiles_list[i]
            name = profile['Name']
            surname = profile['Surname']
            profile_link = profile['Linkedin_profile']
            if profile_link is not None :
                if os.path.exists('old_data.csv'):
                    df = pd.read_csv('old_data.csv', sep=',')
                    df.set_index("Link", inplace=True)
                    try:
                        data_indi = df.loc[profile_link[28:]]
                    except KeyError:
                        data_indi = None
                    if data_indi is not None:
                        data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link, data_indi["Skills"], data_indi["Title"], data_indi["Desc"])
                        data_list.append(data_as_dict)
                        new_data.append(data_comp)
                    else:
                        data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link)
                        data_list.append(data_as_dict)
                        new_data.append(data_comp)
                else:            
                    data_as_dict, data_comp = self.scrap_profile(name, surname, profile_link)
                    data_list.append(data_as_dict)
                    new_data.append(data_comp)
        
        
\        with open('old_data.csv', 'w', newline='') as file1:
            writer = csv.DictWriter(file1, fieldnames=['Link', 'Skills', 'Title', 'Desc'])
            writer.writeheader()
            for i in range(0, len(new_data)):
                new_d = new_data[i]
                writer.writerow({'Link': new_d['Link'], 'Skills': new_d['Skills'], 'Title': new_d['Title'], 'Desc': new_d['Desc']})
        
\        file_name = str(datetime.datetime.now())[:10]+'.csv'
        with open(file_name, 'w', newline='') as file2:
            fieldnames = ['Name', 'Surname', 'Linkedin_profile', 'Count_contacts', 'Count_contacts_recruiter', 'Count_recommendations', 'Skills_updated', 'Title_updated', 'Description_updated']
            writer = csv.DictWriter(file2, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, len(data_list)):
                data = data_list[i]
                writer.writerow({'Name': data['Name'], 'Surname': data['Surname'], 'Linkedin_profile': data['Linkedin_profile'], 'Count_contacts': data['Count_contacts'], 'Count_contacts_recruiter': data['Count_cont_recruit'], 'Count_recommendations': data['Count_recommendations'], 'Skills_updated': data['Skills_updated'], 'Title_updated': data['Title_updated'], 'Description_updated': data['Description_updated']})
            
        self.driver.quit()
        print("Exiting...")


        