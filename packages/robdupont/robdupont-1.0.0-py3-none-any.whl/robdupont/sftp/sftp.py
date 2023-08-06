import sys
import pysftp
import os 

class Sftp():
    """Implementation of a sftp connection"""
    def __init__(self, server, username, password, port, ssh_key_path=None):
        cnopts = pysftp.CnOpts(os.path.dirname(__file__) + "/fake_ssh_keys" if ssh_key_path is None else ssh_key_path)
        if ssh_key_path is None:
            cnopts.hostkeys = None
        self.connection = pysftp.Connection(host=server, username=username, password=password, port=port, cnopts=cnopts)

    def disconnect(self):
        self.connection.close()

    def get(self, remote_path, local_path):
        self.connection.get(remote_path, local_path)

    def put(self, remote_path, local_path):
        self.connection.put(local_path, remote_path)

    def get_files_in_path(self, path):
        return self.connection.listdir_attr(path)

    def get_filename(self, file):
        return file.filename

    def get_file_time(self, file):
        return file.st_mtime

    def get_file_size(self, file):
        return int(file.st_size)

    def dir_exist(self, path):
        return self.connection.isdir(path)

    def is_dir(self, file):
        return file.longname[0] == 'd'

    def mv(self, remote_src, remote_dest):
        self.connection.rename(remote_src, remote_dest)