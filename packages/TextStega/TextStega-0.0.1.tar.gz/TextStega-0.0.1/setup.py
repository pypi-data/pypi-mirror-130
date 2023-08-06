from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TextStega',
    version='0.0.1',
    description='library useful for text steganography',
    # long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Atharva Vidwans',
    author_email='atharvavidwans@gmail.com',
    license='MIT',
    classifiers=classifiers,
    kerwords='steganography',
    packages=find_packages(),
    install_requires=['numpy',
                      'matplotlib',
                      'opencv-python',
                      'math']
)
    