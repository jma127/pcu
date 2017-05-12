from setuptools import setup, find_packages

setup(
    name='pcu',
    version='0.1.1',
    description='Comprehensive suite for competitive programming.',
    author='Jerry Ma',
    author_email='jma127@users.noreply.github.com',
    url='https://github.com/jma127/pcu',
    license='BSD-new',

    packages=find_packages(),
    scripts=['scripts/pcu'],
    include_package_data=True,

    install_requires=[
        'colorama>=0.3<1',
        'filelock>=2<3',
        'inflection>=0.3<1',
        'pyyaml>=3<4',
    ],

    zip_safe=False,
)
