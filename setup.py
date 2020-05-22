import sys
import setuptools

import pywalfox.config

LONG_DESC=open('README.md').read()
VERSION=pywalfox.config.DAEMON_VERSION
DOWNLOAD = "https://github.com/Frewacom/pywalfox-native/archive/%s.tar.gz" % VERSION

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
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
    packages=["pywalfox"],
    entry_points={"console_scripts": ["pywalfox=pywalfox.__main__:main"]},
    python_requires=">=2.7",
    include_package_data=True,
    zip_safe=False)
