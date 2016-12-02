import urllib2
import urllib
import re
import os
import shutil
import ctypes
import sys
import requests
from clint.textui import progress
from decimal import *
import hashlib
sDir = os.getcwd() + '/bin'
finDir = os.getcwd() + '/finished'
os.chdir(sDir)
xRun = ""

def HashRK(fn, ln, email):
    seed1 = ln[:len(ln)-1] + email[:len(email)-1] + fn[:len(fn)-1]
    seed2 = "pR0n8O*"
    inseedlen = len(seed1) -1
    finSeed = ""
    seedRuns = 0
    hSeed = len(seed2)
    while inseedlen >=0:
        try:
            finSeed = finSeed + seed1[inseedlen] + seed2[seedRuns]
            if seedRuns == hSeed -1:
                seedRuns = 0
            else:
                seedRuns +=1
            inseedlen -=1
        except Exception as e:
            pass
    hashed =hashlib.sha512(finSeed)
    return hashed.hexdigest()
        

def FolderCheck(maxFolderL):
    folderDir = finDir
    filesCount = os.listdir(folderDir)
    folderVolume = 0
    for i in filesCount:
        fCheck = os.path.join(folderDir, i)
        fStat = os.stat(fCheck)
        fSize = fStat.st_size
        folderVolume += int(fSize)
    remainingSpace = maxFolderL - folderVolume
    return remainingSpace

def FileCheck(fName):
    finFiles = os.listdir(finDir)
    for i in finFiles:
        if fName in i:
            return "Skip"
    return fName

def get_free_space():
	free_bytes = ctypes.c_ulonglong(0)
	ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(os.path.dirname(os.getcwd())), None, None, ctypes.pointer(free_bytes))
	return free_bytes.value - 60000000
    
def AccessPage(url, maxLength):
    http = urllib2.urlopen(url)
    meta = http.info()
    try:
        mLength = meta.getheaders("Content-Length")[0]
    except:
        mLength = 0
    fLen = len(str(mLength))
    if fLen >6:
        print str(mLength[:fLen-6]) + "mb"
    elif fLen >3:
        print str(mLength[:fLen-3]) + "kb"
    else:
        if str(mLength) != '0':
            print str(mLength) + "b"
    if int(mLength) > maxLength:
        return "Skip"
    fSpace = get_free_space()
    if int(mLength) > fSpace:
        return "Skip" 
    return http.read()

def VidDownload(url, vidName, maxLength, minLength):
    if url[0] == '/':
        url = "http:" + url
    sUrl = url.rfind("/")
    eUrl = url.index("?")
    fName = url[sUrl+1:eUrl]
    fName = fName.replace('%20', ' ')
    fName = fName[:50]
    if fName[len(fName)-4:] != '.mp4':
        fName = fName + '.mp4'
    fName = FileCheck(fName)
    if fName == "Skip":
        print "Exists"
        return
    vidName = vidName.replace(' ', '_')
    fName = vidName + ' ' + str(fName)
    fName = fName.capitalize()
    r = requests.get(url, stream=True)
    mLength = int(r.headers.get('content-length'))
    fLen = len(str(mLength))
    if fLen >6:
        print str(mLength)[:fLen-6] + "mb"
    elif fLen >3:
        print str(mLength)[:fLen-3] + "kb"
    else:
        if str(mLength) != '0':
            print str(mLength) + "b"
    if int(mLength) >= int(maxLength):
        return
    if int(mLength) <= int(minLength):
        return
    with open(fName, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

    
    shutil.copyfile(os.getcwd() + '/' + fName, finDir + '/' + fName) 
    os.remove(os.getcwd() + '/' + fName)

def PageRead(url, maxFileL):
    hPage = AccessPage(url, maxFileL)
    try:
        v240 = re.findall("240: '(.*)',",hPage)
        v480 = re.findall("480: '(.*)',",hPage)
        v720 = re.findall("720: '(.*)',",hPage)
        v72060 = re.findall("720_60: '(.*)',",hPage)
        v1080 = re.findall("1080: '(.*)',",hPage)
        v108060 = re.findall("1080_60: '(.*)',",hPage)
        try:
            if v108060[0] != '':
                return v108060[0]
        except:
            pass
        try:
            if v1080[0] != '':
                return v1080[0]
        except:
            pass
        try:
            if v72060[0] != '':
                return v72060[0]
        except:
            pass
        try:
            if v720[0] != '':
                return v720[0]
        except:
            pass
        try:
            if v480[0] != '':
                return v480[0]
        except:
            pass
        try:
            if v240[0] != '':
                return v240[0]
        except:
            return "skip"
    except:
        print "Error PageRead"
        return "skip"

#pornhub video url http://www.pornhub.com/view_video.php?viewkey=ph56bcf4c903a63
bvUrl = "http://www.youporn.com"

Master = os.getcwd() + "\Yp Master.txt"
with open(Master, 'r') as f:
	content = f.readlines()

reads = 0
rContent = []
for i in content:
    if reads == 0:
        reads = 1
    else:
        rContent.append(i)

for i in rContent:
    aUrl = "http://www.youporn.com/category"
    try:
        #Disregard category if # is found
        try:
            if i.index("##") ==0:
                try:
                    if i.index("FirstName") > 0:
                        #Pornhub gay category URL
                        fName = i[12:]
                except:
                    pass
                try:
                    if i.index("LastName") > 0:
                        #Pornhub gay category URL
                        lName = i[11:]
                except:
                    pass
                try:
                    if i.index("EmailName") > 0:
                        #Pornhub gay category URL
                        eAddress = i[12:]
                except:
                    pass
                try:
                    if i.index("ProductKey") > 0:
                        #Pornhub gay category URL
                        prodKey = i[13:len(i)-1]
                        kCompare = HashRK(fName, lName, eAddress)
                        if kCompare == prodKey:
                            pass
                    else:   
                            print "Your software has not been registered"
                except:
                    pass
                try:
                    if i.index("MaxFile=") > 0:
                        #Pornhub main category URL
                        maxFileL = i[11:] + "000000"
                        maxFileL = re.sub("[^0-9]", "", maxFileL)
                except:
                    pass
                try:
                    if i.index("MinFile=") > 0:
                        #Pornhub main category URL
                        minFileL = i[11:] + "000000"
                        minFileL = re.sub("[^0-9]", "", minFileL)
                except:
                    pass
                try:
                    if i.index("MaxFolder=") > 0:
                        #Pornhub main category URL
                        maxFolderL = i[13:]
                        maxFolderL = Decimal(maxFolderL) * 1000000000                        
                except:
                    pass
                try:
                    if i.index("MaxVids=") > 0:
                        #Pornhub main category URL
                        maxVids = i[11:]
                        maxVids = re.sub("[^0-9]", "", maxVids)
                except:
                    pass
                try:
                    if i.index("Tag") > 0:
                        xRun = "tag"
                        urlB = i[6:]
                        urlB = urlB.replace(" ","+")
                        pName = urlB[:len(urlB)-1]
                        urlA = "http://www.youporn.com/search/?query="
                        urlC = ""
                        url = urlA + urlB + urlC
                        html = AccessPage(url, maxFileL)
                        videoA = re.findall("<a href=(.*) class='video",html)
                        videoB = []
                        for i in videoA:
                            iUrl = bvUrl + i.strip('"')
                            if iUrl in videoB:
                                pass
                            else:
                                videoB.append(iUrl)
                        rDowns = int(maxVids)
                        while rDowns != 0:
                            vidUrl = PageRead(videoB[rDowns], maxFileL)
                            if vidUrl != "skip":
                                rSpace = FolderCheck(maxFolderL)
                                if int(rSpace) > int(maxFileL):
                                    if kCompare == prodKey:
                                        VidDownload(vidUrl, pName, maxFileL, minFileL)
                                elif int(rSpace) > int(minFileL):
                                    if kCompare == prodKey:
                                        VidDownload(vidUrl, pName, rSpace, minFileL)
                                else:
                                    print "No more space"
                            rDowns -=1
                except Exception as e:
                    pass
        except:
            xRun = "Cat"
        if xRun == "Cat":
            try:
                #Disregard category if # is found
                if i.index("##") <=0:
                    pass
            except:
                aName = i[1:]
                pName = re.findall('/(.*)/', aName)
                url = aUrl + i
                html = AccessPage(url, maxFileL)
                videoA = re.findall("<a href=(.*) class='video",html)
                videoB = []
                for i in videoA:
                    iUrl = bvUrl + i[1:len(i)-1]
                    if iUrl in videoB:
                        pass
                    else:
                        videoB.append(iUrl)
                rDowns = int(maxVids)
                
                while rDowns != -1:
                    vidUrl = PageRead(videoB[rDowns], maxFileL)
                    if vidUrl != "skip":
                        rSpace = FolderCheck(maxFolderL)
                        if int(rSpace) > int(maxFileL):
                            if kCompare == prodKey:
                                VidDownload(vidUrl, pName, maxFileL, minFileL)
                        elif int(rSpace) > int(minFileL):
                            if kCompare == prodKey:
                                VidDownload(vidUrl, pName, rSpace, minFileL)
                        else:
                            print "No more space"
                    rDowns -=1
    except:
        pass
        #for i in videoB:
            #vidUrl = PageRead(i)
            #VidDownload(vidUrl, pName)

