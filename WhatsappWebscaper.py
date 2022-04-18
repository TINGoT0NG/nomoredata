from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import base64
import time
from datetime import datetime 
import os
import os.path
import glob 
import zipfile
import re
import shutil
import datetime
from pathlib import Path
from urllib.parse import urlparse
import threading
import keyboard

# def press_Enter():
#     while True:
#         try:
#             if thread_check == 1:
#                 keyboard.press('enter')
#                 time.sleep(30)
#         except:
#             pass
#     t_thread = threading.Thread(target=press_Enter)
#     t_thread.start()


class Scraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized") 
        chrome_options.add_argument("disable-infobars")
#         chrome_options.add_argument("disable-extensions")
#         chrome_options.add_argument("disable-gpu")
#         chrome_options.add_argument("disable-dev-shm-usage") 
#         chrome_options.add_argument("no-sandbox") 

        chrome_options.add_argument("--window-size=1366x768")
        chrome_options.add_argument("user-data-dir=/User Data/Default/Cookies") #transferred cookie to the folder
        #chrome_options.add_argument("user-data-dir=~/Library/Application Support/Google/Chrome/Default/Cookies") #read into cookie
        #chrome_options.add_argument("C:\\Users\\Evergreen\\AppData\\Local\\Google\\Chrome\\")
        #chrome_options.add_argument("disable-infobars")
        download_dir = os.getcwd()
        prefs = {"download.default_directory" : ""+download_dir+""}
        chrome_options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(options=chrome_options)
        print("Opening Whatsapp Web Window")
        self.driver.get('https://web.whatsapp.com')
        print("Scan Your QR Codes and Press Enter (Press Enter if You're Already Logged In)")
        input()  
        
    def latest_download_file(self):
        path = os.getcwd()
        os.chdir(path)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]

        return newest   


    def scrapeImages(self, AMOUNT):
        try:
            if(AMOUNT == "Single"):
                try: 
                    print("Please Input a Contact Name (case sensitive) : ")
                    contact_name_final = input()
                    contact_final = WebDriverWait(self.driver,10).until(lambda driver: self.driver.find_element_by_xpath("//span[@title=\""+contact_name_final+"\"]"))
                except:
                    #print("Searching for " + contact_name_final + " in the search bar")
                    #search_box_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]'
                    #print("xpath initialised")
                    #search_box = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(search_box_xpath))
                    #search_box = self.driver.find_elements_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
                    #print("found search box")
                    #print(search_box)
                    #search_box.click()
                    #print("clicked")
                    #search_box.send_keys(contact_name_final)
                    #print("Sent keys")
                    search_box_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]'
                    search_box = WebDriverWait(self.driver,20).until(lambda driver: self.driver.find_element_by_xpath(search_box_xpath))
                    search_box.click()
                    search_box.send_keys(contact_name_final)                    
                    time.sleep(2)
                    contact_final = self.driver.find_element_by_xpath("//span[@title=\""+contact_name_final+"\"]")
                    #contact_name_final = contact_final.text
            else:
                try:
                    print("searching contacts test")
                    #contact_names = WebDriverWait(self.driver,15).until(lambda driver: self.driver.find_elements_by_xpath(('//div[contains(@class, "zoWT4")]//span[@class="_ccCW FqYAR i0jNr"]')))
                    contact_names = WebDriverWait(self.driver, 15).until(lambda driver: self.driver.find_elements_by_class_name('zoWT4'))
                    print("contact 1")
                except:
                    contact_names = WebDriverWait(self.driver,15).until(lambda driver: self.driver.find_elements_by_xpath(('//span[contains(@class, "_3q9s6")]//span[@class="_ccCW FqYAR i0jNr"]'))) #search single contact chats
                print("Searching all Contacts")
                
                contact_final = contact_names[len(contact_names)-1]
                contact_name_final = contact_names[len(contact_names)-1].text
                    
            
            time.sleep(2)
            print("Contact Found: ",contact_name_final)
            
            
            contact_final.click()

            action = ActionChains(self.driver)
            self.driver.execute_script("arguments[0].scrollIntoView();", contact_final)
            
            #start the thread to press enter
            #thread_check = 1
            
            # Scrolling up. Get initial html content of chat window -> run through for loop for certain time.
            # //div[@class="_3Iosq"] exists until no more content to load ( FOund this out later XD, could prob simplify code]
            # Then compare html content and see whether any change. If no change stop scrolling up.
            
            # POST UPDATE _33LGR in, out _1gL0z, dont know if correct swap.  _3Iosq in, out _2hDby. NOT sure if correct
            
            while True:
                #break; #GET RID OF THIS LATER
                content = self.driver.find_element_by_class_name('_33LGR')
                #html_content_x = content.get_attribute('innerHTML')
                for i in range(0, 4):
                    self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.HOME)
                    time.sleep(0.5)
                    self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.END)
                    try:
                        loading_content = self.driver.find_elements_by_xpath('//div[@class="_3Iosq"]')
                        time.sleep(0.5)
                    except:     
                        time.sleep(0.5)
  
                content = self.driver.find_element_by_class_name('_33LGR')
                #html_content_y = content.get_attribute('innerHTML')
                self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.HOME)
                time.sleep(0.5)
                
                #if ((html_content_x == html_content_y) and (not loading_content)):
                if not loading_content:
                    break;   
            
            # Same method for scrolling down
            while True:
               # break; #GET RID OF THIS LATER
                content = self.driver.find_element_by_class_name('_33LGR')
                html_content_x = content.get_attribute('innerHTML')
                for i in range(0, 4):
                    self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.END)
                    time.sleep(0.5)

                content = self.driver.find_element_by_class_name('_33LGR')
                html_content_y = content.get_attribute('innerHTML')
                self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.END)
                time.sleep(0.5)
                if (html_content_x == html_content_y):
                    break;            
                
            #WebDriverWait(self.driver,20).until(lambda driver: self.driver.find_element_by_class_name('_33LGR').send_keys(Keys.CONTROL + Keys.HOME))
               # time.sleep(5)
            # POST UPDATE _23P3O in, out _2uaUb
            contact2 = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_class_name("_23P3O"))
            contact2.click()
            time.sleep(1)
        
        
            media_xpath = '//span[text()="Media, links and docs"]'
            media = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(media_xpath))
            media.click()
            time.sleep(2)
            
            WebDriverWait(self.driver,50).until(lambda driver: driver.find_element_by_xpath('//*[@title="Docs"]')).click()
            time.sleep(1)
            # POST UPDATE _18eKe in, out _18eKe
            WebDriverWait(self.driver,50).until(lambda driver: driver.find_element_by_xpath('//button[@class="_18eKe"]')).click()
            time.sleep(1)
            
            media = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(media_xpath))
            media.click()
            time.sleep(2)
            
            WebDriverWait(self.driver,50).until(lambda driver: driver.find_element_by_xpath('//*[@title="Docs"]')).click()
            time.sleep(1)
            
            num_images = 0
            i = 0
            #search for documents
##################################### FIXED EDGE CASE deleted documents HERE ################
            verified_document = False            
            ##Slight bug somewhere here and below for how it handles documents.
            try:
                # POST UPDATE _36BuW in, out _1-D-8 
                tiles2 = WebDriverWait(self.driver,10).until(lambda driver: self.driver.find_elements_by_xpath('//div[@class="_36BuW"]'))
                for i in range(0, len(tiles2)):
                    html_content_document = tiles2[i].get_attribute('innerHTML')
                    action = ActionChains(self.driver)
                    self.driver.execute_script("arguments[0].scrollIntoView();", tiles2[i])
                    action.move_to_element(tiles2[i]).move_by_offset(-182,0).click().perform() #this is wrong actually.
                    num_images += 1
                    time.sleep(0.05)
                    try:
                        if 'data-testid="audio-download"' in html_content_document:
                            verified_document = True
                    except:
                        pass

                print("Done Searching For Documents for "+contact_name_final+"")
            except:
                pass            
            print("verified_documents: ", verified_document)
            try:
                num_images = len(WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_elements_by_class_name("_36BuW")))
                #print('in try loop for _36BuW')
            except:
                pass
            
            # If no documents found
            if num_images == 0:
                print("No Documents found for "+contact_name_final)

            if (num_images != 0) and (verified_document== False):
                print ("removing deleted documents from DOCS")
                WebDriverWait(self.driver,2).until(lambda driver: self.driver.find_elements_by_xpath('//span[@data-testid="delete"]'))
                time.sleep(1)
           
            if (num_images != 0) and (verified_document== True):
                #print('in num_images != 0 statement')
                ##Download was previously here##
                print("checking if folder is created") 
##################################### APR 29 Changes finish HERE ################
                #create folder 
                currentDirectory = os.getcwd()
                folder_path = os.path.join(currentDirectory,"images\\" + contact_name_final)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    time.sleep(5)
                
                if not os.path.exists(currentDirectory + "\\" + "images\\" + "temp_file"):
                    os.makedirs(currentDirectory + "\\" + "images\\" + "temp_file")  
                    time.sleep(5)
                
                print("folder created checked")    
                # Download 
                # POST UPDATE _1fimr in, out _1toeX
                self.driver.find_element_by_xpath('//button[contains(@class,"_1fimr") and contains(@title,"Download")]').click()
                time.sleep(15)
                # Shifted download here
                    
                current_time = datetime.datetime.now()
                year = str(current_time.year)
                month = str(current_time.month)
                
                if( month != ("10" or "11" or "12")):
                    month = "0" + month

                if not os.path.exists(folder_path + "\\" + year + "\\" + month):
                    os.makedirs(folder_path + "\\" + year + "\\" + month)
                    time.sleep(5)
            
                if (num_images != 1):
                    # 1. search for folder name that contains string"WhatsApp Unknown"

                    ##FIX THE BELOW FOR DOCS, CAN REF IMAGES##
                    fileends = "none"
                    while fileends == "none":
                        zip_check = []
                        ## THE PROGRAM BROKE HERE, FIX IT LATER ##
                        for file in glob.glob("*.zip", recursive=False):
                            #print('in file in glob statement')
                            zip_check.append(file)
                            if len(zip_check) != 0:
                                myZip = zipfile.ZipFile(str(file))
                                fileends = 'zip'
                                print(zip_check)

                    new_folder_path = os.getcwd()
                    new_file_type = '\*zip'
                    new_files = glob.glob(new_folder_path + new_file_type)
                    max_file = max(new_files, key=os.path.getctime)

                    ## while something somethign
                    flag_zip = 1
                    num_filesinzip = len(zipfile.ZipFile.infolist(myZip))
                    myZip.close()
                    print("num_filesinzip: ",num_filesinzip)
                    ## get intial number of files in folder
                    path_init, dirs_init, files_init = next(os.walk(folder_path))
                    file_count_init = len(files_init)
                    print("file_count_init: ",file_count_init)
                    while(True):
                        for i in zip_check:
                            shutil.unpack_archive(i, folder_path + "\\" + year + "\\" + month)
                            flag_zip = 0    
                            path_fin, dirs_fin, files_fin = next(os.walk(folder_path + "\\" + year + "\\" + month))
                            file_count_fin = len(files_fin)
                            # check to see if all images have copied over
                            if(file_count_fin == file_count_init + num_filesinzip):
                                print("file_count_fin: ",file_count_fin)
                                break  
                        break
                                    
                                    
                                    
                        ### Buggy code below, rest in peace ###
#                     fileends = "none"
#                     while "none" == fileends:
#                         time.sleep(1)
#                         newest_file = scraper.latest_download_file()
#                         if "zip" in newest_file:
#                             fileends = "zip"
#                         else:
#                             fileends = "none"
                
#                     new_folder_path = os.getcwd()
#                     new_file_type = '\*zip'
#                     new_files = glob.glob(new_folder_path + new_file_type)
#                     max_file = max(new_files, key=os.path.getctime)

#                     with zipfile.ZipFile(max_file, 'r') as zip_ref:
#                         zip_ref.extractall(folder_path + "\\" + year + "\\" + month)
                        
                    #### Buggy Code ends here ###
                    
                    
                    
                    time.sleep(5)
                    os.remove(max_file)
                    time.sleep(2)
                else: # make exception for single file download (not zip file)
                    time.sleep(2)
                    arr = os.listdir()
                    # POST UPDATE _2vB9T _2QSxG _2HDxO, i0jNr in, out VtaVl -TvKO _3tOOP, _3-8er
                    substring = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath('//div[@class="_2vB9T _2QSxG _2HDxO"]//span[@class="i0jNr"]')).text
                    list_of_files = glob.glob(os.getcwd() + '\*') 
                    latest_file = max(list_of_files, key=os.path.getctime)
                    os.replace(os.getcwd()+ "\\" +  os.path.basename(latest_file), folder_path + "\\" + year + "\\" + month + "\\" + os.path.basename(latest_file))
                    #print(arr)            
                    time.sleep(2)

            print("Collecting media")
            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath('//*[@title="Media"]')).click()
            time.sleep(2)

            num_images = 0
            i = 0
            #search for images
            while True:
                try:
                    #POST UPDATE _3_8JL in, out i-d_o 
                    #25 Nov Update, _3_8JL out, _23fpc in
                    tiles3 = self.driver.find_elements_by_xpath('//div[@class="_23fpc"]')
                    for i in range(0, len(tiles3)):
                        action = ActionChains(self.driver)
                        self.driver.execute_script("arguments[0].scrollIntoView();", tiles3[i])
                        action.move_to_element(tiles3[i]).move_by_offset(-40,-40).click().perform()
                        num_images += 1
                        #time.sleep(0.05)   
                    try:
                        tiles3 = self.driver.find_elements_by_xpath('//div[@class="_23fpc"]')
                        action = ActionChains(self.driver)
                        #action.move_to_element(tiles2[0]).perform()                        
                        self.driver.execute_script("arguments[0].scrollIntoView();", tiles3[0])
                        action.move_to_element(tiles3[0]).move_by_offset(-40,-40).click().perform()
                    except Exception as e:      
                        time.sleep(2)
                        try:
                            print("searching for more images")
                            tiles3 = self.driver.find_elements_by_xpath('//div[@class="_23fpc"]')
                            action = ActionChains(self.driver)
                            self.driver.execute_script("arguments[0].scrollIntoView();", tiles3[0])
                            #action.move_to_element(tiles2[0]).perform()
                            #time.sleep(3)
                            action.move_to_element(tiles3[0]).move_by_offset(-40,-40).click().perform()
                        except Exception as e:
                            print("no more images found")
                            break;
                except Exception as e:
                    print("no more images found")
                    break;
            
            
            try:
                num_images = len(WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_elements_by_class_name("_23fpc")))
            except:
                pass
            
            # If no images found
            if num_images == 0:
                print("No media found for "+contact_name_final+"")
           
            if num_images != 0:
                # Download
                
                ##download was previously here##
            
                #create folder 
                currentDirectory = os.getcwd()
                folder_path = os.path.join(currentDirectory,"images\\" + contact_name_final)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    time.sleep(5)

                    ##Download shifted here##
                self.driver.find_element_by_xpath('//button[contains(@class,"_1fimr") and contains(@title,"Download")]').click()
                time.sleep(15)

                print("num_images: ",num_images)    
                if (num_images != 1):
                    # 1. search for folder name that contains string"WhatsApp Unknown"
                    
                    #folder_path = os.path.join(currentDirectory,"images\\" + contact_name_final)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        time.sleep(5)

                    if (num_images != 1):
                        fileends = "none"

                        #ADDING TIMER 29 APR
                        start_time = time.time()
                        seconds = 900

                        while fileends == "none":
                            zip_check = []
                            for file in glob.glob("*.zip", recursive=False):
                                zip_check.append(file)
##################################################################################### 29APR
                                current_time = time.time()
                                elapsed_time = current_time - start_time
                                if elapsed_time > seconds:
                                   print("Download failed, Return to search for contacts")
                                   if (AMOUNT == "Multiple"):
                                       scraper.scrapeImages("Multiple")
                                   else:
                                       scraper.scrapeImages("Single")    
########################################################################################
                                if len(zip_check) != 0:
                                    myZip = zipfile.ZipFile(str(file))
                                    fileends = 'zip'
                                    print(zip_check)

                        new_folder_path = os.getcwd()
                        ### CHECK ABOVE ### ### FIX ###
                        new_file_type = '\*zip'
                        new_files = glob.glob(new_folder_path + new_file_type)
                        max_file = max(new_files, key=os.path.getctime)

                        ## while something somethign
                        #flag_zip = 1

                        ## get intial number of files in folder
                        ##there is probably a problem here
                        
                        #new zip code
                        # num_zipfiles = *run script*
                        # oh i dunno what the below code does
                        
                        # targert folder = folder_path -< just so i remembere extracting it to here /images/%contact_name%
                        # if(file_count_fin == file_count_init + num_filesinzip :
                        # break;

                        flag_zip = 1
                        path_init, dirs_init, files_init = next(os.walk(folder_path))
                        ## Problem might be the os.walk()? ## ## FIX IT LATER ##
                        
                        num_filesinzip = len(zipfile.ZipFile.infolist(myZip)) #can we close here?
                        myZip.close() #attempt to close it
                        print("num_filesinzip: ",num_filesinzip)
                        file_count_init = len(files_init)
                        print("file_count_init: ",file_count_init)
                        while(True):
                            ##something something throw back to attempt to unzip?
                            for i in zip_check:
                                shutil.unpack_archive(i, folder_path)
                                flag_zip = 0    
                                path_fin, dirs_fin, files_fin = next(os.walk(folder_path))
                                file_count_fin = len(files_fin)
                                # check to see if all images have copied over
                                if(file_count_fin == file_count_init + num_filesinzip):
                                    print("file_count_fin: ",file_count_fin)
                                    break
                            break
                    ####
                    #below lies the buggy unzip code, may it rest in peace
                    # this is it,
                    
                    
                    
#                     fileends = "none"
#                     while "none" == fileends:
#                         time.sleep(1)
#                         newest_file = scraper.latest_download_file()
#                         if "zip" in newest_file:
#                             fileends = "zip"
#                         else:
#                             fileends = "none"
                
#                     new_folder_path = os.getcwd()
#                     new_file_type = '\*zip'
#                     new_files = glob.glob(new_folder_path + new_file_type)
#                     max_file = max(new_files, key=os.path.getctime)
        
#                     ## while something somethign
#                     flag_zip = 1
                
#                     ## get intial number of files in folder
#                     path_init, dirs_init, files_init = next(os.walk(folder_path))
#                     file_count_init = len(files_init)
#                     print("file_count_init: ",file_count_init)
#                     while(True):
#                             with zipfile.ZipFile(max_file, 'r') as zip_ref:
#                                 zip_ref.extractall(folder_path)
#                             flag_zip = 0    
#                             path_fin, dirs_fin, files_fin = next(os.walk(folder_path))
#                             file_count_fin = len(files_fin)
#                             # check to see if all images have copied over
#                             if(file_count_fin != file_count_init):
#                                 break;

                    # XD
                    time.sleep(10)
                    ##### CONSIDER BUILDING A CHECKER TO ENSURE ALL FILES ARE REMOVED ####
                    os.remove(max_file)
                else: # make exception for single file download (not zip file)
                    time.sleep(2)
                    arr = os.listdir() #working directory
                    substring = "WhatsApp"
                    strings2 = ([string1 for string1 in arr if substring in string1])
                    for i in range(0, len(strings2)):
                        os.replace(os.getcwd()+ "\\" +  strings2[i], folder_path + "\\" + strings2[i])
                    print("moving single file")
                    #time.sleep(1)
            

            #create folder 
            currentDirectory = os.getcwd()
            folder_path = os.path.join(currentDirectory,"images\\" + contact_name_final)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                    
        
            #move images into correct directory
            ##### CONSIDER BUILDING A CHECKER TO ENSURE ALL FILES ARE REMOVED ####
            while len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,name))]) != 0:
                print("files in path: ", len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,name))]))
                arr = os.listdir(folder_path)
                substring = "WhatsApp"
                strings2 = ([string1 for string1 in arr if substring in string1])
                for i in range(0, len(strings2)):
                    file_date = re.findall(r'\d+', strings2[i])
                    if not os.path.exists(folder_path + "\\" + file_date[0] + "\\" + file_date[1]):
                        os.makedirs(folder_path + "\\" + file_date[0] + "\\" + file_date[1])                
                    shutil.copy(folder_path + "\\" +  strings2[i], folder_path + "\\" + file_date[0] + "\\" + file_date[1])
                    os.remove(folder_path + "\\" +  strings2[i])
                time.sleep(1)
                print("in new implementation")
                print("files after cycle: ", len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,name))]))
         
            print("broke out of new implementation")
            time.sleep(20)    
            #Clearing and Archiving Chat
            print("Clearing and Archiving Chat")
            WebDriverWait(self.driver,50).until(lambda driver: driver.find_element_by_xpath('//button[@class="_18eKe"]')).click()
            #print("Clearing and Archiving Chat 1 ")
            time.sleep(1)
            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath('//span[@data-icon="x"]')).click()
            #print("Clearing and Archiving Chat 2")
            time.sleep(1)
            #first menu, _2n-zq out, _2cNrC in
            menu2 = WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_elements_by_css_selector('.\_1QVfy > div > .\_2cNrC > .\_26lC3 > span'))
            #print("Clearing and Archiving Chat 3")
            menu2[0].click()
            time.sleep(1)
            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_css_selector('div[aria-label="Clear messages"]')).click()
#            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_2n-zq _3zHcq"]//span//div//ul//li//div[@aria-label="Clear messages"]'))).click()
            #was the element changed?
            #<div class="_11srW _2xxet" role="button" aria-label="Clear messages">Clear messages</div>
            #//div[@id='a']//a[@class='click']
            #print("Clearing and Archiving Chat 4 ")
            time.sleep(2)
            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_css_selector(('.\_2Zdgs'))).click()
            #print("Clearing and Archiving Chat 5")
            time.sleep(2)
            action = ActionChains(self.driver)
            action.move_to_element(contact_final).move_by_offset(130,0).context_click().perform() # dodge the popupbox XD
            #print("Clearing and Archiving Chat 6")
            time.sleep(1)
            
            
            WebDriverWait(self.driver,50).until(lambda driver: self.driver.find_element_by_xpath(('//div[@aria-label="Archive chat"]'))).click()
            print("Clearing and Archiving Chat Successfully")
            #thread_check = 0
            
            #try: 
                #WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_2n-zq _3zHcq"]//span//div//ul//li//div[@aria-label="Clear messages"]'))).click()
            #except:
            #    WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_2n-zq _3zHcq"]//span//div//ul//li//div[@aria-label="Exit group"]'))).click()
                
            #time.sleep(2)
            
            #try: 
                #WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_3NCXc _1Yw2u _FUG3 _2HGw4"]//div[contains(text(),"Clear")]'))).click()
           # except:
            #    WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_3NCXc _1Yw2u _FUG3 _2HGw4"]//div[contains(text(),"Exit")]'))).click()
            #    time.sleep(3)
            #    menu2 =  WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_elements_by_xpath('//div[@class="_2n-zq"]//div[@title="Menu"]'))
            #    menu2[1].click()
            #    time.sleep(1)
            #    WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_2n-zq _3zHcq"]//span//div//ul//li//div[@aria-label="Delete group"]'))).click()
            #    time.sleep(2)
            #    WebDriverWait(self.driver,5).until(lambda driver: self.driver.find_element_by_xpath(('//div[@class="_3NCXc _1Yw2u _FUG3 _2HGw4"]//div[contains(text(),"Delete")]'))).click()
            
            

            
            print("Finished downloading all files for: "+contact_name_final+"")
            time.sleep(2)
            
            if (AMOUNT == "Multiple"):
                time.sleep(5)
                print("Searching for the next contact")
                scraper.scrapeImages("Multiple")
            else:
                return None
            
        except Exception as e:
            print(e)
            self.driver.quit()

    def quitDriver(self):
        print("Quit")
        self.driver.quit()

scraper = Scraper()

while True:

    print("Logged In")
    print("===================Menu=================")
    print("Please wait for Whatsapp to load page before selecting option below")
    print("Press '1' to search by contact name")
    print("Press '2' to search all contacts")
    print("Press '3' to quit")
    print("========================================")
    menu = input()
    #print(menu)
    if menu == '1':
        scraper.scrapeImages("Single")
    elif menu == '2': 
        scraper.scrapeImages("Multiple")
    elif menu == '3':
        scraper.quitDriver()
        break
