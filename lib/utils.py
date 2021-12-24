def is_gz_file(file_path):
    with open(file_path, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'