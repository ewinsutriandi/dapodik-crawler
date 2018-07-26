from bs4 import BeautifulSoup
import urllib2
import requests
import re
import psycopg2

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ConfigParser import SafeConfigParser

def prepareParams():
    parser = SafeConfigParser()
    parser.read('config.ini')

    global glIP,glDBuser,glDBpass, glDB

    #database configurations
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDB = parser.get('db', 'db')

    global apiHost
    apiHost = parser.get('api', 'host')

    global conn

    cs = "dbname=%s user=%s password=%s host=%s" % (glDB,glDBuser,glDBpass,glIP)
    # use our connection values to establish a connection
    conn = psycopg2.connect(cs)

    #print conn.status


def grabSchoolData(school_id):
    url = apiHost+'sekolah/'+school_id
    #print url
    sess_req = requests.session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    sess_req.mount('http://', HTTPAdapter(max_retries=retries))
    rslt = sess_req.get(url)
    #print rslt.status_code
    if rslt.status_code == requests.codes.ok :
        soup = BeautifulSoup(rslt.content,'lxml')
        divNama = soup.find("div", {"class": "info"})
        divProfil = soup.find("div", {"id": "profil"})
        divKontak = soup.find("div", {"id": "kontak"})

        textProfil = divProfil.getText()
        textKontak = divKontak.getText()

        nama = soup.find("h2").getText()
        npsn = (re.search('NPSN :  (.*) ', textProfil)).group(1)
        status = (re.search('Status : (.*)', textProfil)).group(1)
        bentuk = (re.search('Bentuk Pendidikan : (.*)', textProfil)).group(1)
        waktuPenyelenggaraan = (re.search('Penyelenggaraan : (.*)', textProfil)).group(1)
        kepemilikan = (re.search('Status Kepemilikan : (.*)', textProfil)).group(1)
        luasTanahMilik = int((re.search('Luas Tanah Milik : (.*)', textProfil)).group(1) or 0)
        luasTanahBukanMilik = int((re.search('Luas Tanah Bukan Milik : (.*)', textProfil)).group(1) or 0)
        dayaListrik = int((re.search('Daya Listrik : (.*)', textProfil)).group(1) or 0)
        aksesInternet = (re.search('Akses Internet : (.*)', textProfil)).group(1)

        alamat = (re.search('Alamat : (.*)', textKontak)).group(1)
        deskel = (re.search('Kelurahan : (.*)', textKontak)).group(1)
        kec = (re.search('Kecamatan : (.*)', textKontak)).group(1)
        kodepos = (re.search('Kode Pos : (.*)', textKontak)).group(1)
        lintang = float((re.search('Lintang : (.*)', textKontak)).group(1) or 0)
        bujur = float((re.search('Bujur : (.*)', textKontak)).group(1) or 0)
        email = (re.search('Email : (.*)', textKontak)).group(1)
        telp = (re.search('Telepon : (.*)', textKontak)).group(1)

        cursor = conn.cursor()
        sql = """insert into dapodik.sekolah(nama,
                npsn,status,bentuk,waktu_penyelenggaraan,kepemilikan,
                luas_tanah_milik,luas_tanah_bukan_milik,daya_listrik,akses_internet,
                alamat,deskel,kecamatan,kodepos,latitude,longitude,email,telp)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        cursor.execute(sql,(nama,npsn,status,bentuk,waktuPenyelenggaraan,kepemilikan,
            luasTanahMilik,luasTanahBukanMilik,dayaListrik,aksesInternet,
            alamat,deskel,kec,kodepos,lintang,bujur,email,telp))
        cursor.close()    


    else:
        print "failed request"

def grabEmAll():
    prepareParams()
    fp = open('school_ids.txt')
    schools = fp.readlines()
    cnt = 0
    for id in schools:
        cnt += 1
        print cnt
        grabSchoolData(id.strip())
    conn.commit()
    conn.close()
grabEmAll()

