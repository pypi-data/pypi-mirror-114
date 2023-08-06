import pandas as pd
import os
from pandas_datareader import data as pdr
from bs4 import BeautifulSoup
import requests
from forex_python.converter import CurrencyRates
import datetime


class Information:
    def __init__(self):
        self.customers = {
            'Monty': {
                'location': 'EU',
                'volumes': 200,
                'comment': 'moving_average'
            },
            'Triangle': {
                'location': 'CN',
                'volumes': 30,
                'comment': 'monthly'
            },
            'Stone': {
                'location': 'EU',
                'volumes': 150,
                'comment': 'moving_average'
            },
            'Poly': {
                'location': 'EU',
                'volumes': 70,
                'comment': 'monthly'
            }
        }
        self.discounts = {'up to 100': 0.01,
                          'up to 300': 0.05,
                          '300 plus': 0.1}


class MyException(Exception):
    pass


def get_price_product_a(date):
    """
    Проверяет date и возвращает цену продукта А

    Parameters:
        date: День в формат datetime, timestamp

    Returns:
        Значение цены продукта А в день date

    Raises:
        MyException: когда date имеет некорректный формат

    """
    try:
        date = pd.to_datetime(date)
    except:
        raise MyException('Не распознан формат даты. Должен быть datetime, Timestamp')

    if pd.to_datetime(date).strftime('%Y-%m') == '2018-10':
        return 1600
    elif pd.to_datetime(date).strftime('%Y-%m') == '2018-11':
        return 1550
    elif pd.to_datetime(date).strftime('%Y-%m') == '2019-02':
        return 1600
    else:
        return 0


def get_price_with_discounts(date,
                             oil_price='auto',
                             barrels_to_one_ton=16,
                             production_cost=400,
                             client='Noname',
                             eurusd_rate='auto',
                             discount_on_price_a=True,
                             discount_from_volume=True,
                             add_logistic_cost=True,
                             cn_logistic_cost_usd=130,
                             eu_logistic_cost_eur=30):
    """
    Получает цену на нефть, курс Евро.
    Рассчитывает цену на продукт ВБП с завода
    Рассчитывает скидку от объемов покупки продукта ВБП
    Рассчитывает скидку от цены продукта А
    Рассчитывает стоимость доставки клиенту

    Parameters:
        date: День в формат datetime, timestamp
        oil_price: Цена на нефть в USD. Если 'auto', цена будет взята из yahoo
        barrels_to_one_ton: Количество баррелей нефти для производства 1 тонны ВБП
        production_cost: Стоимость производства 1 тонны ВБП
        client: Название клиента
        eurusd_rate: курс евро к доллару. Если 'auto', курс будет взят с forex_python.converter.CurrencyRates
        discount_on_price_a: признак применения скидки от цена продукта А
        discount_from_volume: признак применения скидки от объемов покупки
        add_logistic_cost: признак применения цены логистики
        cn_logistic_cost_usd: цена доставки для Китая
        eu_logistic_cost_eur: цена доставки для Европы

    Returns:
        Цена на продукт ВБП

    Raises:
        MyException: когда date имеет некорректный формат

    """
    try:
        date = pd.to_datetime(date)
    except:
        raise MyException('Не распознан формат даты. Должен быть datetime, Timestamp')

    # получем цену на нефть
    if oil_price == 'auto':
        oil_price_usd = get_brent_rate(date)
    else:
        oil_price_usd = oil_price

    # получаем курс евро
    if eurusd_rate == 'auto':
        usd_eur_rate = get_currency_rate_eur(date, 'USD')
    else:
        usd_eur_rate = 1 / eurusd_rate

    # рассчитываем цену на ВБП
    try:
        price = ((oil_price_usd * usd_eur_rate) * barrels_to_one_ton) + production_cost
    except:
        price = 0

    # рассчитываем скидки
    if discount_on_price_a:
        discount_on_price_a = get_discount_on_price_a(price_a=get_price_product_a(date),
                                                      price_b=price)
    else:
        discount_on_price_a = 0

    if discount_from_volume:
        discount_from_volume = (price * get_volume_discount(client))
    else:
        discount_from_volume = 0

    # рассчитываем затраты на доставку
    if add_logistic_cost:
        logistic_cost = get_logistic_cost(client, eu_logistic_cost_eur, cn_logistic_cost_usd)
    else:
        logistic_cost = 0
    return round(price - discount_on_price_a - discount_from_volume + logistic_cost, 2)


def get_logistic_cost(client='Noname', eu_logistic_cost_eur=30, cn_logistic_cost_usd=130):
    """
    Проверяет регион клиента и возвращает цену доставки

    Parameters:
        client: Название клиента
        cn_logistic_cost_usd: цена доставки для Китая
        eu_logistic_cost_eur: цена доставки для Европы

    Returns:
        Стоимость логистики продукта

    """
    info = Information()
    try:
        location = info.customers.get(client).get('location')
    except:
        print('Не найден клиент. Затраты на доставку = 0')
        return 0

    if location == 'EU':
        return eu_logistic_cost_eur
    elif location == 'CN':
        return cn_logistic_cost_usd
    else:
        print(f'Нет информации по доставке в регион {location}. Затраты на доставку = 0')
        return 0


def get_volume_discount(client='Noname'):
    """
    Возвращает значение скидки в зависимости от объемов покупок

    Parameters:
        client: Название клиента


    Returns:
        Значение скидки

    """
    info = Information()
    try:
        volume = info.customers.get(client).get('volumes')
    except:
        print(f'Не найдены объемы покупок для клиента {client}. Скидка равна 0')
        return 0

    if volume == 0:
        return 0
    elif volume >= 300:
        return 0.1
    elif volume >= 100:
        return 0.05
    elif volume > 0:
        return 0.01
    else:
        return 0


def get_discount_on_price_a(price_a, price_b):
    """
    Проверяет цены на продукты А и ВБП.
    Если продукт А дешевле, возвращает разницу

    Parameters:
        price_a: Цена на товар А
        price_b: Цена на товар ВБП

    Returns:
        Значение скидки

    """
    if price_a == 0:
        return 0
    elif price_b <= price_a:
        return 0
    elif price_b > price_a:
        return price_b - price_a
    else:
        return 0


def get_currency_rate_eur(date=datetime.datetime(2018, 1, 5), currency='USD'):
    """
    Возвращает отношение currency к Евро из библиотеки forex_python.converter.CurrencyRates

    Parameters:
        date: День в формат datetime, timestamp
        currency: Валюта, к которому необходимо получить курс Евро

    Returns:
        Отношение currency к Евро

    Raises:
        MyException: когда date имеет некорректный формат
        MyException: когда не найден курс для валюты за 5 дней

    """
    try:
        date = pd.to_datetime(date)
    except:
        raise MyException('Не распознан формат даты. Должен быть datetime, Timestamp')

    c = CurrencyRates()
    days_back = 0
    while days_back < 5:  # 5 попыток получить валюту в предыдущих днях
        try:
            rate = c.get_rate(currency, 'EUR', date - datetime.timedelta(days=days_back))
        except:
            days_back += 1
        else:
            return rate
    raise MyException(f'Не найден курс для {currency} на {date}')


def get_brent_rate(date):
    """
    Возвращает стоимость 1 барреля нефти из библиотеки pandas_datareader

    Parameters:
        date: День в формат datetime, timestamp

    Returns:
        Курс на баррель нефти Brent

    Raises:
        MyException: когда date имеет некорректный формат

    """
    try:
        date = pd.to_datetime(date)
    except:
        raise MyException('Не распознан формат даты. Должен быть datetime, Timestamp')
    data = pdr.DataReader('BZ=F', 'yahoo')
    days_back = 0
    while days_back < 5:  # 5 попыток получить стоимость нефти в предыдущих днях

        try:
            rate = data.loc[(date - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')].Open
        except:
            days_back += 1
        else:
            try:
                if len(rate) > 1:  # DataReader иногда возвращает 2 строки с одной датой
                    return rate[0]
            except:
                return rate
    raise MyException(f'Не найден курс для нефти в {date}')


def get_rub_eur_rate(date):
    """
    Возвращает курс рубля к евро с сайта ЦБ РФ

    Parameters:
        date: День в формат DD.MM.YYYY

    Returns:
        Курс рубля к евро

    Raises:
        MyException: когда date имеет некорректный формат
        MyException: когда на сайте ЦБ РФ нет ставки в date

    """
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        raise ValueError("Некорректный формат даты, должен быть DD.MM.YYYY")

    url = f'http://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01239&UniDbQuery.From={date}&UniDbQuery.To={date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        number = soup.find('table', {'class': 'data'}).text.find(date)
    except:
        raise MyException(f'На сайте ЦБ РФ нет ставки за день {date}')
    else:
        return float(soup.find('table', {'class': 'data'}).text[number + 13:number + 20].replace(',', '.'))


def script_for_2task():
    client = input('Введите название компании (Monty, Triangle, Stone, Poly): ')
    date = input('Введите дату в формате YYYY-MM-DD: ')
    return print(get_price_with_discounts(date=datetime.datetime(int(date.split('-')[0]),
                                                           int(date.split('-')[1]),
                                                           int(date.split('-')[2])),
                                    oil_price='auto',
                                    eurusd_rate='auto',
                                    client=client,
                                    discount_on_price_a=True,
                                    discount_from_volume=True,
                                    add_logistic_cost=True,
                                    barrels_to_one_ton=16,
                                    production_cost=400,
                                    cn_logistic_cost_usd=130,
                                    eu_logistic_cost_eur=30))


def script_for_3task():
    date = input('Введите дату в формате YYYY-MM-DD: ')
    year = date.split('-')[0]
    month = date.split('-')[1]
    day = date.split('-')[2]
    price = get_price_with_discounts(date=datetime.datetime(int(year),
                                                            int(month),
                                                            int(day)),
                                     oil_price='auto',
                                     eurusd_rate='auto',
                                     client='Noname',
                                     discount_on_price_a=True,
                                     discount_from_volume=False,
                                     add_logistic_cost=False,
                                     barrels_to_one_ton=16,
                                     production_cost=400,
                                     cn_logistic_cost_usd=130,
                                     eu_logistic_cost_eur=30)

    rate = get_rub_eur_rate(f'{day}.{month}.{year}')
    print(f'Price is: {price} EUR or {round(price * rate, 2)} RUB')
