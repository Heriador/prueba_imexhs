import logging
import os
from datetime import datetime
import csv
from collections import Counter
from exceptions import IncorrectFileFormatException
import pydicom
import matplotlib.pyplot as plt
import numpy as np
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
                raise IncorrectFileFormatException()
            
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
            
    def read_dicom(self,filename,tags = [], extract_image = False,extract_with_mean = True):
        file_path = os.path.join(self.__base_path,filename)
        print("DICOM Analysis:\n")
        try:
            if not filename.endswith('.dcm'):
                raise IncorrectFileFormatException()
            
            file_dicom = pydicom.dcmread(file_path)

            #Printing the patient name, study date and modality of the DICOM file
            print(f"Patient Name: {file_dicom.PatientName}")

            #Converting the study date to a readable format
            study_date = datetime.strptime(file_dicom.StudyDate, "%Y%m%d")
            print(f"Study date {study_date.strftime('%d/%m/%Y')}")
            print(f"Modality: {file_dicom.Modality}")

            #Printing the additional tags if they are provided
            if len(tags) > 0:
                for tag in tags:
                    element = file_dicom.get(tag, None)
                    
                    print(f'Tag {hex(tag[0])}, {hex(tag[1])} = {element.name}: {element.value}')
            if extract_image:
                #Extracting the pixel data from the DICOM file
                image_path = file_path.replace('.dcm','.png')
                self.__Dicom_to_image(file_dicom, image_path,extract_with_mean)

                
        except FileNotFoundError as e:
            logging.error(f'File not found: {e}')
            return
        except Exception as e:
            logging.error(f'Error: {e}')
            return None
        
    def __Dicom_to_image(self, file_dicom, image_path, extract_with_mean):
        pixel_data = file_dicom.pixel_array.astype(float)
        rescaled_image = (np.maximum(pixel_data,0)/pixel_data.max())*255 #Rescaling the pixel data to 0-255 float
        final_image = np.uint8(rescaled_image) #Converting the pixel data to uint8
        
        #Validating if the DICOM file is a multiframe file
        if file_dicom.NumberOfFrames:
            num_frames = file_dicom.NumberOfFrames

            #Convert the multiframe image to a 2D image by taking the mean of the frames in the image
            if extract_with_mean:
                mean_image = np.mean(final_image, axis=0)
                plt.imsave(image_path.replace('.png','_mean.png'),mean_image, cmap='gray')
            else:
                #Extracting the frames from the multiframe image and saving them as separate images
                for i in range(num_frames):
                    sub_image_path = image_path.replace('.png',f'_frame_{i+1}.png')
                    plt.imsave(sub_image_path,final_image[i], cmap='gray')
                
                image_path = image_path.replace('.png',f'_frame_*.png')
        else:
            #Saving the 2D image to a PNG file
            plt.imsave(image_path, final_image, cmap='gray')

        print(f"Extracted image saved to {os.path.relpath(image_path)}\n")
