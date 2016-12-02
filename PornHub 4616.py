import urllib2
import urllib
import re
import os
import shutil
import ctypes
import sys
import requests
from decimal import *
from clint.textui import progress
import hashlib
print 1
sDir = '"' + os.getcwd() + '/bin"'
finDir = os.getcwd() + '/finished'
os.chdir(sDir)
xRun = ""
print 2
def HashRK(fn, ln, email):
    print "HashRK"
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
    print "FolderCheck"
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
    print "FileCheck"
    finFiles = os.listdir(finDir)
    for i in finFiles:
        if fName in i:
            return "Skip"
    return fName

def get_free_space():
    print "Get Free Space"
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(os.path.dirname(os.getcwd())), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value - 60000000

def AccessPage(url,maxLength):
    print "Access Page"
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
    print "Vid Download"
    if url[0] == '/':
        url = "http:" + url
    #print url
    sUrl = url.rfind("/")
    eUrl = url.index("?")
    fName = FileCheck(url[sUrl+1:eUrl])
    if fName == "Skip":
        return
    vidName = vidName.replace(' ', '_')
    fName = vidName[:len(vidName)-1] + ' ' + fName
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
    print "Page Read"
    hPage = AccessPage(url, maxFileL)
    try:
        vUrls = re.findall("var player(.*)';",hPage)
        vUrls = vUrls[0]
        if len(re.findall("quality_1080p",vUrls))!=0:
            sUrl = vUrls.index("1080p = '")
            tezUrls = vUrls[sUrl+8:]
            try:
                eUrl = tezUrls.index(";")
            except:
                eUrl = len(tezUrls)
            tezUrls = tezUrls[:eUrl]
            tezUrls = tezUrls.strip("'")
            return tezUrls
        if len(re.findall("quality_720p",vUrls))!=0:
            sUrl = vUrls.index("720p = '")
            stzUrls = vUrls[sUrl+8:]
            try:
                eUrl = stzUrls.index(";")
            except:
                eUrl = len(stzUrls)
            stzUrls = stzUrls[:eUrl]
            stzUrls = stzUrls.strip("'")
            return stzUrls
        if len(re.findall("quality_480p",vUrls))!=0:
            sUrl = vUrls.index("480p = '")
            fezUrls = vUrls[sUrl+8:]
            try:
                eUrl = fezUrls.index(";")
            except:
                eUrl = len(fezUrls)
            fezUrls = fezUrls[:eUrl]
            fezUrls = fezUrls.strip("'")
            return fezUrls
        if len(re.findall("quality_240p",vUrls))!=0:
            sUrl = vUrls.index("240p = '")
            tfzUrls = vUrls[sUrl+8:]
            try:
                eUrl = tfzUrls.index(";")
            except:
                eUrl = len(tfzUrls)
            tfzUrls = tfzUrls[:eUrl]
            tfzUrls = tfzUrls.strip("'")
            return tfzUrls
    except:
        print "Error PageRead"
        return "skip"

#pornhub video url http://www.pornhub.com/view_video.php?viewkey=ph56bcf4c903a63
bvUrl = "http://www.pornhub.com/view_video.php?viewkey="

print "Start"
try:
    Master = sDir + "\ph Master.txt"
    with open(Master, 'r') as f:
            content = f.readlines()
    reads = 0
except Exception as e:
    pass

print "Start 2"
for i in content:
    if reads == 0:
        reads = 1
    else:
        try:
            if i.index("##") <=0:
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
                            print "Your copy has not been registered"
                except:
                    pass
                try:
                    if i.index("gay") > 0:
                        #Pornhub gay category URL
                        xRun="Cat"
                        aUrl = "http://www.pornhub.com/gay/video?"
                except:
                    pass
                try:
                    if i.index("straight") > 0:
                        #Pornhub main category URL
                        xRun="Cat"
                        aUrl = "http://www.pornhub.com/video?"
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
                            dlBy = "&o=cm"
                            tgBy = "&o=mr"
                        else:
                            dlBy = ""
                            tgBy = ""
                except:
                    pass
                try:
                    if i.index("Tag") > 0:
                        xRun = "tag"
                        urlB = i[6:]
                        urlB = urlB.replace(" ","+")
                        pName = urlB
                        urlA = "http://www.pornhub.com/video/search?search="
                        urlC = tgBy
                        url = urlA + urlB + urlC
                        html = AccessPage(url, maxFileL)
                        videoA = re.findall('viewkey=(.*)" title="',html)
                        videoB = []
                        for i in videoA:
                            iUrl = bvUrl + i
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
                except:
                    pass
        except:
            pass
        if xRun == "Cat":
            try:
                #Disregard category if # is found
                if i.index("##") <=0:
                    pass
                

            except Exception as e:
                pCat = i[:4]
                pCat = pCat.strip(" ")
                pName = i[4:]
                pName = pName.strip(" ")
                bUrl = "c=" + pCat
            #search by most recent
                cUrl = dlBy
                url = aUrl + bUrl + cUrl
                html = AccessPage(url, maxFileL)
                videoA = re.findall('viewkey=(.*)" title="',html)
                videoB = []
                for i in videoA:
                    iUrl = bvUrl + i
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
        #for i in videoB:
            #vidUrl = PageRead(i)
            #VidDownload(vidUrl, pName)


