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


def receive(cap, SOC):
    bus.send(wakeup)
    for msg in bus:
        if msg.arbitration_id in handshake:
            cap.append(msg)
            time.sleep(0.01)
            if len(cap) == 4:
                break
        elif msg.arbitration_id == 0x111:
            string = make_nice_hex_string(msg.data)
            relevant = string[-2:]
            SOC_temp = int(relevant, 16)
            if SOC_temp > 0:
                SOC[0] = SOC_temp


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
    SOC = [101]
    p = threading.Thread(target=receive, args=[captured, SOC])
    p.start()
    p.join(timeout=5)
    bus.send(switchoff)

    captured_important = [[hex(msg.arbitration_id),
                           make_nice_hex_string(msg.data),
                           time.strftime("%d %b %H:%M:%S")]
                          for msg in captured]
    df = pandas.DataFrame(data=captured_important, columns=['arbitration ID', 'data', 'time'])
    print(df)

    if len(SOC) > 0:
        print('SOC: ' + str(SOC[0]) + '%')

        if SOC[0] < 5:
            print('Too low SOC, stopping recording.')
            break

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
