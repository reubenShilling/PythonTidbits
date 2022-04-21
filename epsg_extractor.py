import requests
import re
from bs4 import BeautifulSoup

epsg_codes = []
for i in range(1, 88):
    url = r'https://www.spatialreference.org/ref/epsg/?page=' + str(i)
    url_res = requests.get(url, verify=False)
    if url_res.status_code != 200:
        continue
    url_str = url_res.text
    soup = BeautifulSoup(url_str, 'html.parser')
    codes = soup.select("table td li a")
    for code in codes:
        txt = code.text.replace('EPSG:', '')
        num = long(txt)
        epsg_codes.append(num)

epsg_codes.sort()

for srid in epsg_codes:
    print '\nExtracting SRID: ' + str(srid) + '...'
    ogc = 'https://www.spatialreference.org/ref/epsg/' + str(srid) + '/ogcwkt/'
    ogc_res = requests.get(ogc, verify=False)
    if ogc_res.status_code != 200:
        continue
    esri = 'https://www.spatialreference.org/ref/epsg/' + str(srid) + '/esriwkt/'
    esri_res = requests.get(ogc, verify=False)
    if esri_res.status_code != 200:
        continue
    ogc_wkt = ogc_res.content
    esri_wkt = esri_res.content
    st = ogc_wkt.find('["') + 2
    end = ogc_wkt.find('",')
    fullName = ogc_wkt[st:end]
    filename = re.sub(r'\W', '_', fullName)
    filename = re.sub(r'__+', '_', filename)
    filename = re.sub('_$', '', filename)
    if filename == '':
        continue
    fullpath = 'F:\\RiderProjects\\EpsgCoordinateSystems\\EpsgCoordinateSystems\\' + filename + '.cs'
    ogc_wkt = ogc_wkt.replace('"', '')
    esri_wkt = esri_wkt.replace('"', '')
    with open(fullpath, 'w') as f:
        f.write('namespace EpsgCoordinateSystems')
        f.write('{')
        f.write('public class ' + filename + ' : IEpsgCoordinateSystem')
        f.write('{')
        f.write('public string Name => "' + fullName + '";')
        f.write('public long Srid => ' + str(srid) + ';')
        f.write('public string OgcWkt => "' + ogc_wkt + '";')
        f.write('public string EsriWkt => "' + esri_wkt + '";')
        f.write('}')
        f.write('}')
        f.close()
    print '...SRID:' + str(srid) + 'extracted!'
