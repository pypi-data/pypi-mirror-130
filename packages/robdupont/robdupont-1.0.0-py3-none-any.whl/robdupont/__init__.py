import sys
from .sftp import Sftp

def get_cwd():
    return sys.argv[0][0: sys.argv[0].rfind('/') + 1]
