from setuptools import setup, find_packages

setup(
    name="ImageSynthesisTool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.20.0',
        'opencv-python>=4.5.0',
        'PyYAML>=5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'image-synthesis=src.main:main',
        ],
    },
    python_requires='>=3.6',
)