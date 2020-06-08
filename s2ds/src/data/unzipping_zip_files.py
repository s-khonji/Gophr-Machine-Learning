from zipfile import ZipFile
import os
import utils
#unzip_dir = utils.path_to('src', 'data')
# Create a ZipFile Object and load sample.zip in it
def unzipping_zip_files(file_name, unzip_dir = utils.path_to('data', 'external')):
   file_path = os.path.join(unzip_dir,file_name)
   with ZipFile(file_path, 'r') as zipObj:
   # Extract all the contents of zip file in current directory
      zipObj.extractall(unzip_dir)
   return(print('file unzipped'))