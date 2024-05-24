import numpy as np
from scipy.signal import butter, spectrogram
import matplotlib.pyplot as plt
from hilbert_envelope import *
from homomorphic_envelope import *
from wavelet_envelope import  *
from preprocessing import schmidt_spike_removal, normalize, \
    high_pass_filter, downsample, low_pass_filter



NFFT = 256

def get_psd_feature(data, sampling_frequency, frequency_limit_low, frequency_limit_high):
    f, t, sxx = spectrogram(x=data, window=[sampling_frequency / 40],
                            noverlap=round(sampling_frequency / 80),
                            fs=sampling_frequency, mode='complex', scaling='density')

    low_lim = min(abs(f - frequency_limit_low))
    high_lim = min(abs(f - frequency_limit_high))

    return np.mean(sxx[low_lim:high_lim, :])

def get_pcg_features(audio_data, features_fs, audio_fs, wavelet=False):
    audio_data = low_pass_filter(audio_data, 2, 400, audio_fs)
    audio_data = high_pass_filter(audio_data, 2, 25, audio_fs)
    # audio_data = schmidt_spike_removal(audio_data, audio_fs)

    hilbert_env = hilbert_envelope(audio_data, audio_fs)
    normalized_hilbert = downsample(hilbert_env, features_fs, audio_fs)
    normalized_hilbert = normalize(normalized_hilbert)

    homomorphic_env = homomorphic_envelope(hilbert_env, audio_fs)
    normalized_homomorphic = downsample(homomorphic_env, features_fs, audio_fs)
    normalized_homomorphic = normalize(normalized_homomorphic)
    '''
    psd = get_psd_feature(audio_data, features_fs, 40, 60)
    psd = downsample(psd, len(normalized_homomorphic), len(psd))
    psd = normalize(psd)
    '''
    num_of_dims = 2 # change to 3 to include psd
    if wavelet:
        num_of_dims = 3 # change to 4 to include psd
    pcg_features = np.zeros((len(normalized_homomorphic), num_of_dims))
    pcg_features[:, 0] = normalized_homomorphic
    pcg_features[:, 1] = normalized_hilbert
    # pcg_features[:, 2] = psd

    if wavelet:
        wavelet = wavelet_envelope(audio_data, audio_fs)
        wavelet = wavelet[1:len(normalized_homomorphic)]
        normalized_wavelet = downsample(wavelet, features_fs, audio_fs)
        normalized_wavelet = normalize(normalized_wavelet)
        pcg_features[:, 3] = normalized_wavelet

    return {
        'pcg_features': pcg_features,
        'fs': features_fs
    }
