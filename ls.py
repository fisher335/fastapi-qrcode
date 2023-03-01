# coding=utf-8
import base64
import uuid
s = "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"
ss = base64.b64encode(s.encode("utf-8"))
print(ss.decode("utf-8"))

print(base64.b64decode("c2stRFZyZE5QdEFJMGhnUzFXbFFBVDBUM0JsYmtGSjNkWjM3TXRDZGZ6bGFxYk5wOERn").decode("utf-8"))