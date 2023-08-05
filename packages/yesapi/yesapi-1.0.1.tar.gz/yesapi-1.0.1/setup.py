from setuptools import setup

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# python3 -m twine upload dist/*
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='yesapi',
    version='1.0.1',
    packages=['yesapi'],
    url='https://github.com/asihacker/yesapi',
    license='MIT license',
    author='chenjunxue',
    author_email='asihacker@gmail.com',
    description='yesapi-python3-sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    keywords=['yesapi', 'api', 'yes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
