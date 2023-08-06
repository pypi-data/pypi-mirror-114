from pyrogen.src import pyrogen
import setuptools


setuptools.setup(version=pyrogen.__version__,
                 include_package_data=True,
                 install_requires=[
                     "pyglet==1.5.17",
                     "pillow==8.1.2",
                     "moderngl==5.6.4",
                     "moderngl-window==2.3.0", ]
                 )
