
from FileProcessor import FileProcessor
import os

if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    sample_directory = os.path.join(base_path)
    file_processor = FileProcessor(sample_directory)
    file_processor.list_folder_contents('', True)