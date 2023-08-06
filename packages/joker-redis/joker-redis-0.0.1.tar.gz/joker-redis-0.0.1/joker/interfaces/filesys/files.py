#!/usr/bin/env python3
# coding: utf-8

import base64
import mimetypes
import os.path
from typing import Generator

from joker.stream.utils import read_as_chunks, checksum_hexdigest


def b64_encode_data_url(mediatype: str, content: bytes):
    b64 = base64.b64encode(content).decode('ascii')
    return 'data:{};base64,{}'.format(mediatype, b64)


def b64_encode_local_file(path: str):
    mediatype = mimetypes.guess_type(path)[0]
    with open(path, 'rb') as fin:
        return b64_encode_data_url(mediatype, fin.read())


class FileStorageInterface:
    def __init__(self, base_dir: str):
        self.base_dir = os.path.abspath(base_dir)

    def under_base_dir(self, *paths):
        return os.path.join(self.base_dir, *paths)

    def read_as_chunks(self, path: str, length=-1, offset=0, chunksize=65536) \
            -> Generator[bytes, None, None]:
        path = self.under_base_dir(path)
        return read_as_chunks(
            path, length=length,
            offset=offset, chunksize=chunksize,
        )

    def checksum_hexdigest(self, path: str, algo='sha1') -> str:
        path = self.under_base_dir(path)
        return checksum_hexdigest(path, algo=algo)

    def read_as_binary(self, path: str):
        path = self.under_base_dir(path)
        with open(path, 'rb') as fin:
            return fin.read()

    def read_as_base64_data_url(self, path: str):
        path = self.under_base_dir(path)
        return b64_encode_local_file(path)

    def save_as_file(self, path: str, chunks):
        path = self.under_base_dir(path)
        with open(path, 'wb') as fout:
            for chunk in chunks:
                fout.write(chunk)


__all__ = [
    'FileStorageInterface',
    'b64_encode_data_url',
    'b64_encode_local_file',
]