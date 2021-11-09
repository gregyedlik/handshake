import can
import pandas
import time
import binascii
import threading

handshake = {0x72, 0x73, 0x80, 0x81}


def make_nice_hex_string(raw):
    string = binascii.hexlify(bytes(raw)).decode('utf-8')
    string = " ".join(string[i:i + 2] for i in range(0, len(string), 2))
    return string


def receive(cap):
    bus.send(wakeup)
    for msg in bus:
        if msg.arbitration_id in handshake:
            cap.append(msg)
            time.sleep(0.01)
            if len(cap) == 4:
                break


bus = can.Bus(channel=0,
              interface='kvaser', # noqa
              receive_own_messages=True, # noqa
              bitrate=500000) # noqa


wakeup = can.Message()

switchoff = can.Message(arbitration_id=0x61,
                        is_extended_id=False,
                        data=[0x00])

while 1:
    captured = []
    p = threading.Thread(target=receive, args=[captured])
    p.start()
    p.join(timeout=5)
    bus.send(switchoff)

    captured_important = [[hex(msg.arbitration_id),
                           make_nice_hex_string(msg.data),
                           time.strftime("%d %b %H:%M:%S")]
                          for msg in captured]
    df = pandas.DataFrame(data=captured_important, columns=['arbitration ID', 'data', 'time'])
    print(df)

    if len(captured) == 4:
        df.to_csv('list_scott.csv', index=False, mode='a', header=False)
        time.sleep(7)
    else:
        print("Incomplete sequence. Reinitialize...")
        time.sleep(10)
        print("Turn on...")
        bus.send(wakeup)
        time.sleep(10)
        print("Turn off...")
        bus.send(switchoff)
        time.sleep(10)
        print("Back to normal.")
