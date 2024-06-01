import asyncio

from pytonlib import TonlibClient

from tonsdk.utils import to_nano, b64str_to_bytes
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.contract import Address
from tonsdk.boc import Cell, Slice

from ton.utils import read_address

from get_collection import pytonlib_get_data as get_collection_data

import TonTools
from secret import mainnet_api_key

import requests
from pathlib import Path


async def tontools_get_data():
    client = TonTools.TonCenterClient(key=mainnet_api_key)

    collection = TonTools.NftCollection(data='коллекция', provider=client)

    await collection.update()

    await collection.get_collection_items(limit_per_one_request=10)

    print(collection)


async def get_client():
    url = 'https://ton.org/global-config.json'

    config = requests.get(url).json()

    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True, exist_ok=True)

    client = TonlibClient(ls_index=2, config=config, keystore=keystore_dir, tonlib_timeout=10)

    await client.init()

    return client


async def get_nft_address(client, index: int):
    stack = (await client.raw_run_method(address='коллекция',
                                         method='get_nft_address_by_index', stack_data=[["number", index]]))['stack']
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[0][1]['bytes']))).to_string(True, True, True)
    return nft_address



async def main():
    data = await get_collection_data()
    next_item_index = data[0]

    client = await get_client()
    with open('items_for_transfering.txt', 'w', encoding='utf-8') as f:
        for index in range(0, next_item_index):
            nft_address = await get_nft_address(client, index)
            print(nft_address)
            f.write(nft_address + '\n')

    await client.close()


if __name__ == '__main__':
    asyncio.run(main())
