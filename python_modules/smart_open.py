#!/usr/bin/env python3
"""
Function for versatile opening of file/file paths/stdout to write to
"""
import sys
import io
from contextlib import contextmanager

@contextmanager
def smart_open(path, **kwargs):
    """Context manager managing a specified file (via a path or file_object) or sys.stdout"""
    close = False
    if not path:
        file_handle = sys.stdout
    elif isinstance(path, io.IOBase):
        file_handle = path
    else:
        file_handle = open(path, **kwargs)
        close = True
    yield file_handle
    if close:
        file_handle.close()

if __name__ == '__main__':
    pass