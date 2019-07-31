#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
from scipy import signal
from scipy import interpolate

#normalization
def norm(a):
    a /= np.trapz(np.trapz(a))


#calculating amplitude using Intensity and phi. 
def int_phi_to_comp(I,phi):
    A=np.sqrt(I)*np.exp(1j*phi)
    return A

#calculating Intensity and phi from amplitude. 
def comp_to_int_phi(A):
    I=np.abs(A)**2
    x1=np.imag(A)
    x2=np.real(A)
    phi=np.arctan2(x1,x2)
    
    assert (phi==np.angle(A)).all(), "Value of phi is incorrect"
    
    return I, phi


def blur_image(phi):

    t = np.linspace(-10, 10, 5)
    bump = np.exp(-20*t**2)
    bump /= np.trapz(bump)
    kernel = bump[:, np.newaxis] * bump[np.newaxis, :]
##    kernel_ft = fftpack.fft2(kernel, shape=phi.shape[:2], axes=(0, 1))
##    phi_ft = fftpack.fft2(phi, axes=(0, 1))
##    phi2_ft = kernel_ft * phi_ft
##    phi2 = fftpack.ifft2(phi2_ft, axes=(0, 1)).real
##    phi2 = np.clip(phi2, 0, 1)
    phi3 = signal.fftconvolve(phi, kernel, mode='same')
    
    return phi3


def get_error(A, B):
    C = np.abs(A-B)
    C = np.mean(C)
    return C

def gs_alg(target_intensity, iterations):
    ar_shape = np.shape(target_intensity)

    source_I=np.ones(ar_shape)
    norm(source_I)
    np.random.seed(1)
    phi=np.random.rand(*ar_shape)


    for _ in range(iterations):
        A = int_phi_to_comp(source_I, phi)
        fft_A = np.fft.fft2(A, norm='ortho')
        
        I_final, phi = comp_to_int_phi(fft_A)

        print get_error(I_final, img2)
        
        
        A = int_phi_to_comp(img2,phi)
        ifft_A= np.fft.ifft2(A, norm='ortho')
        
        _, phi = comp_to_int_phi(ifft_A)

        phi = blur_image(phi)

      


    A = int_phi_to_comp(source_I, phi)
    fft_A = np.fft.fft2(A, norm='ortho')
    I_final, _ = comp_to_int_phi(fft_A)

    return phi, I_final

def scale_image(img, scaling_factor):
    image_width, image_height = np.shape(img)

    

def load_image(filename):
    
    #importing image
    img = plt.imread(filename)
    img=np.mean(img,2)
    #plt.figure()
    plt.imshow(img)
    plt.show()

    height=1920
    width=1080

    slm=np.zeros((width,height))

    #image_height=np.shape(img)[1]
    #image_width=np.shape(img)[0]
    image_width, image_height = np.shape(img)

    ix=int(width/2-image_width/2)
    iy=int(height/2-image_height/2)

    slm[ix:ix+image_width, iy:iy+image_height]=img

    img2=slm
    norm(img2)
    plt.imshow(img2)
    plt.show()

    return img2


if __name__ == '__main__':

    #img2 = load_image('slm1.png')
    img2 = load_image('ball.png')
    phi, I_final = gs_alg(target_intensity=img2, iterations=10)
    
    plt.imshow(phi)
    plt.show()
    
    plt.imshow(np.log(I_final))
    plt.show()


    np.save('gs algorithm 2',phi)





