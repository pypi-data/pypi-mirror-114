"""Setup."""
import time

import setuptools

DIST_NAME = 'utils'
long_description = ''
with open('README.md') as fin:
    long_description = fin.read()

IS_RELEASE = True
MAJOR, MINOR, PATCH = 1, 0, 24

if IS_RELEASE:
    version = '%d.%d.%d' % (MAJOR, MINOR, PATCH)
else:
    ts = time.strftime('%Y%m%d%H%M%S0000', time.localtime())
    version = '%d.%d.%d.%s' % (MAJOR, MINOR, PATCH, ts)

setuptools.setup(
    name="%s-nuuuwan" % DIST_NAME,
    version=version,
    author="Nuwan I. Senaratna",
    author_email="nuuuwan@gmail.com",
    description="Simple extensions to the core python libraries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuuuwan/%s" % DIST_NAME,
    project_urls={
        "Bug Tracker": "https://github.com/nuuuwan/%s/issues" % DIST_NAME,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'area',
        'bs4',
        'psutil',
        'requests',
        'selenium',
        'tweepy',
        'pandas',
        'shapely',
        'geopandas',
        'pillow',
        'matplotlib',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
