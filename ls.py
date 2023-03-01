# coding=utf-8
import base64
import uuid
s = "111"
ss = base64.b64encode(s.encode("utf-8"))
print(ss.decode("utf-8"))

print(base64.b64decode("c2stTFNHa0dVb2hkNVVCZERYaXRXV3hUM0JsYmtGSkZYYjRnZTRxMnAwUllCWTdYamxU").decode("utf-8"))