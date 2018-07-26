from bs4 import BeautifulSoup
import urllib2
import requests
import re

def getSchoolData():
    url = 'http://dapo.dikdasmen.kemdikbud.go.id/sekolah/7C62A6203981834A98EB'
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content,'lxml')
        divProfil = soup.find("div", {"id": "profil"})
        divKontak = soup.find("div", {"id": "kontak"})
        textProfil = divProfil.getText()
        textKontak = divKontak.getText()

        npsn = (re.search('NPSN :  (.*) ', textProfil)).group(1)
        status = (re.search('Status : (.*)', textProfil)).group(1)
        bentuk = (re.search('Bentuk Pendidikan : (.*)', textProfil)).group(1)
        waktuPenyelenggaraan = (re.search('Penyelenggaraan : (.*)', textProfil)).group(1)
        kepemilikan = (re.search('Status Kepemilikan : (.*)', textProfil)).group(1)
        luasTanahMilik = (re.search('Luas Tanah Milik : (.*)', textProfil)).group(1)
        luasTanahBukanMilik = (re.search('Luas Tanah Bukan Milik : (.*)', textProfil)).group(1)
        dayaListrik = (re.search('Daya Listrik : (.*)', textProfil)).group(1)
        aksesInternet = (re.search('Akses Internet : (.*)', textProfil)).group(1)

        alamat = (re.search('Alamat : (.*)', textKontak)).group(1)
        deskel = (re.search('Kelurahan : (.*)', textKontak)).group(1)
        kec = (re.search('Kecamatan : (.*)', textKontak)).group(1)
        kodepos = (re.search('Kode Pos : (.*)', textKontak)).group(1)
        lintang = (re.search('Lintang : (.*)', textKontak)).group(1)
        bujur = (re.search('Bujur : (.*)', textKontak)).group(1)
        email = (re.search('Email : (.*)', textKontak)).group(1)
        telp = (re.search('Telepon : (.*)', textKontak)).group(1)

        #print npsn.group(1)
        #print(divProfil.prettify())
        print(npsn)
        print(status)
        print(bentuk)
        print(waktuPenyelenggaraan)
        print(kepemilikan)
        print(luasTanahMilik)
        print(luasTanahBukanMilik)
        print(dayaListrik)
        print(aksesInternet)

        print(alamat)
        print(deskel)
        print(kec)
        print(kodepos)
        print(telp)
        print(email)
        print(lintang)
        print(bujur)

    else:
        print "failed request"
    
getSchoolData()