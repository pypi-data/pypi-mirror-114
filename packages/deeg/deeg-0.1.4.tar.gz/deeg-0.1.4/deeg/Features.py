import scipy
import numpy as np


def power_spectral_density(array, signal_frequency, window_size):
    """
    Calculate the power spectral density on EEG signal, and then extract the band power of Delta, Theta, Alpha, Beta, and Gamma band.
    We support both 1d array input and DEEG standard input (p,m,e). For the later format, we calculate PSD on dim "e" and return a (p,m) numpy array.

    input:
        array: numpy array. The temporal signal for feature extraction. 1d or with multiple dimensions
        signal_frequency: int. Original frequency of the signal
        window_size: int. Size of the window
    return
        band power: tuple or numpy array, depends on the input shape
    """
    def cal_psd(s, sf, ws):
        freqs, psd = scipy.signal.welch(s, sf, nperseg=ws)
        freq_res = freqs[1] - freqs[0]
        delta = scipy.integrate.simps(psd[np.logical_and(freqs >= 0, freqs < 4)], dx=freq_res)
        theta = scipy.integrate.simps(psd[np.logical_and(freqs >= 4, freqs <= 7)], dx=freq_res)
        alpha = scipy.integrate.simps(psd[np.logical_and(freqs >= 8, freqs <= 15)], dx=freq_res)
        beta = scipy.integrate.simps(psd[np.logical_and(freqs >= 16, freqs <= 31)], dx=freq_res)
        gamma = scipy.integrate.simps(psd[np.logical_and(freqs >= 32, freqs <= freqs[-1])], dx=freq_res)
        return delta, theta, alpha, beta, gamma
    if len(array.shape) == 1:
        return cal_psd(array, signal_frequency, window_size)
    else:
        return np.apply_along_axis(cal_psd, axis=-1, arr=array, sf=signal_frequency, ws=window_size)


def mean_absolute_deviation(array):
    """
    Calculate the mean_absolute_deviation on EEG data

    input:
        array: numpy array. The temporal signal for feature extraction. 1d or with multiple dimensions
    return
        de: int or numpy array, depends on the input shape
    """
    def cal_mad(s):
        return np.mean(np.abs(s - np.mean(s)))
    if len(array.shape) < 2:
        return cal_mad(array)
    else:
        return np.apply_along_axis(cal_mad, axis=-1, arr=array)


def skewness(array):
    """
    Calculate the feature "skewness" of the EEG signal
    We support both 1d array input and DEEG standard input (p,m,e). For the later format, we calculate SKEW on dim "e" and return a (p,m) numpy array.

    input:
        array: numpy array. The temporal signal for feature extraction. 1d or with multiple dimensions
    return
        SKEW: int or numpy array, depends on the input shape
    """
    def cal_skewness(s):
        n = len(s)
        ave1 = 0.0
        ave2 = 0.0
        ave3 = 0.0
        for x in s:
            ave1 += x
            ave2 += x ** 2
            ave3 += x ** 3
        ave1 /= n
        ave2 /= n
        ave3 /= n
        sigma = np.sqrt(ave2 - ave1 ** 2)
        return (ave3 - 3 * ave1 * sigma ** 2 - ave1 ** 3) / (sigma ** 3)
    if len(array.shape) == 1:
        return cal_skewness(array)
    else:
        return np.apply_along_axis(cal_skewness, axis=-1, arr=array)


def kurtosis(array):
    """
    Calculate the feature "kurtosis" of the EEG signal
    We support both 1d array input and DEEG standard input (p,m,e). For the later format, we calculate KURT on dim "e" and return a (p,m) numpy array.

    input:
        array: numpy array. The temporal signal for feature extraction. 1d or with multiple dimensions
    return
        KURT: int or numpy array, depends on the input shape
    """
    def cal_kurtosis(s):
        n = len(s)
        ave1 = 0.0
        ave2 = 0.0
        ave4 = 0.0
        for x in s:
            ave1 += x
            ave2 += x ** 2
            ave4 += x ** 4
        ave1 /= n
        ave2 /= n
        ave4 /= n
        sigma = np.sqrt(ave2 - ave1 ** 2)
        return ave4 / (sigma ** 4)
    if len(array.shape) == 1:
        return cal_kurtosis(array)
    else:
        return np.apply_along_axis(cal_kurtosis, axis=-1, arr=array)


def differential_entropy(array):
    """
    Calculate the feature "Differential Entropy" following the paper: "Differential Entropy Feature for EEG-based Vigilance Estimation", with hypothesis that processed signal is normal-distributed
    We support both 1d array input and DEEG standard input (p,m,e). For the later format, we calculate DE on dim "e" and return a (p,m) numpy array.
    input:
        array: numpy array. The temporal signal for feature extraction. 1d or with multiple dimensions
    return:
        de: int or numpy array, depends on the input shape
    """
    def cal_de(s):
        return (1/2)*np.log(2*np.pi*np.e*np.std(s)**2)
    if len(array.shape)<2:
        return cal_de(array)
    else:
        return np.apply_along_axis(cal_de, axis=-1, arr=array)


def rational_asymmetry(array, channel_name):
    """
    Calculate the rational asymmetry, of EEG singnal
    The differential entropy of the right brain channel is divided by that of the corresponding left brain channel

    input:
        array: numpy array. The temporal signal (>=2d) for feature extraction.
        channel_name: list or 1d array. The names of all the channels of the EEG signal
    return
        rasm: numpy array.
    """
    if len(channel_name) != array.shape[-2]:
        raise ValueError("The length of channel_name must be the same as the number of channels of the signal")
    DE = differential_entropy(array)
    def cal_rasm(de, cn):
        signal_DE = dict(zip(cn, de))
        y = []
        for key in signal_DE:
            if key == 'Fp1':
                y.append(signal_DE['Fp1'] / signal_DE['Fp2'])
            if key == 'AF7':
                y.append(signal_DE['AF7'] / signal_DE['AF8'])
            if key == 'AF3':
                y.append(signal_DE['AF3'] / signal_DE['AF4'])
            if key == 'F9':
                y.append(signal_DE['F9'] / signal_DE['F10'])
            if key == 'F7':
                y.append(signal_DE['F7'] / signal_DE['F8'])
            if key == 'F5':
                y.append(signal_DE['F5'] / signal_DE['F6'])
            if key == 'F3':
                y.append(signal_DE['F3'] / signal_DE['F4'])
            if key == 'F1':
                y.append(signal_DE['F1'] / signal_DE['F2'])
            if key == 'FT9':
                y.append(signal_DE['FT9'] / signal_DE['FT10'])
            if key == 'FT7':
                y.append(signal_DE['FT7'] / signal_DE['FT8'])
            if key == 'FC5':
                y.append(signal_DE['FC5'] / signal_DE['FC6'])
            if key == 'FC3':
                y.append(signal_DE['FC3'] / signal_DE['FC4'])
            if key == 'FC1':
                y.append(signal_DE['FC1'] / signal_DE['FC2'])
            if key == 'LPA':
                y.append(signal_DE['LPA'] / signal_DE['RPA'])
            if key == 'T7':
                y.append(signal_DE['T7'] / signal_DE['T8'])
            if key == 'C5':
                y.append(signal_DE['C5'] / signal_DE['C6'])
            if key == 'C3':
                y.append(signal_DE['C3'] / signal_DE['C4'])
            if key == 'C1':
                y.append(signal_DE['C1'] / signal_DE['C2'])
            if key == 'TP9':
                y.append(signal_DE['TP9'] / signal_DE['TP10'])
            if key == 'TP7':
                y.append(signal_DE['TP7'] / signal_DE['TP8'])
            if key == 'CP5':
                y.append(signal_DE['CP5'] / signal_DE['CP6'])
            if key == 'CP3':
                y.append(signal_DE['CP3'] / signal_DE['CP4'])
            if key == 'CP1':
                y.append(signal_DE['CP1'] / signal_DE['CP2'])
            if key == 'P9':
                y.append(signal_DE['P9'] / signal_DE['P10'])
            if key == 'P7':
                y.append(signal_DE['P7'] / signal_DE['P8'])
            if key == 'P5':
                y.append(signal_DE['P5'] / signal_DE['P6'])
            if key == 'P3':
                y.append(signal_DE['P3'] / signal_DE['P4'])
            if key == 'P1':
                y.append(signal_DE['P1'] / signal_DE['P2'])
            if key == 'PO7':
                y.append(signal_DE['PO7'] / signal_DE['PO8'])
            if key == 'PO3':
                y.append(signal_DE['PO3'] / signal_DE['PO4'])
            if key == 'O1':
                y.append(signal_DE['O1'] / signal_DE['O2'])
        return np.array(y)
    if len(DE.shape) == 1:
        return cal_rasm(DE, channel_name)
    else:
        return np.apply_along_axis(cal_rasm, axis=-1, arr=DE, cn=channel_name)


def differential_asymmetry(array, channel_name):
    """
    Calculate the differential asymmetry of EEG singnal
    The differential entropy of the right brain channel was subtracts from that of the corresponding left brain channel

    input:
        array: numpy array. The temporal signal (>=2d) for feature extraction
        channel_name: list or 1d array. The names of all the channels of the EEG signal
    return
        dasm: numpy array.
    """
    if len(channel_name) != array.shape[-2]:
        raise ValueError("The length of channel_name must be the same as the number of channels of the signal")
    DE = differential_entropy(array)
    def cal_dasm(de, cn):
        signal_DE = dict(zip(cn, de))
        y = []
        for key in signal_DE:
            if key == 'Fp1':
                y.append(signal_DE['Fp1'] - signal_DE['Fp2'])
            if key == 'AF7':
                y.append(signal_DE['AF7'] - signal_DE['AF8'])
            if key == 'AF3':
                y.append(signal_DE['AF3'] - signal_DE['AF4'])
            if key == 'F9':
                y.append(signal_DE['F9'] - signal_DE['F10'])
            if key == 'F7':
                y.append(signal_DE['F7'] - signal_DE['F8'])
            if key == 'F5':
                y.append(signal_DE['F5'] - signal_DE['F6'])
            if key == 'F3':
                y.append(signal_DE['F3'] - signal_DE['F4'])
            if key == 'F1':
                y.append(signal_DE['F1'] - signal_DE['F2'])
            if key == 'FT9':
                y.append(signal_DE['FT9'] - signal_DE['FT10'])
            if key == 'FT7':
                y.append(signal_DE['FT7'] - signal_DE['FT8'])
            if key == 'FC5':
                y.append(signal_DE['FC5'] - signal_DE['FC6'])
            if key == 'FC3':
                y.append(signal_DE['FC3'] - signal_DE['FC4'])
            if key == 'FC1':
                y.append(signal_DE['FC1'] - signal_DE['FC2'])
            if key == 'LPA':
                y.append(signal_DE['LPA'] - signal_DE['RPA'])
            if key == 'T7':
                y.append(signal_DE['T7'] - signal_DE['T8'])
            if key == 'C5':
                y.append(signal_DE['C5'] - signal_DE['C6'])
            if key == 'C3':
                y.append(signal_DE['C3'] - signal_DE['C4'])
            if key == 'C1':
                y.append(signal_DE['C1'] - signal_DE['C2'])
            if key == 'TP9':
                y.append(signal_DE['TP9'] - signal_DE['TP10'])
            if key == 'TP7':
                y.append(signal_DE['TP7'] - signal_DE['TP8'])
            if key == 'CP5':
                y.append(signal_DE['CP5'] - signal_DE['CP6'])
            if key == 'CP3':
                y.append(signal_DE['CP3'] - signal_DE['CP4'])
            if key == 'CP1':
                y.append(signal_DE['CP1'] - signal_DE['CP2'])
            if key == 'P9':
                y.append(signal_DE['P9'] - signal_DE['P10'])
            if key == 'P7':
                y.append(signal_DE['P7'] - signal_DE['P8'])
            if key == 'P5':
                y.append(signal_DE['P5'] - signal_DE['P6'])
            if key == 'P3':
                y.append(signal_DE['P3'] - signal_DE['P4'])
            if key == 'P1':
                y.append(signal_DE['P1'] - signal_DE['P2'])
            if key == 'PO7':
                y.append(signal_DE['PO7'] - signal_DE['PO8'])
            if key == 'PO3':
                y.append(signal_DE['PO3'] - signal_DE['PO4'])
            if key == 'O1':
                y.append(signal_DE['O1'] - signal_DE['O2'])
        return np.array(y)
    if len(DE.shape) == 1:
        return cal_dasm(DE, channel_name)
    else:
        return np.apply_along_axis(cal_dasm, axis=-1, arr=DE, cn=channel_name)


def differential_caudality(array, channel_name):
    """
    Calculate the differential caudality of EEG singnal
    The differential entropy of the posterior brain channel was subtracts from that of the corresponding frontal brain channel

    input:
        array: numpy array. The temporal signal (>=2d) for feature extraction.
        channel_name: list or 1d array. The names of all the channels of the EEG signal
    return
        dcau: numpy array.
    """
    if len(channel_name) != array.shape[-2]:
        raise ValueError("The length of channel_name must be the same as the number of channels of the signal")
    DE = differential_entropy(array)

    def cal_dcau(de, cn):
        signal_DE = dict(zip(cn, de))
        y = []
        for key in signal_DE:
            if key == 'Nz':
                y.append(signal_DE['Nz'] - signal_DE['Iz'])
            if key == 'Fp1':
                y.append(signal_DE['Fp1'] - signal_DE['O1'])
            if key == 'Fpz':
                y.append(signal_DE['Fpz'] - signal_DE['Oz'])
            if key == 'Fp2':
                y.append(signal_DE['Fp2'] - signal_DE['O2'])
            if key == 'AF7':
                y.append(signal_DE['AF7'] - signal_DE['PO7'])
            if key == 'AF3':
                y.append(signal_DE['AF3'] - signal_DE['PO3'])
            if key == 'AFz':
                y.append(signal_DE['AFz'] - signal_DE['POz'])
            if key == 'AF4':
                y.append(signal_DE['AF4'] - signal_DE['PO4'])
            if key == 'AF8':
                y.append(signal_DE['AF8'] - signal_DE['PO8'])
            if key == 'F9':
                y.append(signal_DE['F9'] - signal_DE['P9'])
            if key == 'F7':
                y.append(signal_DE['F7'] - signal_DE['P7'])
            if key == 'F5':
                y.append(signal_DE['F5'] - signal_DE['P5'])
            if key == 'F3':
                y.append(signal_DE['F3'] - signal_DE['P3'])
            if key == 'F1':
                y.append(signal_DE['F1'] - signal_DE['P1'])
            if key == 'Fz':
                y.append(signal_DE['Fz'] - signal_DE['Pz'])
            if key == 'F2':
                y.append(signal_DE['F2'] - signal_DE['P2'])
            if key == 'F4':
                y.append(signal_DE['F4'] - signal_DE['P4'])
            if key == 'F6':
                y.append(signal_DE['F6'] - signal_DE['P6'])
            if key == 'F8':
                y.append(signal_DE['F8'] - signal_DE['P8'])
            if key == 'F10':
                y.append(signal_DE['F10'] - signal_DE['P10'])
            if key == 'FT9':
                y.append(signal_DE['FT9'] - signal_DE['TP9'])
            if key == 'FT7':
                y.append(signal_DE['FT7'] - signal_DE['TP7'])
            if key == 'FC5':
                y.append(signal_DE['FC5'] - signal_DE['CP5'])
            if key == 'FC3':
                y.append(signal_DE['FC3'] - signal_DE['CP3'])
            if key == 'FC1':
                y.append(signal_DE['FC1'] - signal_DE['CP1'])
            if key == 'FCz':
                y.append(signal_DE['FCz'] - signal_DE['CPz'])
            if key == 'FC2':
                y.append(signal_DE['FC2'] - signal_DE['CP2'])
            if key == 'FC4':
                y.append(signal_DE['FC4'] - signal_DE['CP4'])
            if key == 'FC6':
                y.append(signal_DE['FC6'] - signal_DE['CP6'])
            if key == 'FT8':
                y.append(signal_DE['FT8'] - signal_DE['TP8'])
            if key == 'FT10':
                y.append(signal_DE['FT10'] - signal_DE['TP10'])
        return np.array(y)

    if len(DE.shape) == 1:
        return cal_dcau(DE, channel_name)
    else:
        return np.apply_along_axis(cal_dcau, axis=-1, arr=DE, cn=channel_name)

