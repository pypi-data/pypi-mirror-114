#!/usr/bin/env python3
# coding: utf-8

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESKeyWrapper(object):
    iv_size = 16

    def __init__(self, key):
        self.key = key

    def get_cipher(self, iv):
        assert len(iv) == self.iv_size
        a = algorithms.AES(self.key)
        m = modes.CBC(iv)
        return Cipher(a, m, default_backend())

    @classmethod
    def generate_key(cls):
        return os.urandom(32)

    def encrypt(self, data, iv=None):
        assert isinstance(data, bytes)
        if not self.key:
            return data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        iv = iv or os.urandom(self.iv_size)
        encryptor = self.get_cipher(iv).encryptor()
        return iv + encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, data):
        assert isinstance(data, bytes)
        if not self.key:
            return data
        iv = data[:self.iv_size]
        data = data[self.iv_size:]
        decryptor = self.get_cipher(iv).decryptor()
        plaintext_padded = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(plaintext_padded) + unpadder.finalize()
