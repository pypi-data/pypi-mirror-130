# PyNUFFT: Python non-uniform fast Fourier transform
![](g5738.jpeg)

A minimal "getting start" tutorial is available at http://jyhmiinlin.github.io/pynufft/ . This package reimplements the min-max interpolator (Fessler, Jeffrey A., and Bradley P. Sutton. "Nonuniform fast Fourier transforms using min-max interpolation." IEEE transactions on signal processing 51.2 (2003): 560-574.) for Python.

Please cite Lin, Jyh-Miin. "Python non-uniform fast Fourier transform (PyNUFFT): An accelerated non-Cartesian MRI package on a heterogeneous platform (CPU/GPU)." Journal of Imaging 4.3 (2018): 51.

and or

Jyh-Miin Lin and Hsiao-Wen. Chung, Pynufft: python non-uniform fast Fourier transform for MRI Building Bridges in Medical Sciences 2017, St John’s College, CB2 1TP Cambridge, UK. 

### Latest message from ESMRMB

"Dear Friends and Colleagues,


We are writing to spread the word about "MRI Together", the first global workshop on open science and reproducibility in MRI sponsored by the European Society for Magnetic Resonance in Medicine and Biology (www.esmrmb.org) and taking place December 13-16, 2021.

Topics ranging from the statistical tools for reproducible research, to data sharing policies, artificial intelligence and preclinical research will be covered.

The event will span four time zones to enable global attendance.

Registration is free to both ESMRMB members and non-members, with the option of paying a fee by registering as a supporting attendee.

For more information, please visit https://mritogether.github.io/



We would also be grateful if you could spread the word to your friends/colleagues who may be interested.

If you have any questions, please feel free to contact us.

Kind regards,

Workshop organizing committee

https://www.esmrmb.org/events/mri-together-a-global-workshop-on-open-science-and-reproducibility/

"

### SciPy Japan 2020 talk

An introduction to PyNUFFT is available 

https://www.youtube.com/watch?v=smvZS5fPW8g&t=1s

### ATAT 2021 at Taiwan

https://sites.google.com/site/atathpsc/

### Recent NUFFT functions available in Python

You can also find other very useful Python nufft/nfft functions at: 

1. SigPy (Ong, F., and M. Lustig. "SigPy: a python package for high performance iterative reconstruction." Proceedings of the ISMRM 27th Annual Meeting, Montreal, Quebec, Canada. Vol. 4819. 2019. Note the order starts from the last axis), https://sigpy.readthedocs.io/en/latest/generated/sigpy.nufft.html?highlight=nufft
2. gpuNUFFT: (Knoll, Florian, et al. "gpuNUFFT-an open source GPU library for 3D regridding with direct Matlab interface." Proceedings of the 22nd annual meeting of ISMRM, Milan, Italy. 2014.): https://github.com/andyschwarzl/gpuNUFFT/tree/master/python
3. mrrt.nufft (mrrt.mri demos for the ISMRM 2020 Data Sampling Workshop in Sedona, AZ with raw cuda kernels): https://github.com/mritools/mrrt.nufft
4. pyNFFT (Keiner, J., Kunis, S., and Potts, D. ''Using NFFT 3 - a software library for various nonequispaced fast Fourier transforms'' ACM Trans. Math. Software,36, Article 19, 1-30, 2009. The python wrapper of NFFT): https://pythonhosted.org/pyNFFT/tutorial.html
5. python-NUFFT: Please see: https://github.com/dfm/python-nufft, "Python bindings by Dan Foreman-Mackey, Thomas Arildsen, and Marc T. Henry de Frahan but the code that actually does the work is from the Greengard lab at NYU (see the website). " 
6. finufft (Barnett, Alexander H., Jeremy Magland, and Ludvig af Klinteberg. "A Parallel Nonuniform Fast Fourier Transform Library Based on an “Exponential of Semicircle" Kernel." SIAM Journal on Scientific Computing 41.5 (2019): C479-C504., exponential semicircle kernel): https://finufft.readthedocs.io/en/latest/python.html. Recently providing a new cuda implementation with the python wrapper. 
7. torchkbnufft (M. J. Muckley, R. Stern, T. Murrell, F. Knoll, TorchKbNufft: A High-Level, Hardware-Agnostic Non-Uniform Fast Fourier Transform, 2020 ISMRM Workshop on Data Sampling and Image Reconstruction): https://github.com/mmuckley/torchkbnufft
8. tfkbnufft (adapt torchkbnufft for TensorFlow): https://github.com/zaccharieramzi/tfkbnufft
9. TFNUFFT (adapt the min-max interpolator in PyNUFFT for tensorflow): https://github.com/yf0726/TFNUFFT

## Installation

$ pip3 install pynufft --user


### Using Numpy/Scipy

```
$ python
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import NUFFT
>>> import numpy
>>> A = NUFFT()
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A.forward(x)
```

### Using PyCUDA

```
>>> from pynufft import NUFFT, helper
>>> import numpy
>>> A2= NUFFT(helper.device_list()[0])
>>> A2.device
<reikna.cluda.cuda.Device object at 0x7f9ad99923b0>
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> Kd = (128,128)
>>> Jd = (6,6)
>>> A2.plan(om, Nd, Kd, Jd)
0
>>> x=numpy.random.randn(*Nd)
>>> y = A2.forward(x)
```

### Using NUDFT (double precision)

Some users ask for double precision. 
NUDFT is offered.

```
>>> from pynufft import  NUDFT
>>> import numpy
>>> x=numpy.random.randn(*Nd)
>>> om = numpy.random.randn(10,2)
>>> Nd = (64,64)
>>> A = NUDFT()
>>> A.plan(om, Nd)
>>> y_cpu = A.forward(x)

```


## Testing GPU acceleration

```
Python 3.6.11 (default, Aug 23 2020, 18:05:39) 
[GCC 7.5.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pynufft import tests
>>> tests.test_init(0)
device name =  <reikna.cluda.cuda.Device object at 0x7f41d4098688>
0.06576069355010987
0.006289639472961426
error gx2= 2.0638987e-07
error gy= 1.0912560261408778e-07
acceleration= 10.455399523742015
17.97926664352417 2.710083246231079
acceleration in solver= 6.634211944790991
```
### Comparisons

![](comparison.png)

The comparison may not imply the clinical quality of third-party packages.

### Contact information
If you have professional requests related to the project, please contact
email: pynufft@gamil.com

