from bs4 import BeautifulSoup
import urllib2
import requests
import re
import psycopg2

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ConfigParser import SafeConfigParser


url = 'http://dapo.dikdasmen.kemdikbud.go.id/sekolah/7C62A6203981834A98EB'
#url2 = 'http://dapo.dikdasmen.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah=230309'
#print url
#print url2


sess_req = requests.session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
sess_req.mount('http://', HTTPAdapter(max_retries=retries))
rslt = sess_req.get(url)
#print rslt.status_code
if rslt.status_code == requests.codes.ok :
    soup = BeautifulSoup(rslt.content,'lxml')
    textNama = soup.find("h2").getText()
    #nama = (re.search(' (.*)Sinkronisasi', textNama)).group(1)
    print textNama