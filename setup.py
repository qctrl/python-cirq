
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='qctrl-cirq',
    version='0.0.4',
    description='Q-CTRL Python Cirq',
    python_requires='<3.9,>=3.7',
    project_urls={"documentation": "", "homepage": "https://q-ctrl.com", "repository": "https://github.com/qctrl/python-cirq"},
    author='Q-CTRL',
    author_email='support@q-ctrl.com',
    license='Apache-2.0',
    keywords='q-ctrl qctrl quantum control',
    classifiers=['Development Status :: 5 - Production/Stable', 'Environment :: Console', 'Intended Audience :: Developers', 'Intended Audience :: Education', 'Intended Audience :: Science/Research', 'Natural Language :: English', 'Operating System :: OS Independent', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Topic :: Internet :: WWW/HTTP', 'Topic :: Scientific/Engineering :: Physics', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Embedded Systems', 'Topic :: System :: Distributed Computing'],
    packages=['qctrlcirq'],
    package_dir={"": "."},
    package_data={},
    install_requires=['cirq==0.*,>=0.6.0', 'numpy==1.*,>=1.16.0', 'qctrl-open-controls==8.*,>=8.5.1', 'scipy==1.*,>=1.3.0', 'toml==0.*,>=0.10.0'],
    extras_require={"dev": ["nbval==0.*,>=0.9.5", "pylama", "pylint", "pylint-runner", "pytest", "qctrl-visualizer==2.*,>=2.12.1", "sphinx==2.*,>=2.2.0"]},
)
