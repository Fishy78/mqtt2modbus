# MQTT to Modbus Bridge

This project provides a Python-based bridge that reads power meter data delivered by MQTT and makes it available to Modbus devices. It is designed to work with an ESP8266 running Tasmota firmware configured to read data from a power meter using an optical reader.

## Features

- Converts power meter data received via MQTT to Modbus registers.
- Supports various power metrics like voltage, current, frequency, and power.
- Runs as a systemd service for easy deployment and management.

## Requirements

- Python 3.x
- Tasmota firmware on ESP8266 with an optical power meter reader.
- An MQTT broker.
- Modbus TCP server.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Fishy78/mqtt2modbus.git
cd mqtt2modbus
```

### 2. Install the required Python packages

Ensure you have Python 3.x installed. Then, install the required packages using pip:

```bash
pip install pyModbusTCP paho-mqtt
```

### 3. Configure the Tasmota ESP8266

Upload the following script to your Tasmota device to configure it for reading power meter data:

```plaintext
>D
>B
->sensor53 r
>M 1
+1,5,s,0,9600,ZAEHLER,1,10,2F3F210D0A,063035310D0A

1,77070100010800ff@1000,Gesamt kWh bezogen,kWh,Power_in,1
1,77070100020800ff@1000,Gesamt kWh geliefert,kWh,Power_out,1
1,77070100100700ff@1,Verbrauch aktuell,W,Wirkleistung,0
1,77070100200700ff@1,Voltage L1,V,Spannung_L1,1
1,77070100340700ff@1,Voltage L2,V,Spannung_L2,1
1,77070100480700ff@1,Voltage L3,V,Spannung_L3,1
1,770701001f0700ff@1,Amperage L1,A,Strom_L1,1
1,77070100330700ff@1,Amperage L2,A,Strom_L2,1
1,77070100470700ff@1,Amperage L3,A,Strom_L3,1
1,770701000e0700ff@1,Frequency,Hz,HZ,2
```

To configure Tasmota for MQTT, refer to the official [Tasmota MQTT Setup Guide](https://tasmota.github.io/docs/MQTT/).

### 4. Configure the `mqtt2modbus` script

Edit the `mqtt2modbus.conf` configuration file to match your environment:

```ini
[mbserver]
ip = 0.0.0.0
port = 502

[mqtt]
ip = 10.10.9.72
client_id = mqtt2modbus
subscription = tele/M-Stromzaehler1/SENSOR
```

### 5. Install the systemd service

1. Copy the service file to the systemd directory:

   ```bash
   sudo cp mqtt2modbus.service /etc/systemd/system/
   ```

2. Reload systemd to recognize the new service:

   ```bash
   sudo systemctl daemon-reload
   ```

3. Start the service:

   ```bash
   sudo systemctl start mqtt2modbus.service
   ```

4. Enable the service to start on boot:

   ```bash
   sudo systemctl enable mqtt2modbus.service
   ```

### 6. Check the service status

To check if the service is running correctly, use:

```bash
sudo systemctl status mqtt2modbus.service
```

### 7. Verify the Setup

- Ensure that your MQTT broker is receiving data from the Tasmota ESP8266.
- Verify that Modbus registers are being updated by polling the Modbus server.

## Modbus Register Addresses

The following Modbus addresses are used to query specific values. Each entry includes the Modbus register address, the length of the data, and the scaling factor (`10^x`), where `x` is negative for scaling down:

| **Metric**         | **Modbus Address** | **Register Type** | **Length (Registers)** | **Faktor 10<sup>x</sup>** |
|--------------------|---------------------|-------------------|------------------------|-----------------|
| Voltage L1         | 40077               | Holding Register  | 1                      | 10<sup>-1</sup>           |
| Voltage L2         | 40078               | Holding Register  | 1                      | 10<sup>-1</sup>           |
| Voltage L3         | 40079               | Holding Register  | 1                      | 10<sup>-1</sup>           |
| Current L1         | 40072               | Holding Register  | 1                      | 10<sup>-2</sup>           |
| Current L2         | 40073               | Holding Register  | 1                      | 10<sup>-2</sup>           |
| Current L3         | 40074               | Holding Register  | 1                      | 10<sup>-2</sup>           |
| Power (Wirkleistung) | 40087             | Holding Register  | 1                      | 10<sup>0</sup>            |
| Frequency (HZ)     | 40070               | Holding Register  | 1                      | 10<sup>-1</sup>            |
| Power_in           | 40090               | Holding Register  | 1                      | 10<sup>-1</sup>           |
| Power_out          | 40091               | Holding Register  | 1                      | 10<sup>-1</sup>           |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Support

If you encounter any issues, please create an issue in the [GitHub repository](https://github.com/Fishy78/mqtt2modbus/issues).
