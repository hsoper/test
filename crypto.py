import requests
import json
import pandas as pd
import sqlalchemy as sq
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


# Test when if the input is a supported crypto in the correct format
# Check for null inputs
def get_coingecko_json(coin):
    baseURL = ('https://api.coingecko.com/'
               + 'api/v3/simple/price?ids=')
    response = requests.get(baseURL + str(coin) + '&vs_currencies=usd')
    if response.json() == requests.get(baseURL + 'w'
                                       + '&vs_currencies=usd').json():
        print("That is not a valid crypto name. Heres the value of bitcoin")
        return requests.get(baseURL + "bitcoin" + '&vs_currencies=usd').json()
    print(response.json())
    return response.json()


# check if the function returns a 2d array and not a none object
def get_names_and_usd(json):
    temp = [[], []]
    for key, usd in json.items():
        temp[0].append(key)
        for k, i in usd.items():
            temp[1].append(float(i))
    return temp


# deleted get_get_users_coinusd() since its
# function is similar to get_coingecko_json()
# check when the input is a null for the list
# check when the json file is empty
def append_json_values(lis, json):
    temp = get_names_and_usd(json)
    if type(lis) is not list:
        return temp
    for i in range(0, len(temp)):
        for x in temp[i]:
            lis[i].append(x)
    return lis


# check when the input is an empty list/invalid
# check when when the list contains the wrong types. (not a string or float)
def make_dataframe(coin_usd):
    if type(coin_usd) is not list:
        print("Sorry that is not a valid input. Your input will be returned.")
        return coin_usd
    if (len(coin_usd) != 2
            or type(coin_usd[1]) is not list
            or type(coin_usd[0]) is not list):
        print("Sorry that is not a valid input. Your input will be returned.")
        return coin_usd
    dcoins = {"Coin": coin_usd[0], "PriceUSD": coin_usd[1]}
    dcoins = pd.DataFrame.from_dict(dcoins)
    return dcoins


# no return value
# Possibly check the inputs of the method
def sendto_database(datafr, database, table):
    engine = sq.create_engine('mysql://root:codio@localhost/' + database)
    datafr.to_sql(table, con=engine, if_exists='replace', index=False)


def save_database(database, file):
    os.system("mysqldump -u root -pcodio " +
              database + " > " + file)


def get_database(database, file):
    os.system("mysql -u root -pcodio " +
              database + " < " + file)


def get_table(database, table):
    engine = sq.create_engine('mysql://root:codio@localhost/'
                              + database)
    return pd.read_sql_table(table, con=engine)


def update_table_coin(database, table, price, crypto):
    engine = sq.create_engine('mysql://root:codio@localhost/'
                              + database)
    meta = sq.MetaData()
    con = engine.connect()
    tab = sq.Table(table, meta, autoload=True, autoload_with=engine)
    q = sq.update(tab).values(PriceUSD=price).where(tab.columns.Coin ==
                                                    crypto)
    con.execute(q)


# get_database("crypto",'crypto.sql')
coins = get_coingecko_json('ethereum,monero,dash,litecoin')
tether = coins['dash']['usd']
monero = coins['monero']['usd']
ethereum = coins['ethereum']['usd']
bitcoin = coins['litecoin']['usd']
coin = make_dataframe(get_names_and_usd(coins))
# sendto_database(coin,'crypto','CoinPrices')
# update_table_coin('crypto', 'CoinPrices', tether, 'dash')
# update_table_coin('crypto', 'CoinPrices', monero, 'monero')
# update_table_coin('crypto', 'CoinPrices', bitcoin, 'litecoin')
# update_table_coin('crypto', 'CoinPrices', ethereum, 'ethereum')


def make_barChart(dataframe, titles, values, x_label, graph_title):
    title = dataframe[titles]
    y_pos = np.arange(len(title))
    prices = [float(i) for i in dataframe[values]]
    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, prices, align='center',
                    label=dataframe[values])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(title)
    ax.invert_yaxis()
    ax.set_xlabel(x_label)
    ax.set_title(graph_title)
    ax.legend()
    plt.show()


# make_barChart(coin, 'Coin', 'PriceUSD', 'Prices',
#               "Some Crypto with their prices")
# coin = get_table('crypto','CoinPrices')
print(coin['PriceUSD'].mean())
print(coin['PriceUSD'].median())
print(coin['PriceUSD'].value_counts())
