import wget
import requests
from bs4 import BeautifulSoup, NavigableString
from zipfile import ZipFile
import os
import json
from datetime import datetime
import pprint 
from config import *

class scrape_json:
    
    def __init__(self,url):
        
        self.url = url
        
    
    def get_link(self):
        url = self.url
        page = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(page.content, "html5lib")

        table = soup.find(TABLE)
        table_body = table.find(TBODY)
        recent_json_zip_tag = table_body.find_all(TR,ID_SCRAPER)
        
        recent_json_zip_link = recent_json_zip_tag[0].find(ANCHOR_TAG,href=True)
        
        return recent_json_zip_link[HREF]
    
    def file_download(self,download_link):
        file_name = wget.download(download_link)
        return file_name
    
    def file_extraction(self,file_name):
        with ZipFile(file_name, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
            zipObj.extractall()
        os.remove(file_name)
    def scrapper_class_main(self):
        self.file_extraction(self.file_download(self.get_link()))


class get_data_json:
    
    def get_json_file_name(self):
   
        path_to_json = os.getcwd()
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

        return json_files[0] 
    def read_json(self):
   
        path  = os.path.join(os.getcwd(),self.get_json_file_name())

        with open(path) as f:
            data = json.load(f)
    #     print(data.keys())
        return data
    
    

def get_keys(dl):
    keys_list = []
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)
    return keys_list

# keys = []

class wrangle_json_data:
    
       
    
    def convert_time_stamp(self,data,keys_list):

        try:
            print("-" * 60)
            print("TIME STAMP  PRINTING TASK 1")
            print("-" * 60)  
            data[keys_list[4]] = datetime.strptime(data[keys_list[4]][0:10], "%Y-%m-%d").strftime("%d/%m/%Y")
            print(data[keys_list[4]])
            
        except Exception as e:
            raise ValueError("Timestamp changed already format not match",e)
            
    def get_required_list(self,data,keys_list):
        print("-" * 60)
        print("ID LIST AND ASSIGNER LIST  PRINTING TASK 2")
        print("-" * 60)
        id_list = [key[CVE][CVE_DATA_META][ID] for key in data[keys_list[5]] ]
        assigner_list = [key[CVE][CVE_DATA_META][ASSIGNER] for key in data[keys_list[5]]]
        print("-" * 60)
        print("ID LISTPRINTING TASK 2")
        print("-" * 60)
        pprint.pprint(id_list, depth=1)

        print("-" * 60)
        print("ASSIGNER LIST  PRINTING TASK 2")
        print("-" * 60)
        pprint.pprint(assigner_list, depth=1)

        return id_list,assigner_list
    
    def to_json(self,data,keys_list):
#         print(keys_list)
       
        # Data to be written 
        id_list,assigner_list = self.get_required_list(data,keys_list)
        print("-" * 60)
        print("ID LIST AND ASSIGNER LIST DICTIONARY PRINTING TASK 3")
        print("-" * 60)
        
        dictionary ={ 
            "id" : id_list ,
            "assign" : assigner_list 

        } 
        pprint.pprint(dictionary)
       
        print("-" * 60)
        print("CREATING AN JSON OUTPUT  FILE OF TWO  LISTS TASK 4")
        print("-" * 60)

        # Serializing json 
        json_object = json.dumps(dictionary, indent = 2) 

        # Writing to output.json 
        with open("output.json", "w") as outfile: 
            outfile.write(json_object) 
            
   
    
def main():
    try:
        scrape_json(URL).scrapper_class_main()

        wrangle_json_data().convert_time_stamp(get_data_json().read_json(),get_keys(get_data_json().read_json()))

        wrangle_json_data().to_json(get_data_json().read_json(),get_keys(get_data_json().read_json()))
    
    except Exception as e:
        
        raise ValueError(f"pls check the error{e}")
    

if __name__ == "__main__":
    main()