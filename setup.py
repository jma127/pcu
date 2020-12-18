from setuptools import setup, find_packages

setup(
    name='pcu',
    version='0.1.2',
    description='Comprehensive suite for competitive programming.',
    author='Jerry Ma',
    author_email='jmnospam@mail.com',
    url='https://github.com/jma127/pcu',
    license='BSD-new',

    packages=find_packages(),
    scripts=['scripts/pcu'],
    include_package_data=True,

    install_requires=[
        'colorama>=0.4<1',
        'filelock>=3<4',
        'inflection>=0.5<1',
        'pyyaml>=5<6',
    ],

    zip_safe=False,
)
