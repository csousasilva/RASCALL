import os

THIS_DIR = os.path.dirname(__file__)

def get_file(filename):
    return os.path.join(THIS_DIR, 'input', filename)
    if not os.path.isfile(filename):
        logging.error("Can't find input file: %s", filename)
    return filename