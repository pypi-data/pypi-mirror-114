from setuptools import setup

setup(
    name='folderArranger',
    version='0.1.0',    
    description='A library to assist in organizing folders of student projects so that they are easier to grade.',
    url='https://github.com/mehmetsinanyildirim/folderArranger',
    author='Mehmet Sinan YILDIRIM',
    author_email='mehmetsinanyildirim@yandex.com',
    license='BSD 2-clause',
    packages=['folderArranger'],
    install_requires=['colorama',
                      ],
    include_package_data=True,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows',        
        'Programming Language :: Python :: 3.8',
    ],
)    