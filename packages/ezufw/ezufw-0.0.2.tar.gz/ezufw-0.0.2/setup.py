from setuptools import setup, find_packages
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))
with open(path.join(BASE_DIR, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


VERSION = '0.0.2'
DESCRIPTION = 'Another Eazy UFW wrapper'

setup(
    name="ezufw",
    version=VERSION,
    author="Kyther (Mark Adam Gancarz)",
    author_email="<mrk.gancarz@gmail.com>",
    description=DESCRIPTION, 
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'firewall', 'ufw', 'network', 'inet', 'ipv4', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix"
    ]
)

