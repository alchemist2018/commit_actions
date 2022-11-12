from IPy import IP, IPSet
# import zipfile
import requests
import json
from concurrent.futures import ThreadPoolExecutor



# 获得所有待测试ip
def get_all_ips():
    set = IPSet()
    ips =[]
    url = 'https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json'

    with requests.get(url) as r:
        list = json.loads(r.content)

    for i in list['regions']:
        if i['region'] in ['ap-singapore-1','ap-seoul-1','ap-tokyo-1','ap-osaka-1']:
            for j in i['cidrs']:
                if 'OCI' in j['tags']:
                    set.add(IP(j['cidr']))

    for item in set:
        ips += item
    return ips

      

# 测试ip是否可以播放
def check_ip(ip):
    url = 'http://'+str(ip)+':443/cdn-cgi/trace'
    try:
        r = requests.get(url, timeout=0.5)
        content = str(r.headers)
        content = content.replace("'", '"')
        data = json.loads(content)
        if data["Server"] == "cloudflare":
            print(url)
            with open('oracle.txt','a') as fw:
                fw.write(str(ip) + '\n')
        else:
            pass
    except:
        pass

if __name__ == '__main__':
    with ThreadPoolExecutor(200) as executor:
        executor.map(check_ip,get_all_ips())
#     with zipfile.ZipFile('oracle.zip','w') as zip_file:
#         zip_file.write('oracle.txt',compress_type=zipfile.ZIP_DEFLATED)
