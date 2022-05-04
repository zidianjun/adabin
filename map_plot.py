
from adabin import multi_order_bin, reconstruct_maps

import numpy as np
import matplotlib.pyplot as plt

def _display_map(ax, signal, noise,
                log=True, vrange=(-3, 0), min_SN=3,
                cmap=plt.cm.RdYlBu_r, fontsize=20):
    img = np.flipud(np.where(signal / noise > min_SN, signal, np.nan))
    h, w = signal.shape
    
    if log:
        img = np.log10(img)

    if min_SN < 0.:
        im = ax.imshow(img, cmap=plt.cm.get_cmap('RdYlBu', int(np.ptp(img))))
    else:
        print("[display_map]: %d pixels with S/N > %d.\n" %(
              np.sum(signal / noise > min_SN), min_SN))
        im = ax.imshow(img, cmap=cmap, vmin=vrange[0], vmax=vrange[1])
    
    return im

def recon_plot(signal_map, noise_map, eline='SII6731', vrange=(-3, 0), fontsize=20):

    ticks = range(vrange[0], vrange[1] + 1)
    ticklabels = []
    for tick in ticks:
        ticklabels.append('10$^{%d}$' %(tick))

    signal = np.where(signal_map > 0., signal_map, 0.)
    noise = np.where(noise_map > 0., noise_map, np.mean(noise_map))

    rec_s, rec_n, maps = multi_order_bin(signal, noise)

    fig = plt.figure(figsize=(24, 9))
    plt.subplots_adjust(left=.04, bottom=.08, right=.98, top=.8, wspace=.15)

    ax = plt.subplot(131)
    im = _display_map(ax, signal, noise, vrange=vrange)
    cbar_ax = fig.add_axes([0.04, 0.92, 0.28, 0.05])
    cbar = plt.colorbar(im, orientation="horizontal", cax=cbar_ax, ticks=ticks)
    cbar.ax.set_xticklabels(ticklabels)
    cbar.set_label('Line flux ($10^{-16}$ erg)', size=20)
    cbar.ax.tick_params(labelsize=20)
    ax.set_xlabel('x (arcsec)', fontsize=fontsize)
    ax.set_ylabel('y (arcsec)', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=fontsize)

    ax = plt.subplot(132)
    im = _display_map(ax, maps, 1., min_SN=-1., log=False, cmap=plt.cm.RdYlBu)
    cbar_ax = fig.add_axes([0.368, 0.92, 0.28, 0.05])
    maximum = int(np.max(maps))
    cbar = plt.colorbar(im, orientation="horizontal", ticks=np.arange(maximum)+.5, cax=cbar_ax)
    cbar.ax.set_xticklabels(2**np.arange(maximum))
    cbar.set_label('Map number', size=20)
    cbar.ax.tick_params(labelsize=20)
    ax.set_xlabel('x (arcsec)', fontsize=fontsize)
    ax.set_ylabel('y (arcsec)', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=fontsize)

    ax = plt.subplot(133)
    im = _display_map(ax, rec_s, rec_n, vrange=vrange)
    cbar_ax = fig.add_axes([0.695, 0.92, 0.28, 0.05])
    cbar = plt.colorbar(im, orientation="horizontal", cax=cbar_ax, ticks=ticks)
    cbar.ax.set_xticklabels(ticklabels)
    cbar.set_label('Line flux ($10^{-16}$ erg)', size=20)
    cbar.ax.tick_params(labelsize=20)
    ax.set_xlabel('x (arcsec)', fontsize=fontsize)
    ax.set_ylabel('y (arcsec)', fontsize=fontsize)
    ax.tick_params(axis='both', labelsize=fontsize)

    plt.show()


