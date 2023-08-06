from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cannyfier',
    version='0.2.3',
    author='Pascual Martinez',
    author_email='pascual.martinezzapata@gmail.com',
    description='Show canny on any part of the screen. Better to use with video',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['cannyfier'],
    install_requires=['numpy', 'opencv-python', 'mss', 'Pillow']
)
