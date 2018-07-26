'''
Created on 24 Jul 2018

@author: ewin.sutriandi@gmail.com
'''

from ConfigParser import SafeConfigParser
import logging
import requests
import json
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def prepareParams():
    parser = SafeConfigParser()
    parser.read('config.ini')

    global glIP,glDBuser,glDBpass, glDBschema,glLogFile
    global apiHost, rekapURL, rekapSekolah, rekapLevelParam, rekapWilParam, rekapProgresSP, detailSekolah
    global provCode, kabCode
    global school_ids
    
    #database configurations
    glIP = parser.get('db', 'ip')
    glDBuser = parser.get('db', 'user')
    glDBpass = parser.get('db', 'password')
    glDBschema = parser.get('db', 'schema')
    
    #api configuration
    apiHost = parser.get('api', 'host')
    rekapURL = parser.get('api', 'rekap')
    rekapSekolah = parser.get('api', 'rekap_sekolah')
    rekapLevelParam = parser.get('api', 'rekap_level_param')
    rekapWilParam = parser.get('api', 'rekap_wil_param')
    sekolahIdParam = parser.get('api', 'sekolah_id_param')
    rekapProgresSP = parser.get('api', 'rekap_progres_SP')
    detailSekolah = parser.get('api', 'detail_sekolah')
    
    #local administrative id
    provCode = parser.get('region','prov')
    kabCode = parser.get('region','kab')

    #prepare log file
    glLogFile = "crawler-log.txt"
    logging.basicConfig(filename=glLogFile,level=logging.INFO,format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    #prepare list
    school_ids = []
def crawlRekapKabupaten():
    logging.info("ambil data rekap sekolah di kabupaten")
    url = apiHost + rekapURL + rekapSekolah + rekapLevelParam + "=2&" + rekapWilParam +"="+kabCode 
    print url
    sess_req = requests.session()
    rslt = sess_req.get(url)
    print rslt.status_code
    if rslt.status_code == requests.codes.ok :
       logging.info("pengambilan sukses") 
       rekap_kab = rslt.json() 
       for obj in rekap_kab:
           kecCode = obj['kode_wilayah']
           print kecCode
           crawlRekapKecamatan(kecCode)
           #for attribute, value in obj.iteritems():
               #print attribute, value
            
    else :
        print "failed crawling rekap kab"
    
    print len(school_ids)
    f = open('school_ids.txt', 'w')
    for schid in school_ids:
      f.write("%s\n" % schid)

def crawlRekapKecamatan(kecCode):
    logging.info("ambil data rekap sekolah per kecamatan")
    url = apiHost + rekapURL + rekapProgresSP + rekapLevelParam + "=3&" + rekapWilParam +"="+kecCode 
    print url
    sess_req = requests.session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
    sess_req.mount('http://', HTTPAdapter(max_retries=retries))
    rslt = sess_req.get(url)
    #print rslt.status_code
    if rslt.status_code == requests.codes.ok :
       logging.info("pengambilan sukses") 
       rekap_kec = rslt.json() 
       for obj in rekap_kec:
           school_id = obj['sekolah_id_enkrip']
           school_ids.append(school_id)
           #crawlSchoolDetail(school_id)

    else :
        print "failed crawling rekap kec"

def crawlSchoolDetail(school_id):
    logging.info("ambil detail sekolah")
    url = apiHost + detailSekolah + school_id 
    print url
    
def main():
    prepareParams()
    crawlRekapKabupaten()

main()