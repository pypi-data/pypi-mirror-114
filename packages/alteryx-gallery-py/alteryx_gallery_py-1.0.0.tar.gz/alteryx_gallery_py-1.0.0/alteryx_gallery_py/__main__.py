# __main__.py

from .subscriptions import Subscriptions

def main():
    """Print description of package"""
    print(f"""The alteryx_gallery_py package uses the Alteryx Gallery API 
    connection to connect to Alteryx through Python. This package is intended 
    to be imported for use in other scripts/modules. See README.md for 
    details of use.""")

if __name__ == "__main__":
    main()
