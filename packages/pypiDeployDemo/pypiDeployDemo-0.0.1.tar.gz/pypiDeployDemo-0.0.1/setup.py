from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='pypiDeployDemo',
    description='pypiDeployDemo',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    version='0.0.1',
    license='MIT',
    author='Kushagra Bainsla',
    author_email='kushagrabainsla@gmail.com',
    url='https://github.com/Kushagrabainsla/build-flask-app',
    install_requires=['PyInquirer'],
    entry_points = {
        'console_scripts': ['pypiDeployDemo=pypiDeployDemo.main:main'],
    },
)