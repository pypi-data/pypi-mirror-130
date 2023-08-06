from setuptools import setup, find_packages
import codecs
import os


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()



VERSION = '0.0.1'
DESCRIPTION = 'Wrapper Package for LipGan Project'
# Setting up
setup(
    name="Wav2Lipy",
    version=VERSION,
    author="Mehdi Hosseini Moghadam, Hanie Poursina",
    author_email="<m.h.moghadam1996@gmail.com> , <hanieh.poursina@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['librosa==0.7.0',
                      "numpy==1.17.1",
                      "opencv-contrib-python>=4.2.0.34",
                      "opencv-python==4.1.0.25",
                      "torch==1.1.0",
                      "torchvision==0.3.0",
                      "tqdm==4.45.0",
                      "numba==0.48"],
    keywords=['python', 
              'GAN',
              'LipGan',
              'Speech',
              'Lip-syncing', 
              'Video Lip-syncing', 
              'Image Lip-syncing',
              'Audio Lip-syncing'
              'Speech to gesture'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)










