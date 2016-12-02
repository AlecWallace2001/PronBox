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

def AccessPage(url, maxFileL):
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
    if int(mLength) > maxFileL:
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
    fName = FileCheck(url[sUrl+1:eUrl])
    if fName == "Skip":
        return
    vidName = vidName.replace(' ', '_')
    fName = vidName[:len(vidName)] + ' ' + fName
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
        vUrls =  re.findall('source src="(.*)" type="video',hPage)
        vUrls = vUrls[0]
        return vUrls
    except Exception as e:
        print "Error PageRead"
        return "skip"

#pornhub video url http://www.pornhub.com/view_video.php?viewkey=ph56bcf4c903a63
bvUrl = "http://www.redtube.com"

Master = os.getcwd() + "\Rt Master.txt"
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
    aUrl = "http://www.redtube.com/redtube/"
    try:
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
                            print "Your copy has not been registered."
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
                    if i.index("dlBy=") > 0:
                        #Pornhub main category URL
                        dlBy = i[8:]
                        if dlBy == "Recent":
                            dlBy = ""
                            tgBy = "new?search="
                        else:
                            dlBy = "?sorting=mostfavored"
                            tgBy = "?search="
                except:
                    pass
                try:
                    if i.index("Tag") > 0:
                        xRun = "tag"
                        urlB = i[6:]
                        urlB = urlB.replace(" ","+")
                        pName = urlB[:len(urlB)-1]
                        #http://www.redtube.com/?search=nun
                        #http://www.redtube.com/new?search=nun
                        urlA = "http://www.redtube.com/"
                        urlC = tgBy
                        url = urlA + urlC + urlB
                        html = AccessPage(url, maxFileL)
                        videoA = re.findall('<a href="(.*)" title=',html)
                        videoB = []
                        for i in videoA:
                            if 'redtube' not in i:
                                videoB.append(i)
                        videoC = []
                        for i in videoB:
                            if 'tag' not in i:
                                videoC.append(i)
                        videoB = []
                        for i in videoC:
                            if 's' not in i:
                                videoB.append("http://www.redtube.com" +i)
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
                if i.index('##') <=0:
                    pass
            except:
                try:
                    pCat = i[:len(i)-1]
                    pCat = pCat.strip(" ")
                    pName = pCat
                    bUrl = "c=" + pCat
                #search by most recent
                    aUrl = "http://www.redtube.com/redtube/"
                    cUrl = dlBy
                    url = aUrl + pCat + cUrl
                    html = AccessPage(url, maxFileL)
                    videoA = re.findall('<a href="(.*)" title=',html)
                    videoB = []
                    for i in videoA:
                        if 'redtube' not in i:
                            videoB.append(i)
                    videoC = []
                    for i in videoB:
                        if 'tag' not in i:
                            videoC.append(i)
                    videoB = []
                    for i in videoC:
                        if 's' not in i:
                            videoB.append("http://www.redtube.com" +i)
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
                except Exception as e:
                    pass
        #for i in videoB:
            #vidUrl = PageRead(i)
            #VidDownload(vidUrl, pName)
    except:
        pass

