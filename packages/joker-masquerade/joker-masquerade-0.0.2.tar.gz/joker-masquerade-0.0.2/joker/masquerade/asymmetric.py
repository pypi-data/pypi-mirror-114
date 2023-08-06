#!/usr/bin/env python3
# coding: utf-8

import base64

import rsa
from rsa import PublicKey, PrivateKey


def _hex(n: int):
    return format(n, 'x')


def _unhex(s: str):
    if s is None:
        return
    return int(s, 16)


class AsymmetricEncryptionInterface:
    def __init__(self, pubkey: PublicKey, privkey: PrivateKey = None):
        self.pubkey = pubkey
        self.privkey = privkey

    def __eq__(self, other):
        return self.pubkey == getattr(other, 'privkey', None) \
               and self.privkey == getattr(other, 'privkey', None)

    @classmethod
    def from_numbers(
            cls, n: int, e: int,
            d: int = None, p: int = None, q: int = None):
        if d is not None:
            privkey = PrivateKey(n, e, d, p, q)
        else:
            privkey = None
        pubkey = PublicKey(n, e)
        return cls(pubkey, privkey)

    def to_dict(self, private=False):
        if self.privkey is None or not private:
            return {k: _hex(getattr(self.pubkey, k)) for k in 'ne'}
        return {k: _hex(getattr(self.privkey, k)) for k in 'nedpq'}

    @classmethod
    def from_dict(cls, secret: dict):
        params = {k: _unhex(secret.get(k)) for k in 'nedpq'}
        return cls.from_numbers(**params)

    @classmethod
    def generate(cls, nbits=1024, poolsize=2, **kwargs):
        pubkey, privkey = rsa.newkeys(nbits, poolsize=poolsize, **kwargs)
        return cls(pubkey, privkey)

    def encrypt(self, message: bytes) -> bytes:
        return rsa.encrypt(message, self.pubkey)

    def encrypt_b64s(self, text: str) -> str:
        cipher = self.encrypt(text.encode('utf-8'))
        return base64.urlsafe_b64encode(cipher).decode()

    def decrypt(self, cipher: bytes) -> bytes:
        if self.privkey is None:
            raise RuntimeError('cannot decrypt without a private key')
        return rsa.decrypt(cipher, self.privkey)

    def decrypt_b64s(self, cipher_text: str) -> str:
        cipher = base64.urlsafe_b64decode(cipher_text.encode())
        return self.decrypt(cipher).decode('utf-8')

    def sign(self, message, hash_method: str = 'SHA-256'):
        if self.privkey is None:
            raise RuntimeError('cannot sign without a private key')
        return rsa.sign(message, self.privkey, hash_method)

    def verify(self, message: bytes, signature: bytes):
        return rsa.verify(message, signature, self.pubkey)
