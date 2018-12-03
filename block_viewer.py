import click
import requests
from pathlib import Path
from parser.block import Block

BASE_URL = "https://webbtc.com/block/%s.bin"


def download_file(filename, block_hash):
    r = requests.get(BASE_URL % block_hash, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return filename
    return None


def parse_block(filename):
    with open(filename, "rb") as f:
        block = Block(f)
        print(block)


@click.command()
@click.argument('block_hash')
def run(block_hash):
    filename = "./data/%s.bin" % block_hash
    if not Path(filename).is_file():
        filename = download_file(filename, block_hash)

    if filename:
        parse_block(filename)
    else:
        click.echo("Can't retrieve the block: %s from webbtc, please change the block hash or retry later" % block_hash)


if __name__ == '__main__':
    run()
