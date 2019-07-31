
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack

#importing image
img = plt.imread('slm1.png')
plt.figure()
plt.imshow(img)

#normalization
def norm(a):
    a /= np.trapz(np.trapz(a))

img2=np.mean(img,2)
norm(img2)
plt.imshow(img2)

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

N=5
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


t = np.linspace(-10, 10, 30)
bump = np.exp(-0.05*t**2)
bump /= np.trapz(bump)

kernel = bump[:, np.newaxis] * bump[np.newaxis, :]

print(np.shape(kernel))

# Padded fourier transform, with the same shape as the image
# We use :func:`scipy.signal.fftpack.fft2` to have a 2D FFT
kernel_ft = fftpack.fft2(kernel, shape=phi.shape[:2], axes=(0, 1))


# convolve
phi_ft = fftpack.fft2(phi, axes=(0, 1))
print(np.shape(phi_ft))

print(np.shape(kernel_ft[:, :, np.newaxis]), np.shape(phi_ft))


# the 'newaxis' is to match to color direction
phi2_ft = kernel_ft * phi_ft

print(np.shape(phi2_ft))

phi2 = fftpack.ifft2(phi2_ft, axes=(0, 1)).real

# clip values to range
phi2 = np.clip(phi2, 0, 1)

from scipy import signal
# mode='same' is there to enforce the same output shape as input arrays
# (ie avoid border effects)
phi3 = signal.fftconvolve(phi, kernel, mode='same')
plt.figure()
plt.imshow(phi3)

A = int_phi_to_comp(source_I, phi)
fft_A = np.fft.fft2(A, norm='ortho')
    
I_final, phi = comp_to_int_phi(fft_A)
plt.imshow(I_final)


np.save('gs algorithm 1',phi)
plt.show()
