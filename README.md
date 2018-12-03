# block-viewer

This program is used to reach webbtc.com to retrieve the binary of block, decode the header and first 5 transactions and display them to the terminal

## Setup

set up python3 virtual environment
```
python3 -m venv venv

source ./venv/bin/activate

pip install -r requirements.txt
```

## Usage

> Make sure run the following command in previouse created virtual enviroment

```
python block_viewer.py 000000000000000002775ff227222f47a46cad46b0f634db53c1a8737d7ecd41
```

## Limitation 
1. Didn't handle the segwit address(there is no segwit transaction on webbtc)
2. Only handle the P2PKH and P2SH transaction output
