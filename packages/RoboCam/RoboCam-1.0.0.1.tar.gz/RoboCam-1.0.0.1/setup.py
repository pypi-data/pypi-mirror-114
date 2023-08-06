from setuptools import setup, find_packages, setuptools

setup(
    name='RoboCam',
    version='1.0.0.1',
    description='Python library for RoboCam',
    author='Roborobo',
    author_email='roborobolab@gmail.com',
    url = 'https://eng.roborobo.co.kr/main',
    download_url = 'https://github.com/RoboroboLab/RoboCam/archive/master.tar.gz',
    license='MIT',
    packages = setuptools.find_packages(),
    keywords = ['RoboCam','roborobo'],
    python_requires='>=3',
    package_data =  {
        'RoboCam' : [
            'res/model/face_detector.tflite',
            'res/model/face_keypoints.tflite',
            'res/model/face_recognizer.tflite',
            'res/model/iris_landmark.tflite',
            'res/model/mnist.tflite'
    ]},
    zip_safe=False,
    install_requires=[
        'opencv-contrib-python==3.4.8.29',
        'tflite==2.4.0'
    ], 
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)