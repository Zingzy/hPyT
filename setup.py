from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hPyT',
    version='1.2.1',
    description='Hack Python Titlebar - A package to manipulate windows and titlebar of GUI applications made using python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='zingzy',
    url='https://github.com/zingzy/hPyT',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11' ,
        "Operating System :: Microsoft :: Windows",
    ],
    keywords='Tkinter wxpython pyqt pyside GUI window controls decorations hide show titlebar',
)
