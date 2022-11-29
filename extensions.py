import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту сбережений {base}. Попробуйте еще раз!')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту, на которую вы хотите обменять сбережения {quote}. Попробуйте еще раз!')
        if quote == base:
            raise APIException(f'Ой! Вы ввели одинаковые валюты для расчета сбереженй: {base}. Попробуйте снова!')

        try:
            amount = float(amount)


        except ValueError:
            raise APIException(f'Не удалось обработать количество сбережений {amount}. Попробуйте еще раз!')
        if amount < 0:
            raise APIException(f'Отрицательное количество валюты сбережений. Попробуйте еще раз!')
        if amount == float('inf'):
            raise APIException(f'Вы ввели недопустимо длинное число')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        total_base = total_base * amount

        return total_base