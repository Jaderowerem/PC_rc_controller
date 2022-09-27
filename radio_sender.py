import nrf24
import pigpio
import time
import struct
import traceback

pi = pigpio.pi()
nrf = nrf24.NRF24(pi, ce=25, payload_size=nrf24.RF24_PAYLOAD.DYNAMIC,
                  channel=100, data_rate=nrf24.RF24_DATA_RATE.RATE_250KBPS,
                  pa_level=nrf24.RF24_PA.LOW)

address = "00001"
nrf.set_address_bytes(len(address))
nrf.open_writing_pipe(address)

nrf.show_registers()

try:
    print(f'Send to {address}')
    count = 0
    while True:
        temperature = 23.0
        humidity = 60.0
        print(f'Sensor values: temperature={temperature}, humidity={humidity}')

        payload = struct.pack("<Bff", 0x01, temperature, humidity)
        print("payload:", payload)

        nrf.reset_packages_lost()
        nrf.send(payload)
        try:
            nrf.wait_until_sent()
        except TimeoutError:
            print('Timeout waiting for transmission to complete.')
            time.sleep(10)
            continue

        if nrf.get_packages_lost() == 0:
            print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
        else:
            print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")

        # Wait 10 seconds before sending the next reading.
        time.sleep(10)

except:
    traceback.print_exc()
    nrf.power_down()
    pi.stop()
