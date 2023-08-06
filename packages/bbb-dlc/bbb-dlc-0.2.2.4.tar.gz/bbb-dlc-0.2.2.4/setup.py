from os import path
from setuptools import setup, find_packages

# Get the version from bbb_dlc/version.py without importing the package
exec(compile(open('bbb_dlc/version.py').read(), 'bbb_dlc/version.py', 'exec'))


def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='bbb-dlc',
    version=__version__,
    description='Big Blue Button Downloader that downloads a BBB lesson as MP4 video',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    author='Heracles421',
    license='GPL-2.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bbb-dlc = bbb_dlc.main:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        'cairosvg',
        'youtube_dl',
        'Pillow',
        'pathvalidate'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)