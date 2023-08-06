import sys
import requests

onvista_url = "https://www.onvista.de/"


def parse_price(isin):
    response = requests.get(onvista_url + isin)
    price_string = response.text.split("ask")[1].split(":")[1].split(",")[0]
    return float(price_string)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You must provide exactly one argument.")
    else:
        print(parse_price(sys.argv[1]))
