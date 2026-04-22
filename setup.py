import sys
import setuptools

import pywalfox.config

LONG_DESC=open('README.md').read()
VERSION=pywalfox.config.DAEMON_VERSION
DOWNLOAD = "https://github.com/Frewacom/pywalfox-native/archive/v%s.tar.gz" % VERSION

setuptools.setup(
    name="pywalfox",
    version=VERSION,
    author="Fredrik Engstrand",
    author_email="fredrik@engstrand.nu",
    description="Native app used alongside the Pywalfox browser extension",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="dynamic browser-theme firefox chrome duckduckgo unixporn native-messaging-host pywal colorscheme",
    license="MPL-2.0",
    url="https://github.com/frewacom/pywalfox",
    download_url=DOWNLOAD,
    classifiers=[
        "Topic :: Utilities",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_namespace_packages(include=["pywalfox", "pywalfox.*"]),
    entry_points={"console_scripts": ["pywalfox=pywalfox.__main__:main"]},
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False)
