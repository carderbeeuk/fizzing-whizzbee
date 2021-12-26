import shutil
import os
import gzip


class FileHandler():
    def __init__(self, src_file_path, dest_file_path=None):
        self.src_file_path = src_file_path
        self.dest_file_path = dest_file_path

    def is_gz_file(self):
        with open(self.src_file_path, 'rb') as test_f:
            return test_f.read(2) == b'\x1f\x8b'

    def unzip_file(self):
        if self.is_gz_file():
            with gzip.open(self.src_file_path, 'rb') as f_in:
                with open(self.dest_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(self.src_file_path)

        else:
            os.rename(self.src_file_path, self.dest_file_path)