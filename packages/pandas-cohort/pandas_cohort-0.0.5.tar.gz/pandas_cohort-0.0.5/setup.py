from distutils.core import setup
setup(
    name='pandas_cohort',
    packages=['pandas_cohort'],
    version='0.0.5',

    license='MIT',
    description='simple cohort analysis custom accessor for pandas',
    author='yasir almutairi',
    author_email='yasir.masad1@gmail.com',
    url='https://github.com/Yasalm/pandas_cohorts',

    keywords=['pandas cohort analysis', ],
    install_requires=['pandas>=1.1.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
