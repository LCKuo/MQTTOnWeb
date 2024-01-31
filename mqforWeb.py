# publish_basic.py
import time
import random
from paho.mqtt import client as mqtt_client

broker = '127.0.0.1'

port = 1883
keepalive = 60
topic2 = "/DCS/IOT/ARM1440/Axis5/Rotate"
topic3 = "/DCS/IOT/ARM1440/Axis4/Rotate"
topic4 = "/DCS/IOT/ARM1440/Axis3/Rotate"
topic5 = "/DCS/IOT/ARM1440/Axis2/Rotate"
topic1 = "/DCS/IOT/ARM1440/Axis1/Rotate"
topicrec = "/DCS/IOT/ARM1440/rec/r"

client_id = f'LC-mqtt-send'
ss = ""

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT successfully!")

        else:
            print("Failed to connect, return code {0}".format(rc))

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keepalive)
    return client


def publish(client):
    while True:
        time.sleep(1)
        # 接收 topicrec 的值
        client.subscribe(topicrec)
        #_, _, rec_value = client.subscribe(topicrec).payload.decode().split(",")
        global ss

        if ss == "A":
            do_publish(client,topic5,"AAA  "+str(random.uniform(-30, 30)))


        else:
            do_publish(client,topic5,"BBB  "+str(random.uniform(-30, 30)))


def do_publish(client, topic, msg):
    result = client.publish(topic=topic, payload=msg, qos=0, retain=True)
    if result[0] == 0:
        print("Send {0} to topic {1}".format(msg, topic))
    else:
        print("Failed to send message {0} to topic {1}".format(msg, topic))


def do_another_publish(client):
    # 實現另一種 publish 操作
    # 根據需求修改
    pass

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")
    global ss
    ss = msg.payload.decode()

def run():
    client = connect_mqtt()
    client.on_message = on_message

    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
