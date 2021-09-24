import base64


def decode_base64(data):
    return base64.b64decode(data)


def generate_decoded_file(data, filename):
    formal_data = data.partition(",")[2]
    with open(filename, 'wb') as nf:
        nf.write(decode_base64(formal_data))
    return True