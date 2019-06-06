# ArcGIS Online Backup Script
#script must be run in Python 3

#script based on: "https://community.esri.com/thread/208467-download-feature-service-as-file-geodatabase"
#note: This will delete a temporary geodatabase created in ArcGIS onlne via this script


import time
import os
import zipfile
import arcgis.gis
from zipfile import ZipFile

### *** modify these four lines ***
outputFolder=r"C:\Backups\" #where the GDB will be extracted to
gis = arcgis.GIS("http://maps.arcgis.com", "Username", "password") #replace these with your credentials
item_id='000000000000' #repace with the service_ID of the hosted feature layer to download
timestr = time.strftime("%Y%m%d")
GDBname = ("GeoDatabase_"+timestr) # name of the temporary GDB to be saved in ArcGIS Online
print("Logged in as " + str(gis.properties.user.username))

AGOLitem = gis.content.get(item_id)

print ("Exporting Hosted Feature Layer...")
AGOLitem.export(GDBname,'File Geodatabase', parameters=None, wait='True')
time.sleep(60)#add 10 seconds delay to allow export to complete

search_fgb = gis.content.search(query = "title:{}*".format(GDBname )) #find the newly created file geodatabase in ArcGIS online
fgb_item_id = search_fgb[0].id
fgb = gis.content.get(fgb_item_id)
fgb.download(save_path=outputFolder) #download file gdb from ArcGIS Online to your computer

print ("Zipping exported geodatabase for download...")

'''while statement runs until a valid zipped file is created'''
# randomly the output is a 1 KB file that is not a valid zipped file.
# The while statement forces a valid zipped file to be created.
zipfullpath=os.path.join(outputFolder,GDBname+".zip")#full path to the zipped file once it is downloaded to your computer
while  zipfile.is_zipfile(zipfullpath)==False:
    fgb.download(save_path=outputFolder)
zf = ZipFile(os.path.join(outputFolder,GDBname+ ".zip"))

# print ("Extracting zipped file to geodatabase...")
# zf.extractall(path=os.path.join(outputFolder)) #note: GDB file name is completely random ex. 225eddc131ad4f8cbf4c54e1414bd129.gdb)
# ##a new gdb is created each time the line above is run
#
# #get names of files in zipped folder.
# with ZipFile(zipfullpath, 'r') as f:
#     FilenamesInZip=f.namelist()
#     for name in FilenamesInZip:
#         if '.gdb/' in name:
#             gdbname=str(name).split("/", 1)[0]
# print ("Exported geodatabase is named: "+gdbname) #returns name of the exported gdb
#
# '''delete zipped file in ArcGIS Online '''
# del zf #deletes the zf vairable so the lock file goes away
# print("Deleting "+os.path.join(outputFolder,GDBname+".zip"))
# os.remove(zipfullpath) #deletes actual zipped file on your computer

'''deleting hosted File Geodatabase'''
###  NOTE: This will delete the temporary File Geodatabase in ArcGIS Online
print("Deleting "+fgb.title+"("+fgb.type+")"+" from ArcGIS Online...")
fgb.delete()


print("Done!")
