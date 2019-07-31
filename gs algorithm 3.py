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


def fft2(A):
    return np.fft.fftshift(np.fft.fft2(A, norm='ortho'))

def ifft2(A):
    return np.fft.ifft2(np.fft.ifftshift(A), norm='ortho')

    
def gs_alg(target_intensity, iterations):
    ar_shape = np.shape(target_intensity)

    source_shape = (1080, 1920)

    source_I=np.ones(source_shape)
    source_I=pad_square(source_I)
    
    norm(source_I)
    np.random.seed(1)
    phi=np.random.rand(*ar_shape)


    for _ in range(iterations):
        A = int_phi_to_comp(source_I, phi)
        fft_A = fft2(A)
        
        I_final, phi = comp_to_int_phi(fft_A)

        print get_error(I_final, img2)
        
        
        A = int_phi_to_comp(img2,phi)
        ifft_A= ifft2(A)
        
        _, phi = comp_to_int_phi(ifft_A)

        #phi = blur_image(phi)

      


    A = int_phi_to_comp(source_I, phi)
    fft_A = fft2(A)
    I_final, _ = comp_to_int_phi(fft_A)

    phi=center_slice(phi,source_shape)

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
    #width=1080
    width = 1920

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

def pad_square(A):

    A_width=np.shape(A)[0]
    A_height=np.shape(A)[1]

    l = max([A_width, A_height])
    slm=np.zeros((l,l))

    ix=int(l/2-A_width/2)
    iy=int(l/2-A_height/2)

    slm[ix:ix+A_width, iy:iy+A_height]=A

    return slm

def center_slice(A, shape):

    assert np.shape(A)[0] == np.shape(A)[1], "A is not a square"

    l=np.shape(A)[0]
    ix=int(l/2-shape[0]/2)
    iy=int(l/2-shape[1]/2)

    return A[ix:ix+shape[0], iy:iy+shape[1]]
    
def center_slice_testbench():
    a = np.array([[1,2,6],[3,4,5]])
    print a

    print pad_square(a)

    print center_slice(pad_square(a),np.shape(a))
    
    

if __name__ == '__main__':


    #center_slice_testbench()

    
    img2 = load_image('box.png')
    #img2 = load_image('ball.png')
    phi, I_final = gs_alg(target_intensity=img2, iterations=10)
    
    plt.imshow(phi)
    plt.show()
    
    plt.imshow(I_final)
    plt.show()


    np.save('gs algorithm 2',phi)



