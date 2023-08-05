from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Another Eazy UFW wrapper'

setup(
    name="ezufw",
    version=VERSION,
    author="Kyther (Mark Adam Gancarz)",
    author_email="<mrk.gancarz@gmail.com>",
    description=DESCRIPTION, 
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

