import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
from datetime import datetime

DEVICE_ID = "a1143159-86be-43cf-b604-d397ead8b800"
SECRET_KEY = "Msg?JldOtN#2VUoWj4RJsdefM"

csv_file = open('sensor_data.csv', mode='a', newline='')
csv_file.write("Timestamp, Temperature, Humidity\n")

def on_temperature_changed(client, value):
    print(f"New temperature: {value}")
    write_to_csv(value, None)

def on_humidity_changed(client, value):
    print(f"New humidity: {value}")
    write_to_csv(None, value)

def write_to_csv(temperature, humidity):
    timestamp = datetime.now().isoformat()
    if temperature is not None:
        csv_file.write(f"{timestamp}, {temperature},\n")
    elif humidity is not None:
        csv_file.write(f"{timestamp}, , {humidity}\n")
    else:
        csv_file.write(f"{timestamp}, , \n")

def main():
    print("main() function")

    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    client.register("temperature", value=None, on_write=on_temperature_changed)
    client.register("humidity", value=None, on_write=on_humidity_changed)

    client.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback)
        print(f"{exc_type.__name__}: {exc_value}")
    finally:
        csv_file.close()

