import pip
from setuptools import find_packages, setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yolo_v5_tflite',
    version='1.0',
    author="Neha Soni",
    author_email = 'soni.neha45@gmail.com',
    url = 'https://github.com/neso613/yolo-v5-pip-wheel',
    description="YOLO_v5 - most advanced vision AI model for object detection in TFLite. ",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache-2.0",
    packages=['yolo_v5_tflite'],
    include_package_data=True,
    package_data={
        'yolo_v5': ['yolo-v5-dynm.tflite'],
    },
    python_requires=">=3.5",
    install_requires=[
	"tensorflow>=2.4.1",
        "numpy>=1.18.5",
 	"opencv-python>=4.1.2",
	"Pillow",
	"PyYAML>=5.3.1",
	"scipy>=1.4.1",
	"torchvision>=0.8.1"
    ]
)
