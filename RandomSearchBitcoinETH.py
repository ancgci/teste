#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets
import multiprocessing
import datetime
from binascii import hexlify
from bit import Key
from bit.format import bytes_to_wif
from btcpy.setup import setup
from btcpy.structs.address import P2wpkhAddress
from btcpy.structs.crypto import PublicKey
from eth_keys import keys

setup('mainnet')

class BTCKey(Key):
    def __init__(self, wif=None):
        super().__init__(wif)

def seconds_to_str(elapsed=None):
    if elapsed is None:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        return str(datetime.timedelta(seconds=elapsed))

print('Loading address list...')
with open('BtcEthList.txt', 'r') as f:
    add = set(f.read().split())
print('Total addresses loaded:', len(add))

print('Starting search...')
print('Please wait...')

def seek(r):
    while True:
        # Gera um número aleatório criptograficamente seguro
        ran = secrets.randbelow(2**256)
        key1 = Key.from_int(ran)
        wif = bytes_to_wif(key1.to_bytes(), compressed=False)
        wif2 = bytes_to_wif(key1.to_bytes(), compressed=True)
        key2 = Key(wif)
        caddr = key1.address
        uaddr = key2.address
        saddr = key1.segwit_address
        
        # Fix bech32 address generation
        btc_key = BTCKey(wif2)
        bcaddr = btc_key.address    # Get the address directly
        
        # Generate public keys
        pub1 = hexlify(key1.public_key).decode()
        pub2 = hexlify(key2.public_key).decode()
        
        # Create P2WPKH addresses
        pubk1 = PublicKey.unhexlify(pub1)
        pubk2 = PublicKey.unhexlify(pub2)
        bcaddr = P2wpkhAddress(pubk1.hash(), version=0, mainnet=True)	#Segwit (bech32) compressed address
        buaddr = P2wpkhAddress(pubk2.hash(), version=0, mainnet=True)	#Segwit (bech32) uncompressed address
        myhex = "%064x" % ran
        private_key = myhex[:64]
        private_key_bytes = bytes.fromhex(private_key)
        public_key_hex = keys.PrivateKey(private_key_bytes).public_key
        public_key_bytes = bytes.fromhex(str(public_key_hex)[2:])
        eaddr = keys.PublicKey(public_key_bytes).to_address()			#Eth address

        if caddr in add:
            print("Nice One Found!!!", ran, caddr, wif2, private_key)
            with open("CompressedWinner.txt", "a") as f:
                f.write(f"{ran}:{caddr}:{wif2}:{private_key}\n")
            continue
        if uaddr in add:
            print("Nice One Found!!!", ran, uaddr, wif, private_key)
            with open("UncompressedWinner.txt", "a") as f:
                f.write(f"{ran}:{uaddr}:{wif}:{private_key}\n")
            continue
        if saddr in add:
            print("Nice One Found!!!", ran, saddr, wif, private_key)
            with open("Winner3.txt", "a") as f:
                f.write(f"{ran}:{saddr}:{wif}:{private_key}\n")
            continue
        if str(bcaddr) in add:
            print("Nice One Found!!!", ran, str(bcaddr))
            with open("bech32CompressedWinner.txt", "a") as f:
                f.write(f"{ran}:{bcaddr}:{wif}:{private_key}\n")
            continue
        if str(buaddr) in add:
            print("Nice One Found!!!", ran, str(buaddr))
            with open("bechUncompressedWinner.txt", "a") as f:
                f.write(f"{ran}:{buaddr}:{wif}:{private_key}\n")
            continue
        if eaddr in add:
            print("Nice One Found!!!", ran, private_key, eaddr)
            with open("EthWinner.txt", "a") as f:
                f.write(f"{ran}:{eaddr}:{wif}:{private_key}\n")
            continue
        else:
            colour_cyan = '\033[36m'
            colour_reset = '\033[0;0;39m'
            colour_red = '\033[31m'
            print(colour_cyan + seconds_to_str() + colour_red + "----- Random Search for Bitcoin and ETH Puzzle Wallets -----" + colour_cyan + myhex, end='\r' + colour_reset)

if __name__ == '__main__':
    # Usa todos os núcleos disponíveis
    cores = multiprocessing.cpu_count()
    print(f'Using {cores} CPU cores')
    with multiprocessing.Pool(cores) as p:
        p.map(seek, range(cores))