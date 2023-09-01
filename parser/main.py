from drawing import create_html
from parser import parse_website
from default_classes import ResponseCode


def main():
    response_code = parse_website()

    if response_code is not ResponseCode.EMPTY_DF:
        create_html()
    else:
        print(f"Response code is wrong: {response_code}.")


if __name__ == "__main__":
    main()
