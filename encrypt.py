from base64 import b64encode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
def Encrypt(uid , seed):
    plain_text = uid

    # generate a random salt

    salt = get_random_bytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password

    private_key = hashlib.scrypt(
        seed.encode(),
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
        dklen=32,
        )

    # create cipher config

    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text

    (cipher_text, tag) = \
        cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    encryptedDict = {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        }
    encryptedString = encryptedDict['cipher_text'] + '*' \
        + encryptedDict['salt'] + '*' + encryptedDict['nonce'] + '*' \
        + encryptedDict['tag']
    return encryptedString

