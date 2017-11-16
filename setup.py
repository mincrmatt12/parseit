from setuptools import setup

long_desc = "<built from machine without pandoc, using temporary string>"
try:
    import os
    if not os.path.exists("build"):
        os.mkdir("build")
    if os.system("pandoc --from=markdown --to=rst --output=build/README.rst README.md") == 0:
        long_desc = open("build/README.rst").read()
except OSError:
    pass


setup(
    name='parseit',
    version='1.0.1',
    packages=['parseit'],
    url='https://github.com/',
    license='MIT',
    author='mincrmatt12',
    author_email='matthewmirvish@hotmail.com',
    description='Simple parser that creates ASTs',
    long_description=long_desc,
    install_requires=["future"],
    python_requires=">=2.7"
)
