from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'A tool for downloading audio files from Bilibili videos'

setup(
    name="AudioDownloader",
    version=VERSION,
    author="YoMi",
    author_email="2142603536@qq.com",
    description=DESCRIPTION,
    long_description=open('README.md', encoding="UTF8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'selenium',
    ],
    entry_points={
        'console_scripts': [
            'audio_downloader = AudioDownloader.audio_downloader:main'
        ]
    },
    keywords=['python', 'audio downloader', 'Bilibili'],
    license="MIT",
    url="https://github.com/your_username/your_repo",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
