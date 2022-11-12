from IPy import IP, IPSet
# import zipfile
import requests
import json
from concurrent.futures import ThreadPoolExecutor



# 获得所有待测试ip
def get_all_ips():
    set = IPSet()
    ips =[]
    url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

# 数据中心参考 https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html

    with requests.get(url) as r:
        list = json.loads(r.content)

    for i in list['prefixes']:
        if i['region'] in ['ap-east-1'] and i['service'] in ['EC2']:
            set.add(IP(i['ip_prefix']))
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
            with open('aws.txt','a') as fw:
                fw.write(str(ip) + '\n')
        else:
            pass
    except:
        pass

if __name__ == '__main__':
    with ThreadPoolExecutor(500) as executor:
        executor.map(check_ip,get_all_ips())
#     with zipfile.ZipFile('aws.zip','w') as zip_file:
#         zip_file.write('aws.txt',compress_type=zipfile.ZIP_DEFLATED)
