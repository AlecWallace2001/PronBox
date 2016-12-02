import subprocess
import os
import re
from decimal import *
import time

def Indexing():
    cWD = os.getcwd()
    fWD = os.getcwd() + '\Finished'
    files = os.listdir(fWD)
    catalogue = []
    for i in files:
         if i[:i.index(' ')] not in catalogue:
             
             catalogue.append(i[:i.index(' ')])
    cats = []
    for i in catalogue:
        iFixed = str(i).replace("+", "_")
        caturl = '<th><a href="file://localhost/' + str(cWD) + '/Site/' + i + '.html" style="color:#00FF00; font-size:48px">'+ iFixed +'</a></th>\n'
        nRow = '</tr><tr>\n'
        cats.append(caturl)
    cLinks = []
    for i in catalogue:
        iFixed = str(i).replace("+", "_")
        caturl = '<a href="file://localhost/' + str(cWD) + '/Site/' + i + '.html" style="color:#00FF00; font-size:48px">'+ iFixed +'</a><br>\n'
        cLinks.append(caturl)
    iHeader = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>PronBox Start</title>
</head>

<body BGCOLOR="#000000">
<div id="PronHeader" align="center">
<img src="PBHeader.png" width="794" height="208" alt=""/>
</div>
<div id="PronIntro" align="center">
<a style="color:#00FF00; font-size:20px;">Welcome to your personal curated pornsite.</a><br>
<a style="color:#00FF00; font-size:20px;">You can view the videos from your PronBox downloads by clicking on the category links below.</a><br><br>
</div>
<div id="LeftColumn" align="left">
<table border="2" width="90" align="center">
<col style="width:30%">
<col style="width:30%">
<col style="width:30%">
<tbody>
<tr>
"""
    iCloser = """</tr>
</table>
</body>
</html>"""
    
    header1 = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>PronBox Start</title>
</head>

<body BGCOLOR="#000000">
<div id="PronHeader" align=20%>
<img src="PBHeader.png" width="335" alt=""/>
</div>
<div id="PronIntro" align="center">
<a style="color:#00FF00; font-size:80px;">"""


    header2 = """</a><br><br>
</div>
<table border="2" width=100% align ="justify">
<col style="width:20%">
<col style="width:80%">
<tbody>
<tr>
<th valign="top">
"""

    mid1 = """
</th>
<th>
	<table border="2" width=100% align="Right">
	<col style="width:50%">
	<col style="width:50%">
	<tbody>
	<tr>"""
    
    closer = """</body> 
</html>



  
</body>

</html>"""

    vidOpen = '''<th><video width="600" controls>
  <source src="'''

    vidClose = '''" type="video/mp4">
</video></th>'''

    #Writing the index file
    indexes = open('Your PronBox.html', 'wb')
    indexes.write(iHeader)
    indexRuns = 1
    for i in cats:
        indexes.write(i)
        if indexRuns == 4:
            indexes.write(nRow)
            indexRuns = 0
        indexRuns +=1
    indexes.write(iCloser)
    indexes.close()
    
    #Writing the video files
    for i in catalogue:
        
        htmlName = os.getcwd() + '/Site/' + i +'.html'
        catIndexes = open(htmlName, 'wb')
        vFiles = []
        for h in files:
            if i in h:
                vFiles.append(h)
        catIndexes.write(header1)
        pName = i +' Porn'
        catIndexes.write(pName)
        catIndexes.write(header2)
        for i in cLinks:
            catIndexes.write(i)
        #catIndexes.write('<a href="file://localhost/' + str(cWD) + '/index.html">Back</a><br><br>')
        catIndexes.write(mid1)
        brPoint = 1
        for h in vFiles:
            catIndexes.write(vidOpen)
            catIndexes.write('file://localhost/' + fWD + '/' +h)
            catIndexes.write(vidClose)
            if brPoint == 2:
                catIndexes.write('</tr><tr>')
                brPoint = 0
            brPoint +=1
        catIndexes.write(closer)
        catIndexes.close

def Folder_Size_Check():
    mConfig = os.getcwd() + "\Main Config.txt"
    with open(mConfig, 'r') as f:
        mcContent = f.readlines()
    for i in mcContent:
        try:
            if i.index("MaxFolder=") > 0:
                maxFolderL = i[13:]
                maxFolderL = Decimal(maxFolderL) * 1000000000
        except:
            pass
    folderDir = os.getcwd() + '/finished'
    filesCount = os.listdir(folderDir)
    folderVolume = 0
    for i in filesCount:
        fCheck = os.path.join(folderDir, i)
        fStat = os.stat(fCheck)
        fSize = fStat.st_size
        folderVolume += int(fSize)
    remainingSpace = maxFolderL - folderVolume
    if remainingSpace < 10000000:
        return "Stop"
    else:
        return "Go"

Indexing()
runs = 1


print "Welcome to PronBox v2.0.3"
print "PronBox is the next generation of securely viewing porn"
print "and will download the videos in the genre you selected"
print "from the configuration file."
print ""
print ""
print "The programs will now start processing your preferences."
print "Once a site has been processed, a small html file will be"
print "generated. This file will allow you to browse your videos."

fCheck = os.getcwd() + '/bin'
rTube = re.findall('rt Master.txt', str(os.listdir(fCheck)))
yPorn = re.findall('Yp Master.txt', str(os.listdir(fCheck)))
pHub = re.findall('ph Master.txt', str(os.listdir(fCheck)))
cFinished = ""
if len(rTube) != 1:
    runs = 0
if len(yPorn) != 1:
    runs = 0
if len(pHub) != 1:
    runs = 0


if runs == 0:
    print ""
    print ""
    print "No preference files were found. Please run"
    print "configuration.exe first"
    holding = raw_input("Press any key to exit Pronbox. ")
else:
    for i in os.listdir(os.getcwd()):
        if i == "Finished":
            cFinished = "Y"
            
    if cFinished == "Y":
        print "Finished folder found. Starting downloads."
    else:
        print "No finished folder found. Creating folder now."
        os.mkdir(os.getcwd() + "\Finished")
        print "Finished folder created. Starting downloads."
    while runs ==1:
        try:
            print "PornHub"
            try:
                
                #os.system('"' + os.getcwd()+ 'PornHub 41316.py' + '"')
                testPhub = '"' + os.getcwd()+ '/bin\site1.exe' + '"'
                os.system(testPhub)
            except Exception as e:
                print "Res"
                print e
            print "pHub Ended"
            Indexing()
        except:
            pass
        time.sleep(90)
        cTinue = Folder_Size_Check()
        if cTinue == "Stop":
            while cTinue != "Go":
                time.sleep(900)
        try:
            print "RedTube"
            testPhub = '"' + os.getcwd()+ '/bin\site2.exe' + '"'
            os.system(testPhub)
            Indexing()
        except:
            pass
        time.sleep(90)
        cTinue = Folder_Size_Check()
        if cTinue == "Stop":
            while cTinue != "Go":
                time.sleep(900)
        try:
            print "YouPorn"
            testPhub = '"' + os.getcwd()+ '/bin\site3.exe' + '"'
            os.system(testPhub)
            Indexing()
        except:
            pass
        time.sleep(90)
        cTinue = Folder_Size_Check()
        if cTinue == "Stop":
            while cTinue != "Go":
                time.sleep(900)
    

