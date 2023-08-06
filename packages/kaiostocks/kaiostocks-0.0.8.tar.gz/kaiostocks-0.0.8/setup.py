from setuptools import setup, find_packages


__project__ = "kaiostocks"
__version__ = "0.0.8"
__description__ = "this library treats stocks data"
__requires__ = ["pandas", "ta", "numpy"]
__author__ = "Kaio"
__author_email__ = "akaio@crimson.ua.edu"

setup(
    name = __project__,
    version = __version__,
    url = "https://github.com/kaiomarques93/kaiostocks",
    description = __description__,
    packages = ['kaiostocks'],
    #packages=find_packages(where="./kaiostocks"),
    #package_dir= {'', 'kaiostocks'},
    author = __author__,
    author_email = __author_email__,
    install_requires = __requires__,
)