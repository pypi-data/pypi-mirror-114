#!/usr/bin/env python3
# coding: utf-8

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from joker.cast import want_bytes


def generate_private_key():
    return rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048
    )


def dumps_private_key(rsa_key):
    """
    :type rsa_key: cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey
    :return: a bytes instance
    """
    return rsa_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )


def loads_private_key(binstr, password=None):
    return serialization.load_pem_private_key(
        binstr, password=password, backend=default_backend())


def dumps_public_key(rsa_pubkey):
    """
    :type rsa_pubkey: cryptography.hazmat.backends.openssl.rsa._RSAPublicKey
    :return: a bytes instance
    """
    return rsa_pubkey.public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )


def loads_public_key(binstr):
    return serialization.load_ssh_public_key(binstr, default_backend())


class RSAKeyPair(object):
    """
    Experimental! Take your own risk.
    """
    _crypt_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(), label=None)

    def __init__(self, rsa_key=None):
        if rsa_key is None:
            rsa_key = generate_private_key()
        try:
            self.public_key = rsa_key.public_key()
        except AttributeError:
            self.public_key = rsa_key
            self.private_key = None
        else:
            self.private_key = rsa_key

    @classmethod
    def from_openssh_public_key(cls, content):
        rsa_key = loads_public_key(want_bytes(content))
        return cls(rsa_key)

    @classmethod
    def from_openssh_private_key(cls, content, password):
        rsa_key = loads_private_key(want_bytes(content), password)
        return cls(rsa_key)

    def encrypt(self, message):
        message = want_bytes(message)
        return self.public_key.encrypt(message, self._crypt_padding)

    def decrypt(self, ciphertext):
        if self.private_key is None:
            raise ValueError('cannot decrypt without a private key')
        return self.private_key.decrypt(ciphertext, self._crypt_padding)

    def openssh_private_key(self):
        return dumps_private_key(self.private_key)

    def openssh_public_key(self):
        return dumps_public_key(self.public_key)


__all__ = ['RSAKeyPair']
