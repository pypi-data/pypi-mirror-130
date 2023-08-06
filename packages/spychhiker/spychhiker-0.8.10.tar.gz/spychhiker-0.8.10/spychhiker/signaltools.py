#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 19:21:01 2020

@author: benjamin
"""

import numpy as np
import scipy


def symmetricifft(x, nfft=None):
    """ returns the IFFT by symmetric inverse Fourier transform """
    if len(x.shape) == 1:
        x = x.reshape(-1,1)
    xconj = np.conj(x[-2:0:-1,:])
    xconc = np.concatenate((x, xconj), 0)
    if nfft is None:
        nfft = len(xconc)
    y = np.real(np.fft.ifft(xconc, nfft, axis=0))

    return np.squeeze(y)

def lin_freq(f, F1, Fp1):
    """ returns linear relationship for piece-wise linear warping """
    f_1 = [x for x in f if x >= F1[0] and x<= F1[1]]

    return (Fp1[1] - Fp1[0]) / (F1[1] - F1[0]) * np.array(f_1 - F1[0]) + Fp1[0]

def dfw(x, f_input, form_input, form_output):
    """ frequency warping of cepstral envelope such that peaks match target formants """
    in_form = form_input
    in_form = np.insert(in_form, 0, 0)
    in_form = np.append(in_form, f_input[-1])

    out_form = np.insert(form_output, 0, 0)
    out_form = np.append(out_form, f_input[-1])

    for k in range(5):
        fTmp = lin_freq(f_input, in_form[k:k+2], out_form[k:k+2])
        if k == 0:
            f_output = fTmp
        else:
            f_output = np.vstack((f_output.reshape(-1,1), fTmp.reshape(-1,1)))

    f_output = f_output[:len(f_input)]

    f1 = scipy.interpolate.interp1d(f_input, x, kind='quadratic', fill_value='extrapolate')
    return f1(f_output.squeeze())

def ceps_transform(Sxx, transOper, nwin, novlp, fxx, freq_out):
    """ cepstral transformation """
    nord = transOper.shape[0]
    nfft = nwin
    L = int(nfft / 2 + 1)

    if freq_out is None:
        ceps_coeff = symmetricifft(20 * np.log10(np.abs(Sxx)), nfft)[:nord, :]
        ceps_coeff = scipy.stats.zscore(ceps_coeff)
        cepsT = transOper @ ceps_coeff
        cepsT2 = scipy.stats.zscore(cepsT)
        Sxx_trans = 10**(np.real(np.fft.fft(cepsT2, nfft, axis=0))[:L, :] / 20)
        Sxx_in = 10**(np.real(np.fft.fft(ceps_coeff, nfft, axis=0))[:L, :] / 20)
        del ceps_coeff, cepsT, cepsT2
    else:
        isChange = False
        if len(freq_out) != len(fxx):
            a = TimeFreq('time_frequency_matrix', Sxx_in,
                         'frequency_vector', fxx)
            a.interpolate(freq_out, axis='freq')
            Sxx_in = a.time_frequency_matrix
            isChange = True
        elif not (freq_out==fxx).all():
            a = TimeFreq('time_frequency_matrix', Sxx_in,
                         'frequency_vector', fxx)
            a.interpolate(freq_out, axis='freq')
            Sxx_in = a.time_frequency_matrix
            isChange = True
        Sxx_in = scipy.stats.zscore(Sxx_in)
        Sxx_trans = transOper @ Sxx_in
        Sxx_trans = scipy.stats.zscore(Sxx_trans)
        if isChange:
            a = FreqSig('time_frequency_matrix', Sxx_trans,
                        'frequency_vector', freq_out)
            a.interpolate(fxx, axis='freq')
            Sxx_trans = a.time_frequency_matrix
            a = FreqSig('time_frequency_matrix', Sxx_in,
                        'frequency_vector', freq_out)
            a.interpolate(fxx, axis='freq')
            Sxx_in = a.time_frequency_matrix

    return Sxx_in, Sxx_trans

def get_order_ceps(f0, sr):
    """ returns the optimal cepstral order based on pitch estimation """

    if np.nanmedian(f0) < 0:
        f0 = 125
    else:
        f0 = np.nanmedian(f0)

    if f0 <= 0:
        f0 = 125
    CepOrder = 2 * np.round(sr / f0)

    if np.floor(CepOrder / 2) == CepOrder / 2:
        CepOrder -= 1

    return int(CepOrder)

def cepstral_filtering(logx, nwin, order=None):
    """ cepstral liftering """
    xRealCep = np.real(np.fft.ifft(logx))
    wzp = np.zeros_like(xRealCep)

    CepOrder = int(order)
    midOrdp1 = int((CepOrder+1)/2-1)
    midOrdm1 = int((CepOrder-1)/2)

    winCeps = scipy.signal.hann(CepOrder)
    # winCeps = np.ones(CepOrder)
    wzp = np.concatenate((winCeps[midOrdp1:CepOrder],
                          np.zeros(nwin - CepOrder),
                          winCeps[:midOrdm1]))

    liftCeps = wzp * xRealCep
    xEnv = np.real(np.fft.fft(liftCeps, nwin, axis=0))

    return xEnv

def true_envelope(x, sr, toldB=2, order=None):
    """ returns the true envelope of x """
    nwin = len(x)
    Ao = np.log(abs(np.fft.fft(x)))
    Vo = -np.inf * np.ones_like(Ao)
    while any(20*np.log10(np.exp(Ao)/np.exp(Vo)) > toldB):
        Ao = np.maximum(Ao, Vo)
        Vo = cepstral_filtering(Ao, nwin, order)

    return Vo

def esprit(x, sr = 1, K = 12):
    """ estimate the frequency of the damped sinusoids that model x """
    
    idx = np.argmax(x)
    x = x[idx:]
    x = x - np.mean(x)
    
    M = int(min(100, np.floor(len(x) / 2)))
    Nl = len(x) - M + 1
    Nt = int(Nl / M)
    
    R = np.zeros((M,M))
    for k in range(Nt):
        deb = int(k * M)
        fin = int(deb + 2 * M - 1)
        xtmp = x[deb:fin]
    
        H = scipy.linalg.hankel(xtmp[0:M], xtmp[M - 1:])
        R += H.dot(H.T)
        
    u, s, d = np.linalg.svd(R)
    nx, ny = u.shape
    
    Up = u[1:,:K]
    Um = u[:-1,:K]
    Phi = np.linalg.pinv(Um).dot(Up)
    z,w = np.linalg.eig(Phi)
    freq = np.angle(z) / 2 / np.pi * sr
    
    return np.sort(freq[freq > 50])
