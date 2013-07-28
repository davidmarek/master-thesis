from setuptools import setup

setup(
    name="alex.infer",
    version="0.1",
    author="David Marek",
    author_email="david@marek.me",
    description="Approximative Bayes methods for belief monitoring in spoken dialogue systems.",
    license="Apache License, Version 2.0",
    keywords="loopy belief propagation, variational inference, approximative bayesian methods", 
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
        "Operating System :: OS Independent"
        "Programming Language :: Python :: 2.7"
        "Topic :: Scientific/Engineering"
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    packages=['alex.infer'],
)
