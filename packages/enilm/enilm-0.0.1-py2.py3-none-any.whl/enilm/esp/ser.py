import time

import serial


def start_interactive_serial(port: str = 'COM3', baudrate: int = 115200, timeout: float = 1.0, time_limit: int = 5):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate
    ser.timeout = timeout  # seconds
    ser.open()

    mode = 'ascii'
    connected = True
    print(f'mode is {mode}')
    print('[h]elp, e[x]it')
    while True:
        # process input
        _in = input('Enter: ')
        if _in == 'x':
            if connected:
                ser.close()
            break
        elif _in == 'h':
            print(f'connected: {connected}\n'
                  f'mode: {mode}\n')

            print('ma: change mode to ascii\n'
                  'mh: change mode to hex\n'
                  'dis: disconnect\n'
                  'con: connect\n')

            print('r: Set input buffer index to zero.\n'
                  '0: Set input buffer to zero.\n'
                  'n: Inspect input buffer.\n'
                  'i: Running inference and returning results\n'
                  'cX: Change model to X where X can be: [f]ridge, [d]ish washer, [w]ashing machine\n'
                  'sXXXX: set input buffer index to XXXX.\n'
                  'else: Copy received data to input buffer at input buffer index.\n')
            continue
        elif _in == 'ma':
            mode = 'ascii'
            print(f'changed mode to {mode}')
            continue
        elif _in == 'mh':
            mode = 'hex'
            print(f'changed mode to {mode}')
            continue
        elif _in == "dis":
            if connected:
                ser.close()
                connected = False
                print('Disconnected')
            continue
        elif _in == 'con':
            if not connected:
                ser.open()
                connected = True
                print('Connected')
            continue

        # check connection
        if not connected:
            print('Not connected!')
            continue

        # write over serial
        try:
            if mode == 'hex':
                ser.write(bytearray.fromhex(_in))
            elif mode == 'ascii':
                ser.write(_in.encode(encoding='ascii'))
        except Exception as e:
            print(e)
            continue

        # read result
        start = time.time()
        while ser.readable():
            line = ser.readline()

            # end?
            if line == b'':
                break

            # decode
            try:
                decoded_line = line.decode()
                print(decoded_line, end='')

                # next is input array?
                if 'Sending back input buffer' in decoded_line:
                    print(ser.readline())

            except UnicodeDecodeError:
                print(line)

            # halt?
            if (time.time() - start) > time_limit:
                print(f"Halting since printing took more than {time_limit} seconds")
                break


def flush(ser: serial.Serial):
    time.sleep(.1)
    ser.flush()
