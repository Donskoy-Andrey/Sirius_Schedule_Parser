from drawing import create_html
from parser import parse_website
from utils.default_classes import ResponseCode
from datetime import datetime


def main():
    month = datetime.today().month
    response_code = parse_website(month=month)

    if response_code is not ResponseCode.EMPTY_DF:
        create_html()
    else:
        print(f"Response code is wrong: {response_code}.")


if __name__ == "__main__":
    main()
