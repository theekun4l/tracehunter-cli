import re
import json
import os
import copy
from unicodedata import category
imf_dict = {'📧Emails' : set(),
            '📞Phone numbers' : set(),
            '🌐Urls' : set(),
             '📢Ip addresses' : set()  }
def analyze_file(path):
    global imf_dict
    for keys in imf_dict:
         imf_dict[keys].clear()
    if os.path.exists(path):
        print("File loaded successfully!")
        print("Scanning...")
        with open(path,'r') as file_reader:
            content = str(file_reader.readlines()) #readlines poora content list ki form mai deta hai and find all ko string chahiye hoti hai toh typecast karke string mai convert kardia
        if len(content) == 0:
            print("File is empty.")
        else:
           ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
           email_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
           phone_pattern = r"\+91\s[6-9][0-9]{9}"
           url_pattern = r"\b(https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
           email_compile = re.compile(email_pattern)
           phone_compile = re.compile(phone_pattern)
           url_compile = re.compile(url_pattern)
           ip_compile =  re.compile(ip_pattern)
           ips = re.findall(ip_compile,content)
           for ips_iteratar in ips:
                   imf_dict['📢Ip addresses'].add(ips_iteratar)
           emails = re.findall(email_compile,content)
           for email_iterator in emails:
                   imf_dict['📧Emails'].add(email_iterator.lower())
           phone = re.findall(phone_compile,content)
           for phone_iterator in phone:
                   imf_dict['📞Phone numbers'].add(phone_iterator)
           urls = re.findall(url_compile,content)
           for url_iterator in urls:
                   imf_dict['🌐Urls'].add(url_iterator.lower())   
           print("Scan Done!!")       
    else:
        print("Error : File don't exist!! Give right path.")
    
def user_validation1(number):
          a = number
          while True:
            if a == 1:
                user_validation7 = input("Do you want to export results to a JSON file? (y/n): ")
                user_validation7 = user_validation7.lower()
                if user_validation7 == 'y':
                    return True
                elif user_validation7 == 'n':
                    print("Going back to menu...")
                    return False
                else:
                    print("Invalid Input!! Try Again.")
                    continue
            elif a == 2:
                user_validation_2 = input("Given file name already exists do you want to overwite the all over data(y/n)? ")
                user_validation_2 = user_validation_2.lower()
                if user_validation_2 == 'y':
                    return True
                elif user_validation_2 == 'n':
                    print("Going backstep...")
                    return False
                else:
                    print("Invalid Input!! Try Again.")
                    continue
                 
def file_checker(file):
     return os.path.exists(file)
     
     
def file_maker():
     global imf_dict
     while True:
        file_name = input("Enter file name (without extension or press Enter to cancel): ")
        if file_name == '':
            print("Going back to menu...")
            return False #loop break karne ke liye
        else:
             file_name = file_name + '.json'
             flag3 = file_checker(file_name)
             temp_dict = copy.deepcopy(imf_dict)
             for keys in temp_dict:
                temp_dict[keys] = list(temp_dict[keys])
             if flag3 == True:
                    flag1 = user_validation1(2)
                    if flag1 == True:
                            print("Exporting results...")
                            with open(file_name,'w') as file_updater:
                                    json.dump(temp_dict,file_updater,indent=4)
                            print(f"{file_name} is successfully overwritten")
                            return False #main function ka loop break karne ke liye
                    else:
                            continue
             else:
                    print("Exporting results...")
                    with open(file_name,'x') as new_file_maker:
                            json.dump(temp_dict,new_file_maker,indent=4)
                    print(f"File saved successfully as {file_name}")
                    return False
def main_menu():
    print('''
1) Analyze new file
2) View analysis summary
3) Search extracted data
4) Export Results (JSON)
5) Exit''')
while True:
    print("==========================")
    main_menu()
    try:
        User_input = int(input("Enter your choice from (1-5): "))
    except ValueError:
        print("Invalid input!! Try again.")
        continue
    print("==========================")
    if User_input == 1:
        file_name = input("Enter your file name or full path: ")
        analyze_file(file_name)
        continue
    elif User_input == 2:
        print("--- Analysis Summary ---")
        print(f"Total Emails found : {len(imf_dict['📧Emails'])}")
        print(f"Total Phone Numbers found : {len(imf_dict['📞Phone numbers'])}")
        print(f"Total URLs found : {len(imf_dict['🌐Urls'])}")
        print(f"Total IP Addresses found : {len(imf_dict['📢Ip addresses'])}")
        continue
    elif User_input == 3:
         if not any(imf_dict.values()):
              print("You haven't stored any file!! First store it.")
              continue 
         else:   
            user_search = input("What do you want to search: ")
            user_search = user_search.lower()
            no_of_resultandcategory = {}
            for keys in imf_dict:
                 for item in imf_dict[keys]:
                    if user_search in item:
                        if keys not in no_of_resultandcategory:
                             no_of_resultandcategory[keys] = []
                             no_of_resultandcategory[keys].append(item)
                        else:
                             no_of_resultandcategory[keys].append(item)
            if len(no_of_resultandcategory) == 0:
              print("Not Found!!")
              continue
            else:
              print("🔍 Search Results")
              print("---------------------------")
              number = 0
              for i in no_of_resultandcategory:
                   number += len(no_of_resultandcategory[i])
              print(f"No. of matches {number}")
              print(f"Found!!")
              for keys in no_of_resultandcategory:
                   print(f"{keys}:")
                   for items in no_of_resultandcategory[keys]:
                        print(f"- {items}")
    elif User_input == 4:
            if not any(imf_dict.values()):
                 print("⚠️ No analysis data available to export")
                 continue
            else:
                while True:
                    flag =  user_validation1(1)
                    if flag == True:
                            flag2 = file_maker()
                            if flag2 == False:
                                    break
                    else:
                            break
            continue
    elif User_input == 5:
         print("Session ended successfully.Happy Coding!")
         break
                   
              
                    
              