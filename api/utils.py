from typing import List
import requests
from hashlib import sha256
import collections
from fake_useragent import UserAgent
from urllib import request, parse
import json
PASSWORD = "5dxwvngrpghd2oqg"
TERMINAL_KEY="1627394913817DEMO"


def create_hash_token(data: "List"):
    text_data = ""
    global PASSWORD
    data_request = data.copy()
    if "Shops" in data_request:
        data_request.pop("Shops", None)
    if "Receipt" in data_request:
        data_request.pop("Receipt", None)
    if "DATA" in data_request:
        data_request.pop("DATA", None)
    data_request["Password"]= PASSWORD
    data_request = dict(sorted(data_request.items()))
    print("-"*50)
    print(data_request)
    print("-"*50)
    for key, value in data_request.items():
        text_data += str(value)
    print(text_data)
    result = sha256(text_data.encode('utf-8')).hexdigest()
    return result

#"Description": "Test",
data_req = {
    "TerminalKey": TERMINAL_KEY,
    "Amount": "100",
    "OrderId": "210502319",
    "Receipt": {
        "Email": "v_babaev@webjox.ru",
        "Phone": "+79085117630",
        "EmailCompany": "vadim_gkm@mail.ru",
        "Taxation": "osn",
        "Items": [
            {
                "Name": "Наименование товара 1",
                "Price": "100",
                "Quantity": "2.00",
                "Amount": "100",
                "PaymentMethod": "full_prepayment",
                "PaymentObject": "commodity",
                "Tax": "none",
                "Ean13": "0123456789"
            }
        ]
    }
}   
def get_url_payment():
    
    json_object = json.dumps(data_req)
    req = requests.post(url="https://securepay.tinkoff.ru/v2/Init", data=json_object, headers={"content-type": "application/json"})
    print(req.json())
    return req.json() 

data = get_url_payment()
ua = UserAgent()
hash_token = create_hash_token(data_req)
print(hash_token)
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json" ,
    'User-Agent': "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
    })
data_req={
 "TerminalKey" :TERMINAL_KEY,
  "PaymentId": data["PaymentId"],
 "Token" : hash_token.lower()
}
print("*"*50)
print(data_req)
json_object = json.dumps(data_req)

r = session.post(url="https://securepay.tinkoff.ru/v2/GetState/", data=json_object)
print(r.status_code)
print(r.text)

