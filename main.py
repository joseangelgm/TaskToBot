import sys

if __name__ == "__main__":

    # Check python version 3.9
    if sys.version_info < (3, 9):
        print("Python version has to be at least 3.9")
        sys.exit(-1)

    # Config log

    # Init Flask
