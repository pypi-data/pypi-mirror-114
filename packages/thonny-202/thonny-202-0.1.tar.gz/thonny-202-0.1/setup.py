from setuptools import setup


setup(
    name='thonny-202',
    version='0.1',
    author='Jonathan Campbell',
    author_email='jonathan.campbell@mcgill.ca',
    description='COMP 202 theme for Thonny IDE',
    long_description=open('README.md').read(),
    url='https://github.com/campbelljc/thonny-202',
    license='MIT',
    packages=['thonnycontrib.202theme'],
    include_package_data = True,
    install_requires=['thonny >= 3.0.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Embedded Systems',
    ],
    keywords='IDE education programming Thonny COMP202 theme',
    platforms=['Windows', 'macOS', 'Linux'],
)