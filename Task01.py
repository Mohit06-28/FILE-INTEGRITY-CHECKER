import hashlib
import os
import json

def generate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
         buf = file.read() 
         hasher.update(buf)
    return hasher.hexdigest()

def check_integrity(directory_path, old_report_path, new_report_path):
     old_report = json.load(open(old_report_path, 'r')) 
     new_report = {}

     for filename in os.listdir(directory_path): 
         file_path = os.path.join(directory_path, filename)
         if os.path.isfile(file_path): 
              new_report[filename] = generate_hash(file_path)

     with open(new_report_path, 'w') as file:
         json.dump(new_report, file)

     discrepancies = []
     for file in old_report: 
         if file not in new_report or old_report[file] != new_report[file]:
             discrepancies.append(file)

     return discrepancies

def main(): 
     directory_path = input("Enter the directory path to check: ") 
     old_report_path = 'integrity_report_old.json' 
     new_report_path = 'integrity_report_new.json'

     if not os.path.exists(old_report_path):
         print("Generating initial report...") 
         generate_initial_report(directory_path, old_report_path)
     else:
          discrepancies = check_integrity(directory_path, old_report_path, new_report_path)
          if discrepancies: 
            print("Discrepancies found in the following files:") 
            for file in discrepancies: 
                 print(file)
          else: 
             print("No discrepancies found.")

def generate_initial_report(directory_path, report_path): 
    report = {} 
    for filename in os.listdir(directory_path): 
         file_path = os.path.join(directory_path, filename) 
         if os.path.isfile(file_path): 
             report[filename] = generate_hash(file_path)   

    with open(report_path, 'w') as file: 
          json.dump(report, file) 

if __name__ == "__main__":
    main()                          

