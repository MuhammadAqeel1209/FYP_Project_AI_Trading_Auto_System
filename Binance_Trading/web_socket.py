import websockets
import json
import pandas as pd
import asyncio

def createDataFrame(msg):
    df = pd.DataFrame([msg])
    df = df[['s', 'E', 'c']]  # Fixed index selection with column names
    df.columns = ['Symbol', 'Time', 'Price']
    df['Price'] = df['Price'].astype(float)
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    return df

async def main():
    # Initialize stream connection within the function
    stream = websockets.connect('wss://stream.binance.com:9443/stream?streams=adausdt@miniTicker')
    async with stream as receiver:
        while True:
            data = await receiver.recv()
            try:
                # Correct the key typo here
                data = json.loads(data)['data']
                df = createDataFrame(data)
                print(df)
            except KeyError as e:
                print(f"KeyError: {e} - Check if the incoming message format matches expected structure.")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
