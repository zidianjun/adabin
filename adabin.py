

import numpy as np


def _bin_map(matrix, factor):
    mat = np.where(~np.isnan(matrix), matrix, 0.)
    height, width = mat.shape
    res_h, res_w = int(height / factor), int(width / factor)
    tail_h, tail_w = height % factor, width % factor
    in_mat = mat[:(height - tail_h), :(width - tail_w)]
    in_h, in_w = in_mat.shape
    out_mat = in_mat.reshape(res_h, factor, res_w, factor).mean(1).mean(2)
    res = np.kron(out_mat, np.ones((factor, factor)))
    if width % factor != 0:
        res = np.concatenate([res, np.tile(res[:, -1], (tail_w, 1)).T], axis=1)
    if height % factor != 0:
        res = np.concatenate([res, np.tile(res[-1], (tail_h, 1))], axis=0)
    return res


def multi_order_bin(signal, noise, min_SN=3):
    shape = signal.shape
    
    res_signal = signal.copy()
    res_noise = noise.copy()
    maps = np.zeros(shape)
    sn = signal / noise

    for i in range(1, int(np.log(min(shape)) / np.log(2)) + 1):
        k = 2 ** i
        s = _bin_map(signal, k)
        n = np.sqrt(_bin_map(noise**2, k)) / k
        res_signal = np.where(sn > min_SN, res_signal, s)
        res_noise = np.where(sn > min_SN, res_noise, n)
        maps[res_signal == s] = i
        sn = s / n

    return res_signal, res_noise, maps


def reconstruct_maps(signal, noise, maps):
    s_list, n_list = [signal], [noise]
    s, n = np.zeros((signal.shape)), np.zeros((noise.shape))
    for i in range(1, int(np.max(maps) + 1)):
        k = 2 ** i
        s_list.append(_bin_map(signal, k))
        n_list.append(np.sqrt(_bin_map(noise**2, k)) / k)
    for i in range(int(np.max(maps) + 1)):
        s = np.where(maps == i, s_list[i], s)
        n = np.where(maps == i, n_list[i], n)
    return s, n



