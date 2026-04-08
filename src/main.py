import sys

def main():
    if "android" in sys.platform:
        from gui import main as gui_main
        gui_main()
    else:
        from cli import main as cli_main
        cli_main()


if __name__ == "__main__":
    main()
