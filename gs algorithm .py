#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack


#importing image
img = plt.imread('slm1.png')
img=np.mean(img,2)
plt.figure()
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

#normalization
def norm(a):
    a /= np.trapz(np.trapz(a))


img2=slm
norm(img2)
plt.imshow(img2)
plt.show()

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



ar_shape = np.shape(img2)

source_I=np.ones(ar_shape)
norm(source_I)
np.random.seed(1)
phi=np.random.rand(*ar_shape)

N=10
for _ in range(N):
    A = int_phi_to_comp(source_I, phi)
    fft_A = np.fft.fft2(A, norm='ortho')
    
    _, phi = comp_to_int_phi(fft_A)
    
    A = int_phi_to_comp(img2,phi)
    ifft_A= np.fft.ifft2(A, norm='ortho')
    
    _, phi = comp_to_int_phi(ifft_A)



plt.imshow(phi)





A = int_phi_to_comp(source_I, phi)
fft_A = np.fft.fft2(A, norm='ortho')
    
I_final, phi = comp_to_int_phi(fft_A)
plt.imshow(I_final)


np.save('gs algorithm',phi)
plt.show()




