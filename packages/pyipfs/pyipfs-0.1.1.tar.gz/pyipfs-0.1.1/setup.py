from setuptools import setup

setup(
    name='pyipfs',
    version='0.1.1',    
    description='intract ipfs server with python',
    url='https://github.com/codingbeast/ipfs',
    author='Raaj',
    author_email='Raj0kumar00@gmail.com',
    license='MIT License',
    packages=['pyipfs'],
    install_requires=['requests',                   
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
