import os
import setuptools

this_directory = os.path.abspath(os.path.dirname(__file__))

with open("readme.rst", "r") as f:
  long_description = f.read()


def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
          if not line.startswith('#')]


EXCLUDE_FROM_PACKAGES = ["example"]

setuptools.setup(
    name='iwantadmin',
    version='0.0.7',
    description='An admin pages and apis generator based on fastapi and tortoise.',
    long_description=long_description,
    keywords=['fastapi', 'admin', 'tortoise'],
    author='kai.zhang',
    author_email='1065879514@qq.com',
    url='https://github.com/zhangkai803/iwantadmin',
    install_requires=read_requirements('requirements.txt'),
    license='BSD License',
    packages=setuptools.find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
