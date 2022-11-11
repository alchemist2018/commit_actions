from IPy import IP, IPSet

import requests
import json
from concurrent.futures import ThreadPoolExecutor



# 获得所有待测试ip
# oracle  https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json

# def get_all_ips(hosts_list_path):
#     set = IPSet([IP('1.1.1.1/32')])
#     ips = []
#     with open(hosts_list_path, "r") as f:
#         for host in f.readlines():
#             set.add(IP(host))
#     for item in set:
#         ips += item 
#     return ips

      

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
            with open('output/output.txt','a') as fw:
                fw.write(str(url) + '\n')
        else:
            print(ip)
    except:
        print(ip)

if __name__ == '__main__':
    with ThreadPoolExecutor(5) as executor:
            executor.map(check_ip,IP('140.238.3.0/24'))
