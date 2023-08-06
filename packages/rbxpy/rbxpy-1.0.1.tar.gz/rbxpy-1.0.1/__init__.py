from time import sleep
import requests
import json
import time

"""
hello source creeps!
this was made by strikerz!
(Ryan Awesome222 on v3rmillion lol)
(plz dont steal ig idk lol)

as you can see there is no cookie stealers in here!
"""

def get_description(uid):
    req = requests.get(f"https://users.roblox.com/v1/users/{str(uid)}")
    return req.json()['description']

def get_uid_by_name(name):
    req = requests.get(f"https://api.roblox.com/users/get-by-username?username={name}")
    return req.json()['Id']

def get_name_by_uid(uid):
    req = requests.get(f"https://users.roblox.com/v1/users/{str(uid)}")
    return req.json()['name']

def set_about_pin(cookie, text, pin):
    body_unlockpin = {"pin": str(pin)}
    headers_unlockpin = {"x-csrf-token": get_x_csrf(cookie, "https://auth.roblox.com/v1/account/pin")}
    requests.post("https://auth.roblox.com/v1/account/pin/unlock", json=body_unlockpin, headers=headers_unlockpin, cookies={".ROBLOSECURITY": cookie})
    sleep(1)
    body = {}
    headers = {}
    body['description'] = text
    headers['x-csrf-token'] = get_x_csrf(cookie, "https://accountinformation.roblox.com/v1/description")
    req = requests.post("https://accountinformation.roblox.com/v1/description", json=body, headers=headers, cookies={".ROBLOSECURITY": cookie})
    return req.status_code

def set_light(cookie):
    r = requests.patch("https://accountsettings.roblox.com/v1/themes/user", headers={"x-csrf-token":get_x_csrf(cookie, "https://accountsettings.roblox.com/")}, json={"themeType":"Light"}, cookies={".ROBLOSECURITY":cookie})
    return r.status_code

def set_dark(cookie):
    r = requests.patch("https://accountsettings.roblox.com/v1/themes/user", headers={"x-csrf-token":get_x_csrf(cookie, "https://accountsettings.roblox.com/")}, json={"themeType":"Dark"}, cookies={".ROBLOSECURITY":cookie})
    return r.status_code

def get_theme(cookie):
    themetype = ""
    t = requests.get("https://accountsettings.roblox.com/v1/themes/user", headers={"x-csrf-token":get_x_csrf(cookie, "https://accountsettings.roblox.com/")}, cookies={".ROBLOSECURITY":cookie}).text
    if t == '{"themeType":"Light"}':
        themetype = "Light"
    elif t == '{"themeType":"Dark"}':
        themetype = "Dark"
    return themetype

def toggle_theme(cookie):
    t = requests.get("https://accountsettings.roblox.com/v1/themes/user", headers={"x-csrf-token":get_x_csrf(cookie, "https://accountsettings.roblox.com/")}, cookies={".ROBLOSECURITY":cookie}).text
    if get_theme(cookie) == "Light":
        set_dark(cookie)
    else:
        set_light(cookie)

def set_about(cookie, text):
    body = {}
    headers = {}
    body['description'] = text
    headers['x-csrf-token'] = get_x_csrf(cookie, "https://accountinformation.roblox.com/v1/description")
    req = requests.post("https://accountinformation.roblox.com/v1/description", json=body, headers=headers, cookies={".ROBLOSECURITY": cookie})
    return req.status_code

def set_displayname(cookie, name):
    r = requests.post(f'https://users.roblox.com/v1/users/{get_current_authenticated_user_id}/display-names', json={"newDisplayName": name}, headers={"x-csrf-token": get_x_csrf(cookie, "https://users.roblox.com/v1/users/2763130106")}, cookies={".ROBLOSECURITY": cookie})
    return r.text

def get_previoususernames(uid, limit): # god that took a while lol
    r = requests.get(f"https://users.roblox.com/v1/users/{str(uid)}/username-history?limit={str(limit)}&sortOrder=Asc").text # does not require X-CSRF-TOKEN
    x = []
    for s in str.split(r, '{"name":"'):
        lol = '{"previousPageCursor":null,"nextPageCursor":null,"data":['
        if lol in s:
            s = s.replace(lol, "")
            x.append(s.split('"}', 1)[0])
    return x

def get_current_authenticated_user_id(cookie):
    data = requests.get("https://users.roblox.com/v1/users/authenticated", headers={"x-csrf-token": get_x_csrf(cookie, "https://users.roblox.com/v1/users/authenticated")}, cookies={".ROBLOSECURITY": cookie}).json()
    return data['id']

def get_current_authenticated_username(cookie):
    data = requests.get("https://users.roblox.com/v1/users/authenticated", headers={"x-csrf-token": get_x_csrf(cookie, "https://users.roblox.com/v1/users/authenticated")}, cookies={".ROBLOSECURITY": cookie}).json()
    return data['name']

def get_current_authenticated_displayname(cookie):
    data = requests.get("https://users.roblox.com/v1/users/authenticated", headers={"x-csrf-token": get_x_csrf(cookie, "https://users.roblox.com/v1/users/authenticated")}, cookies={".ROBLOSECURITY": cookie}).json()
    return data['displayName']

def buy_asset(cookie, asset, price, sellerid):
    r = requests.post(f"https://economy.roblox.com/v1/purchases/products/{asset}", cookies={".ROBLOSECURITY":cookie}, headers={"x-csrf-token": get_x_csrf(cookie, "https://economy.roblox.com/")}, json={"expectedCurrency":"1","expectedPrice":int(price),"expectedSellerId":int(sellerid)})
    return r.status_code

def remove_pin(cookie, pin):
    body_unlockpin = {"pin": str(pin)}
    headers_unlockpin = {"x-csrf-token": get_x_csrf(cookie, "https://auth.roblox.com/v1/account/pin")}
    requests.post("https://auth.roblox.com/v1/account/pin/unlock", json=body_unlockpin, headers=headers_unlockpin, cookies={".ROBLOSECURITY": cookie})
    sleep(1)
    headers = {"x-csrf-token": get_x_csrf(cookie, "https://auth.roblox.com/v1/account/pin")}
    ree = requests.delete("https://auth.roblox.com/v1/account/pin", headers=headers, cookies={".ROBLOSECURITY": cookie})
    return ree.status_code

def get_asset_download_url(id):
    return f'https://assetdelivery.roblox.com/v1/asset/?id={str(id)}'

def has_pin(cookie):
    r = requests.get("https://auth.roblox.com/v1/account/pin", headers={"x-csrf-token": get_x_csrf(cookie, "https://auth.roblox.com/v1/account/pin")}, cookies={".ROBLOSECURITY":cookie})
    if '"isEnabled":true' in r.text:
        return "pin is enabled"
    else:
        return "pin is not enabled"

def get_x_csrf(cookie, url):
    req = requests.post(url, cookies={".ROBLOSECURITY": cookie})
    return req.headers["x-csrf-token"]