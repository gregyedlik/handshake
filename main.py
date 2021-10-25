import can
import pandas
import time
import binascii


def make_nice_hex_string(raw):
    string = binascii.hexlify(bytes(raw)).decode('utf-8')
    string = " ".join(string[i:i + 2] for i in range(0, len(string), 2))
    return string


bus = can.Bus(channel=0,
              interface='kvaser', # noqa
              receive_own_messages=True, # noqa
              bitrate=500000) # noqa

handshake = {0x72, 0x73, 0x80, 0x81}

wakeup = can.Message()

switchoff = can.Message(arbitration_id=0x61,
                        is_extended_id=False,
                        data=[0x00])

while 1:
    bus.send(wakeup)

    captured = []
    for msg in bus:
        if msg.arbitration_id in handshake:
            captured.append(msg)
            if msg.arbitration_id == 0x81:
                bus.send(switchoff)
                break

    captured_important = [[hex(msg.arbitration_id),
                           make_nice_hex_string(msg.data)]
                          for msg in captured]
    df = pandas.DataFrame(data=captured_important, columns=['arbitration ID', 'data'])
    df.to_csv('list.csv', index=False, mode='a', header=False)

    print('Success')

    time.sleep(5)
