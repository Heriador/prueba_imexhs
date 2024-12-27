import logging
import os
from datetime import datetime

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
    
    