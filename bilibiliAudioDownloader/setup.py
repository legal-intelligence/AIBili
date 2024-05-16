from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'A tool for downloading audio files from Bilibili videos'

setup(
    name="bilibiliAudioDownloader",
    version=VERSION,
    author="YoMi__token__.21",
    author_email="wanglong67890@outlook.com",
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
            'audio_downloader = bilibiliAudioDownloader.BilibiliAudioDownloader.audio_downloader:main'
        ]
    },
    keywords=['python', 'audio downloader', 'Bilibili'],
    license="MIT",
    url="https://github.com/legal-intelligence/legal-intelligence/tree/Legal_Video/BilibiliAudioDownloader",
    scripts=['BilibiliAudioDownloader/up_uid_search.py', 'BilibiliAudioDownloader/bvid_search.py', 'BilibiliAudioDownloader/audio_downloader.py'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
