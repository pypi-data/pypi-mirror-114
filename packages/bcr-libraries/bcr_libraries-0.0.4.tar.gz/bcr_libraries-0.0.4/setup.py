from setuptools import setup

__project__ = "bcr_libraries"
__version__ = "0.0.4"
__description__ = "MCP3008 Library for BC Robotics 16 Channel Analog Input HATs"
__packages__ = ["bcr_mcp3008"]
__author__ = "Chris Caswell"
__author_email__ = "support@bc-robotics.com"
__classifiers__ = [ 
    "Programming Language :: Python :: 3",
]
__requires__ = ["spidev"]


setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    requires = __requires__,
)
