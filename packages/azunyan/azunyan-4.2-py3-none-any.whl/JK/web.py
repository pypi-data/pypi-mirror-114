import requests


def rGET(url, params={}, headers={}, cookies={}, timeout=15, retry=3):
    for i in range(retry):
        try:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            print(F'({i+1}/{retry}) Http Error:\n{err}\n{err.response.text}')
        except requests.exceptions.ConnectionError as err:
            print(F'({i+1}/{retry}) Connection Error:\n{err}')
        except requests.exceptions.Timeout as err:
            print(F'({i+1}/{retry}) Timeout Error:\n{err}')
        except requests.exceptions.TooManyRedirects as err:
            print(F'({i+1}/{retry}) Too Many Redirects Error:\n{err}')
        except requests.exceptions.RequestException as err:
            print(F'({i+1}/{retry}) Request Exception:\n{err}')
    print('rGET failed')


def rPOST(url, params={}, data='', headers={}, cookies={}, timeout=15, retry=3):
    for i in range(retry):
        try:
            r = requests.post(url, params=params, data=data, headers=headers, cookies=cookies, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            print(F'({i+1}/{retry}) Http Error:\n{err}\n{err.response.text}')
        except requests.exceptions.ConnectionError as err:
            print(F'({i+1}/{retry}) Connection Error:\n{err}')
        except requests.exceptions.Timeout as err:
            print(F'({i+1}/{retry}) Timeout Error:\n{err}')
        except requests.exceptions.TooManyRedirects as err:
            print(F'({i+1}/{retry}) Too Many Redirects Error:\n{err}')
        except requests.exceptions.RequestException as err:
            print(F'({i+1}/{retry}) Request Exception:\n{err}')
    print('rPOST failed')


def toHeaders(str: str):
    temp = str.strip().split('\n')
    headers = {}
    for line in temp:
        key, value = line.split(':', 1)
        headers[key.strip()] = value.strip()
    return headers


def toCookies(str: str):
    temp = str.strip().split(';')
    cookies = {}
    for line in temp:
        key, value = line.split('=', 1)
        cookies[key.strip()] = value.strip()
    return cookies
