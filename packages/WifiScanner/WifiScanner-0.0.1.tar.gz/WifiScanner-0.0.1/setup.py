from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Search WIFIs Around Your Device'
# Setting up
setup(
    name="WifiScanner",
    version=VERSION,
    url='https://github.com/HaniePoursina/Search-Wifis',
    author="Hanie Poursina, Mehdi Hosseini Moghadam, ",
    author_email="<hanieh.poursina@gmail.com>, <m.h.moghadam1996@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pycairo', 'PyGObject'],
    keywords=['python', 'Wifis', 'Scan WIFIs', 'Network Manager', 'drivers', 'iot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)