from pyModbusTCP.server import ModbusServer, DataBank
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import json
from configparser import ConfigParser

powervalues = {
    "L1": 0,
    "L2": 0,
    "L3": 0,
    "I1": 0,
    "I2": 0,
    "I3": 0,
    "P": 0, 
    "F": 0,
    "PIn": 0,
    "POut": 0
}
keymatch = {
    "L1": ["Spannung_L1", 2000, 2500, 40077, 1, [0]],
    "L2": ["Spannung_L2", 2000, 2500, 40078, 1, [0] ],
    "L3": ["Spannung_L3", 2000, 2500, 40079, 1, [0] ],
    "I1": ["Strom_L1", -3200, 3200, 40072, 2, [0]],
    "I2": ["Strom_L2", -3200, 3200, 40073, 2, [0]],
    "I3": ["Strom_L3", -3200, 3200, 40074, 2, [0]],
    "P": ["Wirkleistung", -17000, 17000, 40087, 0, []],
    "F": ["HZ", 400, 600, 40070, 1, []],
    "PIn": ["Power_in", 200, 5000000, 40090, 1, []],
    "POut": ["Power_out", 100, 5000000, 40091, 1, []]
}
db = DataBank()
config = ConfigParser()

def on_message(client, userdata, message, properties=None):
    data = json.loads(message.payload)['ZAEHLER']
    print(data)
    for keys, value in keymatch.items():
        val = int(data[value[0]] * pow(10, value[4]))
        if val > value[1] and val < value[2] and val not in value[5]:
            powervalues[keys] = val
        db.set_holding_registers(address=value[3], word_list=[powervalues[keys]])
        
        
def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(topic=config['mqtt']['subscription'])    

if __name__ == "__main__":
    config.read('/etc/mqtt2modbus.conf')
    modbus_server = ModbusServer(config['mbserver']['ip'], int(config['mbserver']['port']), no_block=True, ipv6=False,data_bank=db)
    modbus_server.start()
    mqtt_client = mqtt.Client(client_id=config['mqtt']['client_id'], transport="tcp", protocol=mqtt.MQTTv5)
    mqtt_client.connect(config['mqtt']['ip'], clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY,properties=Properties(PacketTypes.CONNECT))
    mqtt_client.on_message = on_message;
    mqtt_client.on_connect = on_connect;
    mqtt_client.loop_forever()
