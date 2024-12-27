import logging
import os
from datetime import datetime
import csv
from collections import Counter
from errors import IncorrectFileFormatError

class FileProcessor:
    def __init__(self,base_path):
        self.__base_path = base_path
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=f'{os.path.dirname(__file__)}/FileProcessor.log',
                            filemode='a')
        
    def __get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for file in filenames:
                file_dir = os.path.join(dirpath, file)
                total_size += os.path.getsize(file_dir)
        
        return total_size
    
    def __print_file_details(self, file, path, is_dir):
        size = self.__get_folder_size(path) if is_dir else os.path.getsize(path)
        size_mb = size/(1024*1024.0)
        last_modified_timestamp = os.path.getmtime(path)
        last_modified = datetime.fromtimestamp(last_modified_timestamp)
        print(f'{os.path.basename(path):<30} {"folder" if is_dir else "file":<10} {size_mb:<15.3f} {last_modified.strftime("%Y-%m-%d %H:%M:%S"):<15}')
                
    
        
    def list_folder_contents(self,folder_name,details=False):
        try:
            list_dir = os.path.join(self.__base_path,folder_name)
            print(f'\nFolder: {os.path.relpath(list_dir)}')
            files = os.listdir(list_dir)
            print('Total elements:',len(files),'\n')

            if details:
                print(f'{"Name":<30} {"Type":<10} {"Size (MB)":<15} {"Last Modified":<15}')
            else:
                print(f'{"Name":<30} {"Type":<10}')

            print('\n')
            for file in files:
                path = os.path.join(list_dir,file)
                is_dir = os.path.isdir(path)

                if details:
                    self.__print_file_details(file, path, is_dir)
                else:
                    print(f'{file:<30} {"folder" if is_dir else "file":<10}')
            print('\n')
                

        except FileNotFoundError as e:
            logging.error(f'File not found: {e}')
            return 
        except Exception as e:
            logging.error(f'Error: {e}')
            return None
    
    def read_csv(self, filename, report_path = None, summary = False):
        print("CSV Analysis\n")
        try:
            #Reading the csv file using the csv library
            file = open(os.path.join(self.__base_path,filename), 'r')
            csv_reader = csv.reader(file)

            if(not report_path.endswith('.txt')):
                raise IncorrectFileFormatError()
            
            #Creating a report file if the report_path is provided
            report_path = open(report_path, 'w') if report_path else None


            #Extracting the headers and the data from the csv file
            data = list(csv_reader)
            headers = data[0]

            #Creating a list to store the average and standard deviation of the numeric columns
            average = [0.0 for _ in range(len(headers))]
            std = [0.0 for _ in range(len(headers))]

            #Calculating the average and standard deviation of the numeric columns

            #Iterating through the columns
            for i in range(len(headers)):
                #Verifying if the column is numeric
                if not data[1][i].isnumeric():
                    continue

                #Extracting the column and calculating the average and standard deviation
                column = [float(row[i]) for row in data[1:]]
                average[i] = sum(column)/len(column)
                std[i] = (sum([(x-average[i])**2 for x in column])/len(column))**0.5

            analysis_headers = f"Numeric Columns"

            #Printing the number of columns and the columns in the csv file, as well as the average and standard deviation of the numeric columns
            print(f"Number of columns: {len(headers)} ")
            print(f"Columns: {headers}")
            print(f"Rows: {len(data)-1}")
            print("\n"+analysis_headers)

            #if report_path is provided, writing the same information to the report file
            if report_path:
                report_path.write(analysis_headers+'\n')

            for i in range(len(headers)):
                if(average[i] == 0):
                    continue

                analysis_message = f"   - {headers[i]}: Average = {round(average[i],4):.2f}, Std Dev = {round(std[i],4):.2f}"
                
                #if report_path is provided, writing the average and standard deviation of the numeric columns to the report file
                if report_path:
                    report_path.write(analysis_message+'\n')

                #Printing the average and standard deviation of the numeric columns
                print(analysis_message)
            
            if summary:
                self.__print_non_numeric_summary(headers, data)

            if report_path:
                print(f"\nReport written to {os.path.relpath(report_path.name)}")
                report_path.close()

            print("\n")

        except FileNotFoundError as e:
            logging.error(f'File not found: {e}')
            return
        except Exception as e:
            logging.error(f'Error: {e}')
            return None
    
    def __print_non_numeric_summary(self, headers, data):
        print("\nNon-numeric columns summary:")
        non_numeric_columns = {}

        for i in range(len(headers)):
            if not data[1][i].isnumeric():
                non_numeric_columns[headers[i]] = [row[i] for row in data[1:]]
        
        for header, column in non_numeric_columns.items():
            counter = Counter(column)
            
            unique_values = len(counter.keys())
            print(f'   - {header}: Unique values = {unique_values}')
            
