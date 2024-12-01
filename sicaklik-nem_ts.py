import network
import time
import machine
import urequests
import dht

DHT_PIN = 4  
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

SSID = "WiFi_Network_Name"
PASSWORD = "WiFi_Password"

API_KEY = "ThingSpeak_API_Key"
THINGSPEAK_URL =f"https://api.thingspeak.com/update?api_key={API_KEY}"

wlan = network.WLAN(network.STA_IF)

def connect_wifi():
    global wlan
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Connection to Wifi", end="")
    while not wlan.isconnected():
        print(".", end= "")
        time.sleep(1)
    print("\nConnected to Wifi")
    print("IP adress: ", wlan.ifconfig()[0])


def read_temperature():
    sensor = machine.ADC(4)  # Sensörün bağlı olduğu pin
    conversion_factor = 3.3 / 65535
    reading = sensor.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return round(temperature, 2)


def read_dht_sensor():
    try:
        # Sensörden veriyi oku
        dht_sensor.measure()
        temperature = dht_sensor.temperature()  # Sıcaklık
        humidity = dht_sensor.humidity()        # Nem

        print(f"Sicaklik: {temperature}°C")
        print(f"Nem: {humidity}%")
        print(30*"-")
        return temperature, humidity
    except Exception as e:
        print("Error reading DHT11 sensor:", e)
        return None, None


def send_to_thingspeak(temperature , temperature2 , humidity ):
      try:
        # ThingSpeak'e veri gönder
        response = urequests.get(f"{THINGSPEAK_URL}&field1={temperature}&field2={ temperature2}&field3={humidity}")
        print("Data sent to ThingSpeak:", response.text)
        print(30*"-")
        response.close()
      except Exception as e:
        print("Failed to send data to ThingSpeak:", e)


connect_wifi()

while True:
    temperature = read_temperature()
    print(f"Sıcaklık :{temperature} °C (dahili)")
    temperature2 , humidity =read_dht_sensor()

    if temperature is not None and humidity is not None and temperature2 is not None :
        send_to_thingspeak(temperature,temperature2, humidity)
    else:
        print("No data to send.")
    
    time.sleep(20)
    if not wlan.isconnected():
       print("Wi-Fi disconnected. Reconnecting...")
       connect_wifi()







