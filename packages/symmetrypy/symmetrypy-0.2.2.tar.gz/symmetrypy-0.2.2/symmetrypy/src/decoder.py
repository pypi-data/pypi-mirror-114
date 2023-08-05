

raw = ['AZPF4DobgCux02I3TraehsJmTsuBwx/GZTtJ5KRM3Oer9zrfa1EM5GUAKS8RUDkHovsUjIKwGEDX/3O0nNnTaK917sog1f0RAtj7O4OGRmSfUbsWsXwNlx7c1twGsDa9zQDKmjsAAAAABGQAAAAAAAAAAAAvFxIMAAAAAAAAs1ptZQAAAAAD5wsBAAAAAOy1YAAAAAAAuVs/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
        'base64']
data = raw[0]

import base64
import base58
from pprint import pprint

# a = base64.b64decode(data)[0]
# print(a)



def decode(data, schema):
    """ pass base64 data and schema, returns a dict of data.
        schema = [[<type>, <num_bytes>], ... ] 
        types can be one of: str, bool, int, 'pubkey' """
    # decode data
    decoded = []
    data = base64.b64decode(data)

    i = 0
    for s in schema:
        element_length = s[1]
        element_type = s[0]
        element_bytes = data[i:i+element_length]

        if element_type == bool:
            if len(element_bytes) != 1:
                raise Exception("element at byte {} is bool but length was not 1".format(i))    
            if int(element_bytes[0]) == 1:
                decoded.append(True)
            else:
                decoded.append(False)
        elif element_type == int:
            decoded.append(int.from_bytes(element_bytes, byteorder='little'))
        elif element_type == str:
            decoded.append( element_bytes.decode('utf-8') )
        elif element_type == 'pubkey':
            pubkey = base58.b58encode(element_bytes).decode('ascii')
            decoded.append(pubkey)

        i += element_length
    return decoded



if __name__ == "__main__":
    schema = [
        [bool, 1],
        ['pubkey', 32],
        ['pubkey', 32],
        ['pubkey', 32],
        [int, 8],
        [int, 1],
        [int, 2],
        [int, 8]
    ]
    schema.extend([[int, 1] for _ in range(10)])
    schema.extend([[int, 8] for _ in range(10)])

    decoded = decode(data, schema)
    pprint(decoded)

