import requests, json, time, threading
from datetime import datetime, timezone

currency = ['bitcoin','ethereum','tron','doge','ripple','bnb','cardano','stellar','sui','shib','link']
c_list = ','.join(currency) #CurrencyList(currency)
t_val = 30
table_name='crypto_price_data'
query_for_create_table = f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT PRIMARY KEY AUTO_INCREMENT,
    currency_name VARCHAR(50),
    price_usd DECIMAL(18, 8),
    datetime_utc DATETIME
);
'''

def get_crypto_currency_data():
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={c_list}&vs_currencies=usd'
    data = requests.get(url).json()
    utc_now = datetime.now(timezone.utc)
    print('***************** NEW DATA *****************')
    print(data)
    print()

def task_get_data_in_time_gap(t_val):
    while True:
        get_crypto_currency_data()
        time.sleep(t_val)


if __name__=="__main__":
    task_thread = threading.Thread(target=task_get_data_in_time_gap(t_val))
    task_thread.start()


    # try:
    #     while True:
    #         time.sleep(0.1)
    # except KeyboardInterrupt:
    #     print("Exiting...")