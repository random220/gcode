import base64
d = 'XXXXXXXXXXXXXXXXX'
encoded_bytes = base64.b64encode(bytes(d, 'utf-8'))
encoded_str = str(encoded_bytes, encoding='utf-8')
print(encoded_str)

decoded_bytes = base64.b64decode(encoded_str)
decoded_str = str(decoded_bytes, encoding='utf-8')
print(decoded_str)

