#url = 'https://www.freemaptools.com/download/outcode-postcodes/postcode-outcodes.csv'
#url = 'https://datashare.is.ed.ac.uk/bitstream/handle/10283/2597/GB_Postcodes.zip?sequence=1&isAllowed=y'
import urllib
import requests
import os
import utils
#download_dir = utils.path_to('src', 'data')
#file_name = 'GB_Postcodes.zip'
def downloading_scripts(file_name,url,download_dir=utils.path_to('data', 'external')):
    download_path = os.path.join(download_dir,file_name)
    utils.ensure_directories(download_path)
    urllib.request.urlretrieve(url, download_path)
    return(print('file downloaded'))
# r = requests.get(url)
# with open("vasan-downloads1.csv", "wb") as code:
#     code.write(r.content)
if __name__ == "__main__":
    """
    """
    pass