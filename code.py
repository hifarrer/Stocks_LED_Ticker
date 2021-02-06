# Run on Metro M4 Airlift w RGB Matrix shield and 64x32 matrix display
# show current value of Bitcoin in USD

import time
import board
import terminalio
import random
from random import randrange

from adafruit_matrixportal.matrixportal import MatrixPortal

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
# You can display in 'GBP', 'EUR' or 'USD'
CURRENCY = "USD"
# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

from secrets import stocks
#matrixportal PRE-LOAD
matrixportal = MatrixPortal(
        default_bg=cwd + "/loading.bmp",
        status_neopixel = board.NEOPIXEL,
        debug=True
    )

def text_transform(val):
    if CURRENCY == "USD":
        return "$%d" % val
    if CURRENCY == "EUR":
        return "‎€%d" % val
    if CURRENCY == "GBP":
        return "£%d" % val
    return "%d" % val

#Text1 Price
matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(24, 22),
        text_color=0xffffff,
        text_transform=text_transform,
    )

matrixportal.preload_font(b"$012345789")  # preload numbers
matrixportal.preload_font((0x00A3, 0x20AC))  # preload gbp/euro symbol aa

time.sleep(1)#show first image


def getstocksdata(stock, profileid):
    print("getstocksdata start")
    print("profile id:", profileid)
    APIKEY = secrets["stocks_key"]
    # Set up where we'll be fetching data from
    DATA_SOURCE = "https://finnhub.io/api/v1/quote?symbol="+ stock +"&token="+ APIKEY
    DATA_LOCATION = ["c"] #for this API c means current price

    try:
        stocks_data = matrixportal.network.fetch(DATA_SOURCE)
        stock_price = matrixportal.network.json_traverse(stocks_data.json(), DATA_LOCATION)

    # pylint: disable=broad-except
    except Exception as error:
        print(error)

    stock_price = text_transform(stock_price)
    matrixportal.set_text(stock_price)
    matrixportal.set_background(cwd + "/stocks_background_"+str(profileid)+".bmp")


    #Text2 ticker
    matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(37, 7),
        text_color=0xFF0000,
        text_transform=text_transform,
    )
    matrixportal.set_text(stock, 1)


while True:
    for stock in stocks:
        print(stock)
        try:
            getstocksdata(stock, stocks.index(stock)+1) #the index will be used as bg
            print("after getstocksdata")
            time.sleep(1 * 10)

        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying! -", e)

