from tqdm.auto import tqdm
import shutil
import requests
from datetime import datetime
import re

#https://sun9-69.userapi.com/impg/c857524/v857524768/1e09ce/yLpbzQlBWFQ.jpg?size=224x240&quality=96&sign=61dbaf8eeda2134a1083d723b3b7fb71
#https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg
#https://wallpaperaccess.com/full/508751.jpg
#https://img3.akspic.ru/attachments/crops/1/5/6/9/6/169651/169651-skorpion-grafika-zoloto-art-simmetriya-7680x4320.jpg
#http://ipv4.download.thinkbroadband.com/50MB.zip

fileUrl = input("File url: ")

                                                                                                    #Check for file size (if size > 1gb then exit)
contentLength = requests.head(fileUrl).headers.get('content-length', None)
if (int(contentLength) > 100000000):
    print("File can't be downloaded! (Too big file size!)")
    exit()
                                                                                                    #Check for file name (if name can't be found in header then name file by current date+time )
if (not requests.head(fileUrl).headers.get('content-disposition')):
    now = datetime.now()
    fileName = now.strftime("%d-%m-%Y(%H-%M-%S)")
    fileExtension = requests.head(fileUrl).headers.get('content-type').split('/',1)[1]
    fileName = fileName + '.' + fileExtension
else:
    fileName = re.findall('filename=(.+)', requests.head(fileUrl).headers['content-disposition'])[0]
    fileName = fileName.replace('"','')
                                                                                                    #Downolad file and show progress bar with tqdm
with requests.get(fileUrl, allow_redirects=True, stream=True) as requesthandle:                     #get file form url
    with tqdm.wrapattr(requesthandle.raw, "read", total = int(contentLength), desc="") as rawData:  #downolad data from url with progress bar
        with open(fileName, 'wb') as downloadFile:                                                  #open or create file for write
            shutil.copyfileobj(rawData, downloadFile)                                               #copy downloaded data into file
