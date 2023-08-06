"""Setup script for detection tools"""

from setuptools import find_packages
from setuptools import setup


REQUIRED_PACKAGES = ['Pillow>=1.0', 'Matplotlib>=2.1', 'Cython>=0.28.1', 'tf-slim>=1.1.0']

setup(
    name='detection_tools',
    version='0.3',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=[p for p in find_packages() if
    p.startswith('detection_tools')],
    description='Tensorflow Object Detection Tools Library',
)
