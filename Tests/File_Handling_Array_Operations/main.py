
from FileProcessor import FileProcessor
import os

if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    sample_directory = os.path.join(base_path,'..\samples')

    file_processor = FileProcessor(sample_directory)

    file_processor.list_folder_contents('', True)

    report_path = os.path.join(base_path,'report.txt')
    file_processor.read_csv("sample-02-csv.csv", report_path,True)

    file_processor.read_dicom(
        filename="sample-02-dicom.dcm",
        tags=[(0x0008,0x0016)], 
        extract_image=True,
        # extract_with_mean=False
    )
