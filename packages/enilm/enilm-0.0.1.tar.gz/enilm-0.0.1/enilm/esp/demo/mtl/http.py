import enilm
import numpy as np


def main():
    win_size = 199
    n_outputs = 3

    xy = enilm.esp.demo.common.get_data(skip_days=2)
    xy = enilm.esp.demo.common.norm(xy)
    xy = enilm.esp.demo.common.chunkize(xy, win_size)

    enilm.esp.http.set_params(enilm.esp.http.Params(
        win_size=win_size,
        inbuf_size=win_size * 4,
        n_outputs=3,
        outbuf_size=3 * 4,
        esp_url='http://192.168.178.158/',
    ))

    # pred
    start = 0
    n_samples = 100
    _s = slice(start, start + n_samples)
    pred = np.zeros((n_samples, n_outputs))
    for i in range(n_samples):
        pred[i] = enilm.esp.http.get_inference_result(xy.x[_s][i])


if __name__ == '__main__':
    main()
