from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='py-mapper',
    version='1.1.0a',
    author='Felipe Endlich',
    author_email='endlichfelipe@gmail.com',
    description='Python mapper library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/endlichfelipe/py-mapper',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    keywords=['MAPPER'],
    license='MIT',
    install_requires=[]
)
