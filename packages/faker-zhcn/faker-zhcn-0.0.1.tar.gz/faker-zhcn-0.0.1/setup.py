from setuptools import setup, find_packages

setup(
    name='faker-zhcn',
    version='0.0.1',
    author='buladou',
    author_email='1121031509@qq.com',
    #packages=['data-processing', 'model-builder','test'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    # url='',
    license='LICENSE',
    description='一个专门用于中文随机生成的库',
    long_description=open('README.md', encoding='utf-8').read(),
    python_requires='>=3.6',
    #install_requires=[    ],
    packages=find_packages()
)