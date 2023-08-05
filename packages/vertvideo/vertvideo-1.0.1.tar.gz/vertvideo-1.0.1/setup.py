from setuptools import setup

setup(
    name='vertvideo',
    version="1.0.1",
    description='python package to help you convert video/audio files.',
    url='https://github.com/ellipyhub/vertvideo',
    author='Ellipyhub',
    license='MIT License',
    packages=['vertvideo'],
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    keywords='audio video file convert',
    install_requires=[
        'autopep8==1.5.7',
        'certifi==2021.5.30',
        'charset-normalizer==2.0.3',
        'decorator==4.4.2',
        'idna==3.2',
        'imageio==2.9.0',
        'imageio-ffmpeg==0.4.4',
        'moviepy==1.0.3',
        'numpy==1.21.1',
        'Pillow==8.3.1',
        'proglog==0.1.9',
        'pycodestyle==2.7.0',
        'requests==2.26.0',
        'toml==0.10.2',
        'tqdm==4.61.2',
        'urllib3==1.26.6',
    ],
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Video :: Conversion',
    ],
    entry_points={
        "console_scripts": [
            "vertvideo=vertvideo.__main__:main",
        ]
    },
)
