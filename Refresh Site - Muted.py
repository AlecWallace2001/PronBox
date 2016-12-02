# 4/13/2016 8:33am - Added call to Indexing. This resolved the update issue.

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

    vidOpen = '''<th><video muted width="600" controls>
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

Indexing()
