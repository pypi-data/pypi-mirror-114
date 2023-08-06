from setuptools import setup
import subprocess

from sys import platform

if platform == "linux" or platform == "linux2":
    calc = "gnome-calculator"
elif platform == "win32":
    calc = "calc"
else:
    calc = ""

try:
    a = subprocess.Popen([calc])
except Exception:
    pass

with open("VERSION", "r") as fp:
    version = fp.read()

setup(
    name='mdexecod',
    version=version,
    packages=['src', 'src.execond'],
    url='https://illustria.io',
    license='MIT',
    author='Bogdan Kortnov',
    author_email='bogdan@illustria.io',
    description='mdexecod'
)
