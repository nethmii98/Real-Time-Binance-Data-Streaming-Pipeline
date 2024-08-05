from kafka import KafkaProducer
from time import sleep
from json import dumps
import json
import websocket

# Initialize KafkaProducer instance
producer = KafkaProducer(
    bootstrap_servers=['your public IP:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8'),  
    api_version=(3, 7, 0)  
)

# Define a mapping for renaming keys in the incoming data
key_mapping = {
    "e": "event_type",
    "E": "event_time",
    "s": "symbol",
    "p": "price_change",
    "P": "price_change_percent",
    "w": "weighted_avg_price",
    "x": "prev_close_price",
    "c": "last_price",
    "Q": "last_qty",
    "b": "best_bid_price",
    "B": "best_bid_qty",
    "a": "best_ask_price",
    "A": "best_ask_qty",
    "o": "open_price",
    "h": "high_price",
    "l": "low_price",
    "v": "total_traded_base_asset_volume",
    "q": "total_traded_quote_asset_volume",
    "O": "statistics_open_time",
    "C": "statistics_close_time",
    "F": "first_trade_id",
    "L": "last_trade_id",
    "n": "total_number_of_trades"
}

def on_message(ws, message):
    """
    Handler for WebSocket messages.
    Transforms the incoming message and sends it to Kafka.
    """
    # Parse the incoming message
    data = json.loads(message)
    
    # Transform data using the key mapping
    transformed_data = {key_mapping.get(k, k): v for k, v in data.items()}
    
    # Print transformed data to console
    print(transformed_data)
    
    # Send the transformed data to Kafka topic 'demo_test'
    producer.send('binance_data', value=transformed_data)
    
    # Sleep for a second to control the flow of messages
    sleep(1)

def on_error(ws, error):
    """
    Handler for WebSocket errors.
    """
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """
    Handler for WebSocket closure.
    """
    print("WebSocket closed")

def on_open(ws):
    """
    Handler for WebSocket opening.
    Subscribes to the Binance streams.
    """
    params = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@ticker", "ethusdt@ticker", "bnbusdt@ticker"],  # Subscribe to ticker streams
        "id": 1
    }
    # Send subscription request to WebSocket
    ws.send(json.dumps(params))

def get_data():
    """
    Initialize and run the WebSocket client.
    """
    ws_url = "wss://stream.binance.com:9443/ws"  # Binance WebSocket URL

    # Create a WebSocket app and set up handlers
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # Run the WebSocket app
    ws.run_forever()

if __name__ == "__main__":
    # Start the WebSocket client
    get_data()
