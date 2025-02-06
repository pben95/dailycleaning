import pandas as pd
import glob
import os
from datetime import datetime, timedelta

txt_files = [f for f in glob.glob(os.path.join("input", "*.txt"))]  #Add data files to "input" folder

daily_names = [
    "CERT-NY",
    "CERT-MD",
    "CERT-IL",
    "RECERT-NY",
    "RECERT-MD",
    "RECERT-IL",
    "POST-NY",
    "POST-PA",
    "POST-MD",
    "POST-MA",
    "CORP-NY",
    "CORP-MD",
    "CORP-IL"
]

base_date_str = datetime.today().strftime('%m/%d/%Y')
base_date = datetime.strptime(base_date_str, '%m/%d/%Y')

#split parent folder from file path, remove spaces and compare with names in daily_names to try and match daily
def select_daily():
    while True:
        for k, v in enumerate(daily_names):
            print("(" + str(k) + "): " + v)
        print("Date: " + str(base_date.strftime('%m/%d/%Y')))
        print("File to be cleaned: " + str(file))
        daily_selection = input("Enter the number corresponding to the daily being cleaned, or 'd' to change the date: ").strip()
        if daily_selection == "d":
            select_date()
        try:
            return daily_names[int(daily_selection)]
            break
        except ValueError:
            print("Invalid daily selected, please try again.")

def select_date():
    while True:
        base_date_str = input("Please enter date in MM/DD/YYYY format: ").strip()
        try:
            base_date = datetime.strptime(base_date_str, '%m/%d/%Y')
            break
        except ValueError:
            print("Invalid date, please try again.")

for file in txt_files:  #Iterates through all data files from "input"
    input_file = pd.read_csv(file, dtype=str, delimiter=';', header=None)  #Input files are semicolon delimited
    selected_name = select_daily()
    new_file = pd.DataFrame()
    new_file[0] = input_file[0]
    new_file.insert(1, 'noticedate', base_date.strftime('%m/%d/%Y'))  #Uses date from "date.txt"
    new_file.insert(2, 'responsedate', (base_date + timedelta(days=14)).strftime('%m/%d/%Y'))  #14 days after "date.txt"
    new_file[3] = input_file[1]
    new_file[4] = input_file[2].fillna('') + ' ' + input_file[3].fillna('')  #Concats address1 and address2
    new_file[4] = new_file[4].str.strip()  #Strips spaces
    new_file[5] = input_file[4]
    new_file[6] = input_file[5]
    new_file[7] = input_file[6].astype(str)
    new_file[7] = new_file[7].apply(lambda x: x.zfill(5) if len(x) < 5 else x)
    new_file.columns = ['docid', 'noticedate', 'responsedate', 'company', 'address', 'city', 'state', 'zip']  #Headers
    output_name = selected_name + "-" + str(base_date.strftime('%m-%d-%Y')) + "-" + "cleaned.txt"
    output_dir = "output/" + str(base_date.strftime('%m-%d-%Y'))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_name)  #Creates path
    new_file.to_csv(output_file, sep='\t', index=False)  #Saves cleaned file
    print("Data cleaning completed successfully!")
