import requests


class KursApi:
    KURS_API_KEY = '5e04dd3c439ab55263ffbabaf384fb54'

    def __init__(self, api_key=KURS_API_KEY):
        self.api_id = api_key

    def _data_parse(self):
        pass

    def get_forex_on_date(self, date, format):
        r = requests.get(f"http://api.kursna-lista.info/{self.api_id}/kl_na_dan/{date}/{format}")
        data = r.json()


    # datum = '12.03.2019'  # dd.mm.yyyy
    # format = 'json'

    # print(r)
    #
    # print(r.json())
    # print(r.headers.get('Date'))
    # data = r.json()
    # print(data["result"]['date'])
    # print(data["result"]['eur'])
    # print(data["result"]['eur']['sre'])
