import sys

from utils import process_gallery

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <SOURCE> <TARGET>")
        return

    # Get source and target directories from command-line arguments
    SOURCE = sys.argv[1]
    TARGET = sys.argv[2]
    process_gallery(SOURCE, TARGET)
