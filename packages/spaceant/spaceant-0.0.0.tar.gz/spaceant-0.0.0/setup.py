from setuptools import setup, find_packages

setup(
  name="spaceant",
  version="0.0.0",
  description="Spacial Cell Analysis Toolkit.",
  license="BSD 3-Clause License",
  packages=find_packages(),
  author = "Matthias Bruhns",
  author_email = "matthias.bruhns@posteo.de",
  url = "https://github.com/mbruhns/spaceant",
  keywords = ["Spatial single-cell data"],
  install_requires=[
          "numpy",
          "scipy",
          "joblib",
      ],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Build Tools",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
  ])

