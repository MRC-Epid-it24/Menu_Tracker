import json

import requests

from define_collection_wave import folder
from helpers import create_folder, PDFDownloader

fg_path = create_folder('51_FarmhouseInns', folder)

# url found at https://www.greeneking.co.uk/pubs/greater-london/silver-cross/menu
url_fordownload = 'https://gkbr-p-001.sitecorecontenthub.cloud/api/public/content/79cdd03c480f4c4e855af2cc9e21ae72?v=f3ecf597'
print("Downloading:", url_fordownload)
filePath = fg_path + '/' + url_fordownload.split('/')[-1]
PDFDownloader(url_fordownload, filePath=filePath)