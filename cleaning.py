import pandas as pd
import glob
import os
from datetime import datetime, timedelta

txt_files = [f for f in glob.glob(os.path.join("input", "*.txt"))]  #Add data files to "input" folder

os.makedirs("output", exist_ok=True)  #Cleaned files are saved to "output" folder

with open('date.txt', 'r') as file:  #Date is pulled from "date.txt"
    base_date_str = file.readline().strip()
base_date = datetime.strptime(base_date_str, '%m/%d/%Y')

for file in txt_files:  #Iterates through all data files from "input"
    input_file = pd.read_csv(file, delimiter=';', header=None)  #Input files are semicolon delimited
    new_file = pd.DataFrame()
    new_file[0] = input_file[0]
    new_file.insert(1, 'noticedate', base_date.strftime('%m/%d/%Y'))  #Uses date from "date.txt"
    new_file.insert(2, 'responsedate', (base_date + timedelta(days=14)).strftime('%m/%d/%Y'))  #14 days after "date.txt"
    new_file[3] = input_file[1]
    new_file[4] = input_file[2].fillna('') + ' ' + input_file[3].fillna('')  #Concats address1 and address2
    new_file[4] = new_file[4].str.strip()  #Strips spaces
    new_file[5] = input_file[4]
    new_file[6] = input_file[5]
    new_file[7] = input_file[6]
    new_file.columns = ['docid', 'noticedate', 'responsedate', 'company', 'address', 'city', 'state', 'zip']  #Headers
    output_file = os.path.join("output", f"{os.path.splitext(os.path.basename(file))[0]}_cleaned.txt")  #Creates path
    new_file.to_csv(output_file, sep=';', index=False)  #Saves cleaned file
    print("Data cleaning completed successfully!")
