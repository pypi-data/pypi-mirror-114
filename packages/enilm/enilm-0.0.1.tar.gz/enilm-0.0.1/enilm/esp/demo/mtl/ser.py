import time
from typing import Iterable

import enilm
import numpy as np
import serial


def set_data(
        ser: serial.Serial,
        data: bytes,
        chunk_size_bytes: int = 90,
):
    enilm.esp.ser.flush(ser)
    inbuf_idx = 0
    for i in range(0, len(data), chunk_size_bytes):
        curr_chunk = data[i:i + chunk_size_bytes]

        # set index and update it
        ser.write(bytearray([ord('s')]) + int.to_bytes(inbuf_idx, length=4, byteorder='little'))
        inbuf_idx += len(curr_chunk)
        enilm.esp.ser.flush(ser)

        # send chunk
        ser.write(curr_chunk)
        enilm.esp.ser.flush(ser)


def infer_esp(
        data: Iterable[bytes],
        data_size: int,
        win_size: int,
        n_outputs: int,
        dtype,
        inference_indicator_line: str = 'Running inference and returning results',
) -> np.ndarray:
    ser = serial.Serial()
    ser.port = 'COM3'
    ser.baudrate = 115200
    ser.timeout = 1.0  # seconds
    ser.open()

    sizeof_float = np.dtype(dtype).itemsize
    outputs = np.zeros((data_size, n_outputs))
    for i, d in enumerate(data):
        assert len(d) == win_size * sizeof_float
        assert type(d) == bytes

        # progress
        print(f'Infer {i + 1}/{data_size}')

        # send data over UART
        set_data(ser, d)

        # read data
        ser.write(bytearray([ord('i')]))
        while True:
            try:
                line = ser.readline().decode().strip()
            except UnicodeDecodeError:
                continue
            print(line)
            if line == inference_indicator_line:
                data = ser.read(sizeof_float * n_outputs)
                outputs[i] = np.frombuffer(data, dtype=np.float32, count=3)
                break

        enilm.esp.ser.flush(ser)

    ser.close()
    return outputs


def main():
    win_size = 199
    n_outputs = 3

    xy = enilm.esp.demo.common.get_data()
    xy = enilm.esp.demo.common.norm(xy)
    xy = enilm.esp.demo.common.chunkize(xy, win_size)

    # limit = len(xy.x)
    limit = 100

    x = []
    for i in range(limit):
        x.append(bytes(xy.x[i]))

    p = infer_esp(
        x,
        data_size=limit,
        win_size=win_size,
        n_outputs=n_outputs,
        dtype=np.float32,
    )

    with open('p.npy', 'wb') as fp:
        np.save(fp, p)

    print(p)


if __name__ == '__main__':
    main()
