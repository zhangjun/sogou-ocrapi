#!/usr/bin/env python3

import urllib
import urllib.request
import urllib.parse

import requests 

import base64
import hashlib



service_url = "http://deepi.sogou.com/api/sogouService"


def Post(url, params):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, urllib.parse.urlencode(params).encode(encoding='utf-8'), headers)
    response = urllib.request.urlopen(req)
    return response.read()

def Post2(url, params):
    r = urllib.request.urlopen(url, urllib.parse.urlencode(params).encode(encoding='utf-8'))
    return r.read()
    
def Post3(url, params):
    r = requests.post(url, params)
    return r.text

def File2base64(file):
    f = open(file, 'rb')
    return base64.b64encode(f.read()).decode()

def CalSign(pid, service, salt, sign_image, key):
    m = hashlib.md5()
    data = "%s%s%s%s%s" % (pid, service, salt, sign_image, key)
    print(data)
    m.update(data.encode(encoding='utf-8'))
    return m.hexdigest()


if __name__ == '__main__': 

    img_file = 'ace.PNG'
    pid = 'your pid'
    key = 'your key'
    service = 'basicOpenOcr'
    lang = 'zh-CHS'
    salt = '201810'
    img_base64 = File2base64(img_file)
    print(img_base64[0:1024])
    sign = CalSign(pid, service, salt, img_base64[0:1024], key)
    print(sign)

    param_data = {
        "pid":pid,
        "service":service,
        "lang":lang,
        "salt":salt,
        "image":img_base64,
        "sign":sign
        }
    
    #print param_data

    res = Post2(service_url, param_data)
    #print(res)
    print(res.decode('utf-8'))
