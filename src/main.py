import sys

from utils import process_gallery


if __name__ == "__main__":
    # Get source and target directories from command-line arguments
    SOURCE = sys.argv[1]
    TARGET = sys.argv[2]
    process_gallery(SOURCE, TARGET)
