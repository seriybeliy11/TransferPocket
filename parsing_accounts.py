import requests

url_template = 'https://api.tonscan.com/api/bt/getAccountsTop?limit=50&offset={offset}'
offset = 0

with open('active_accounts.txt', 'w') as f:
    while True:
        url = url_template.format(offset=offset)
        response = requests.get(url)

        if response.status_code != 200:
            print(f'Ошибка! Код ответа: {response.status_code}')
            break

        data = response.json()
        accounts = data['json']['data']['list']

        for account in accounts:
            address = account['address']
            friendly_name = account['friendly_name']
            balance = account['balance']

            f.write(f'Wallet: {address}\n')
            f.write(f' Balance: {balance}')
            

        offset += 50
