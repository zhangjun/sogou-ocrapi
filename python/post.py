#!/usr/bin/env python

import urllib
import urllib2

import base64
import hashlib

import requests


service_url = "http://deepi.sogou.com/api/sogouService"


def Post(url, params):
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    req = urllib2.Request(url, urllib.urlencode(params), headers)
    response = urllib2.urlopen(req)
    return response.read()

def Post2(url, params):
    r = urllib.urlopen(url, urllib.urlencode(params))
    return r.read()
    
def Post3(url, params):
    r = requests.post(url, params)
    return r.text

def File2base64(file):
    f = open(file, 'rb')
    return base64.b64encode(f.read())

def CalSign(pid, service, salt, sign_image, key):
    m = hashlib.md5()
    data = pid + service + salt + sign_image + key
    print data
    m.update(data)
    return m.hexdigest()


if __name__ == '__main__': 

    img_file = 'ace.PNG'
    pid = 'your pid'
    key = 'your key'
    service = 'basicOpenOcr'
    lang = 'zh-CHS'
    salt = '201810'
    img_base64 = File2base64(img_file)
    sign = CalSign(pid, service, salt, img_base64[0:1024], key)
    print img_base64[0:1024]
    print sign

    param_data = {
        "pid":pid,
        "service":service,
        "lang":lang,
        "salt":salt,
        "image":img_base64,
        "sign":sign
        }
    
    #print param_data

    res = Post(service_url, param_data)
    print res
