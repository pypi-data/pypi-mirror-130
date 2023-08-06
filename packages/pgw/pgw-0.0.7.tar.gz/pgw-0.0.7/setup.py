from setuptools import setup
import os

setup(name='pgw',packages=['pygwin'],version='0.0.7',author='themixray',
    description='A library for creating Python applications.',
    license='MIT',install_requires=['cython','pywin32','pygame','inputs',
     'pydub','wxPython','pyautogui','moviepy','pipwin','wave','opencv-python'])
os.system('pipwin install pyaudio')
# os.system('pipwin install pyhook')
