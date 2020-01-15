
# data pineline from Infura API (websocket) to Kafka producer
# extracts all the transactions as JSON objects

import sys
import websockets
import asyncio
import json

from kafka import KafkaProducer
from kafka.errors import KafkaError

async def extract(uri):

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer = lambda m: json.dumps(m).encode('utf-8'))

    async with websockets.connect(uri) as websocket:

        await websocket.send(json.dumps({"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}))
        greetings = await websocket.recv()

        while True:
            message = await websocket.recv()

            msg = json.loads(message)

            if "params" in msg: # is a block header
                block_hash = msg["params"]["result"]["hash"]
                print(block_hash)
                transaction_idx = 0
                request_tx = json.dumps(
                    {"jsonrpc":"2.0",
                    "method":"eth_getTransactionByBlockHashAndIndex",
                    "params": [str(block_hash), str(hex(transaction_idx))],
                    "id":1})
                await websocket.send(request_tx)

            elif "result" in msg: # is transaction

                if msg["result"] is not None:
                    producer.send('chain', msg["result"]) # produce json messages
                    transaction_idx += 1 # request next one
                    request_tx = json.dumps(
                        {"jsonrpc":"2.0",
                        "method":"eth_getTransactionByBlockHashAndIndex",
                        "params": [str(block_hash), str(hex(transaction_idx))],
                        "id":1})
                    await websocket.send(request_tx)

            else:
                print("Should never happen")
                print(msg)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: transaction_feeder.py <infura-ws-address>", file=sys.stderr)
        exit(-1)

    uri = sys.argv[1] # e.g. "wss://mainnet.infura.io/ws/v3/<APP-ID>""
    asyncio.get_event_loop().run_until_complete(extract(uri))
