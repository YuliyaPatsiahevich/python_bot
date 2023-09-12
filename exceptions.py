import json

import requests

from config import keys
class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote==base:
            raise APIException(f'Введенные валюты должны быть различными: {base}-{quote}.')
        quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Неудалось распознать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректно введено количество валюты {float(amount)}')
        if amount >=0:
            raise APIException('Ошибка. Количество валюты не может быть отрицательным числом')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]*amount
        return total_base