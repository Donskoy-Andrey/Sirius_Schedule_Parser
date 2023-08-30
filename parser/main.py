from drawing import create_html
from parser import parse_website


def main():
    parse_website()
    create_html()


if __name__ == "__main__":
    main()
