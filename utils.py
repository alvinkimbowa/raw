""" 

This script will load and display Clarius supported file types.

Adopted from Clarius raw repository by Reza Zahiri.
Available at https://github.com/clariusdev/raw/blob/master/common/python/rdataread.py

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# read rf data
def read_rf(filename):
    hdr_info = ('id', 'frames', 'lines', 'samples', 'samplesize')
    hdr, timestamps, data = {}, None, None
    with open(filename, 'rb') as raw_bytes:
        # Read the header
        # Note: Each item in the header is uint32 format (4 bytes) 
        for info in hdr_info:
            hdr[info] = int.from_bytes(raw_bytes.read(4), byteorder='little')
        # set data type
        if hdr['samplesize'] == 1:
            dtype = 'uint8'
        elif hdr['samplesize'] == 2:
            dtype = 'int16'
        elif hdr['samplesize'] == 4:
            dtype = 'int32'
        else:
            raise ValueError(f'Unsupported sample size: {hdr["samplesize"]}. Supported sizes are 1 and 2.')
        # read timestamps and data
        timestamps = np.zeros(hdr['frames'], dtype='int64') # Timestamps are uint64 (8 bytes)
        sz = hdr['lines'] * hdr['samples'] * hdr['samplesize']  # Total size of each frame (in bytes)
        data = np.zeros((hdr['lines'], hdr['samples'], hdr['frames']), dtype=dtype) # WxHxB
        for frame in range(hdr['frames']):
            # read timestamp
            timestamps[frame] = int.from_bytes(raw_bytes.read(8), byteorder='little')
            # read each frame
            data[:, :, frame] = np.frombuffer(raw_bytes.read(sz), dtype=dtype).reshape(data.shape[:2])
    print('Loaded {d[2]} raw frames of size, {d[0]} x {d[1]} (lines x samples)'.format(d=data.shape))
    return hdr, timestamps, data

# read iq data
def read_iq(filename):
    hdr_info = ('id', 'frames', 'lines', 'samples', 'samplesize')
    hdr, timestamps, data = {}, None, None
    with open(filename, 'rb') as raw_bytes:
        # read 4 bytes header 
        for info in hdr_info:
            hdr[info] = int.from_bytes(raw_bytes.read(4), byteorder='little')
        # read timestamps and data
        timestamps = np.zeros(hdr['frames'], dtype='int64')
        sz = hdr['lines'] * hdr['samples'] * hdr['samplesize']
        data = np.zeros((hdr['lines'], hdr['samples'] * 2, hdr['frames']), dtype='int16')
        for frame in range(hdr['frames']):
            # read 8 bytes of timestamp
            timestamps[frame] = int.from_bytes(raw_bytes.read(8), byteorder='little')
            # read each frame
            data[:, :, frame] = np.frombuffer(raw_bytes.read(sz), dtype='int16').reshape([hdr['lines'], hdr['samples']*2])
    print('Loaded {d[2]} raw frames of size, {d[0]} x {d[1]} (lines x samples)'.format(d=data.shape))
    return hdr, timestamps, data

def plot_image(img, line=50, title=None, cmap='gray', cbar=False, vmin=None, vmax=None):
    plt.figure(figsize=(4,3.5))
    plt.imshow(img, cmap, aspect='auto', vmin=vmin, vmax=vmax)
    if line:
        plt.vlines(line, 0, img.shape[0], color='b')
    plt.title(title)
    if cbar:
        plt.colorbar()
    plt.show()


"""Adopted from ultraspy python package by Pierre Ecarlat.
    Available at https://gitlab.com/pecarlat/ultraspy/-/blob/main/src/ultraspy/gpu/display.py
"""
def get_doppler_colormap(use='matplotlib'):
    """Returns a color map proposition for Doppler, based on typical
    echographs, from blue (flow going away from the probe), to red (going
    toward to).

    :param str use: The lib which will use the colormap, either 'matplotlib' or
        'pyqt'

    :returns: The matplotlib map with the RGB value of our color maps
    :return type: matplotlib.colors.ListedMaps
    """
    x = np.linspace(0, 1, 256)
    reds = np.clip(np.sqrt(np.clip(x - 0.5, 0, 1)) * 1.8, 0, 1)
    greens = np.power(x - 0.5, 4) * -8 + np.power(x - 0.5, 2) * 6
    blues = 1.1 * np.sqrt(0.5 - np.clip(x, 0, 0.5))

    if use == 'matplotlib':
        rgb = np.stack((reds, greens, blues, np.ones(256))).T
        return ListedColormap(rgb)
    elif use == 'pyqt':
        rgb = np.stack((reds, greens, blues)).T * 255
        return rgb
    else:
        raise AttributeError(
            f"Unknown library {use}, should pick matplotlib or pyqt.")

