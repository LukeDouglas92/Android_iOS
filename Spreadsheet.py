import gspread
import os
import json
import pandas as pd
import xml.etree.ElementTree as xml
import os
import plistlib
import csv
import pip
import time
import sys, os, getopt, csv, xml.etree.ElementTree as ET
from xml.dom import minidom
import shutil
import tempfile
from oauth2client.service_account import ServiceAccountCredentials

print("LOADING...")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('Desktop/Localisation_Updater/Client_Secret.json', scope)
client = gspread.authorize(creds)

# define workbook locations get_worksheets are subsheets in the same doc
iOS = client.open("Localisation").sheet1
Android = client.open("Localisation").get_worksheet(1)
#Desktop = client.open("Localisation").get_worksheet(2)

#assign values locally
list_of_hashes = iOS.get_all_values()
list_of_hashes2 = Android.get_all_values()
#list_of_hashes3 = Desktop.get_all_values()


#create dataframe from api data
df = pd.DataFrame(list_of_hashes)
df2 = pd.DataFrame(list_of_hashes2)
#df3 = pd.DataFrame(list_of_hashes3)

#create directory to place data downloaded
fileDestination = "Desktop/Localisation"

#delete file localisation for over-write alternative
if (os.path.exists(fileDestination)):
   
    tmp = tempfile.mktemp(dir=os.path.dirname(fileDestination))
    shutil.move(fileDestination, tmp)
    shutil.rmtree(tmp)

#create new subdirectories for easier file allocating and navigating
os.makedirs(fileDestination)
#path = 'Desktop/Localisation/Desktop'
#os.mkdir(path)
path = 'Desktop/Localisation/iOS'
os.mkdir(path)
path = 'Desktop/Localisation/Android'
os.mkdir(path)
path = 'Desktop/Localisation/Extras'
os.mkdir(path)

#Timestamp for end user to check when up to date .txt
clock = time.strftime("%I:%M:%S\n")
calender = time.strftime("%d/%m/%Y")

#with open("Desktop/Localisation2/Desktop.json") as Desktop_File:
#    Desktop_File.write(list_of_hashes3)


#write last update time
with open("Desktop/Localisation/Extras/LastUpdated.txt", "w") as text_file:
    text_file.write(clock)
    text_file.write(calender)

#write instructions for user to follow
with open("Desktop/Localisation/Extras/usage_directions.txt", "w") as Direction:
    Direction.write("- This working copy requires you to run from Desktop\n"
                    "- ensure python on the system\n"
                    "- in terminal enter:\n"
                    "- python desktop/localisation_updater/spreadsheet.py desktop/localisation\n"
                    "- Overwrite is currently not implemented, ensure files are deleted then repeat process to update language files/strings")

#converting fro df to csv
df.to_csv('Desktop/Localisation/Extras/1_iOS.csv', index=False, header=False, encoding='utf-8')
df2.to_csv('Desktop/Localisation/Extras/1_Android.csv', index=False, header=False, encoding='utf-8')
#df3.to_csv('Desktop/Localisation/Extras/1_Desktop.csv', index=False, header=False, encoding='utf-8')

#
#data = pd.read_csv("Desktop/Localisation/Extras/1_Desktop.csv")
#data_dict = {col: list(data[col]) for col in data.columns}

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

# Read in output directory
try:
    fileDestination = "Desktop/Localisation"
except IndexError:
    print "Error: Please supply an output directory."
    print "Usage: converter.py [FILEPATH]"
    sys.exit()

# Create directory if it doesn't exists
# Read from csv
f = open('Desktop/Localisation/Extras/1_iOS.csv')
csv_f = csv.reader(f)
g = open('Desktop/Localisation/Extras/1_Android.csv')
csv_g = csv.reader(g)
#h = open('Desktop/Localisation/Extras/1_Desktop.csv')
#csv_h = csv.reader(h)

# Determine the number of languages from the csv
line1 = csv_f.next()
numberOfLocales =  len(line1)
line2 = csv_g.next()
numberOfLocales2 =  len(line2)
#line3 = csv_h.next()
#numberOfLocales3 = len(line3)


# Create strings for each language
for x in range(1, numberOfLocales):
    #Returns to the start of the csv and ignores the first line
    f.seek(0)
    csv_f.next()
    rowIndex = 0
    
    # Android xml
    resources = ET.Element("resources")
    
    # Create iOS strings file
    iOSFile = open(fileDestination+"/"+"iOS"+"/"+line1[x]+".Strings", "w+")
    for row in csv_f:
        ++rowIndex
        try:
            
            # Write string to xml
            ET.SubElement(resources, "string", name=row[0]).text = row[x].decode('utf-8')
            # Write string to iOS .Strings
            iOSFile.write('"'+row[0]+'"'+ ' = ' + '"'+row[x]+'"' + ";\n")
        except IndexError:
            f.seek(0)
            print "There is a problem with the csv file at row {}".format(rowIndex+1) + " with the language {}".format(line1[x])
            r = list(csv_f)
            print r[rowIndex]
            sys.exit()


for y in range(1, numberOfLocales2):
#Returns to the start of the csv and ignores the first lin
    g.seek(0)
    csv_g.next()
    rowIndex = 0
    resources = ET.Element("resources")
    androidCopy = open(fileDestination+"/"+"Android"+"/"+line2[y]+".xml", "w+")
    
    for row in csv_g:
        ++rowIndex
        try:
            ET.SubElement(resources, "string", name=row[0]).text = row[y].decode('utf-8')
            androidCopy.write('"'+row[0]+'"'+ ' = ' + '"'+row[y]+'"' + ";\n")
        except IndexError:
            g.seek(0)
            print "There is a problem with the csv file at row {}".format(rowIndex+1) + " with the language {}".format(line2[y])
            r = list(csv_g)
            print r[rowIndex]
            sys.exit()
        androidCopy = open(fileDestination+"/"+"Android"+"/"+line2[y]+".xml", "w+")
        androidCopy.write(prettify(resources).encode('utf-8'))


#for z in range(1, numberOfLocales3):
    #Returns to the start of the csv and ignores the first lin
#   h.seek(0)
#   csv_h.next()
#   rowIndex = 0
#   resources = ET.Element("resources")
#   DesktopCopy = open(fileDestination+"/"+"Desktop"+"/"+line3[z]+".json", "w+")
#
#   for row in csv_h:
#       ++rowIndex
#       try:
#           ET.SubElement(resources, "string", name=row[0]).text = row[z].decode('utf-8')
#           DesktopCopy.write('{'+row[0]+'}'+ ' = ' + '{'+row[z]+'}' + ";\n")
#       except IndexError:
#           h.seek(0)
#           print "There is a problem with the csv file at row {}".format(rowIndex+1) + " with the language {}".format(line3[z])
#           r = list(csv_h)
#           print r[rowIndex]
#           sys.exit()
#       DesktopCopy = open(fileDestination+"/"+"Desktop"+"/"+line3[z]+".json", "w+")
#       json.dump(data_dict, DesktopCopy)

print("Translation Files added")



