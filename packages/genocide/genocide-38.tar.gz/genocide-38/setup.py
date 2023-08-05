# This file is placed in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='38',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="http://genocide.rtfd.io - otp.informationdesk@icc-cpi.int - OTP-CR-117/19",
    long_description=read(),
    install_requires=["feedparser"],
    license='Public Domain',
    py_modules=["ob", 'trm'],
    packages=["bot", "genocide"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
        (
            "share/genocide/",
            [
                "files/genocide.1.md",
                "files/genocidectl.8.md",
                "files/genocided.8.md",
                "files/genocide.service",
                "files/genocide",
            ],
        ),
    ],
    scripts=["bin/genocide", "bin/genocided", "bin/genocidecmd", "bin/genocidectl"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
 