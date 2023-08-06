

import setuptools

with open('README.md') as f:
    README = f.read()

    setuptools.setup(
        author="Corné de Ruijt",
        author_email="cornederuijt@gmail.com",
        name='gecasmo',
        license="MIT",
        description='gecasmo is a package for estimating click models.',
        version='v0.0.1',
        long_description=README,
        url='https://github.com/cornederuijt/gecasmo',
        packages=setuptools.find_packages(),
        python_requires=">=3.8",
        install_requires=['scikit-learn >= 0.23.2',
                          'keras >= 2.4.3',
                          'numpy >= 1.18.5'],
        classifiers=[
            # Trove classifiers
            # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
            'Topic :: Scientific/Engineering',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python',
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
        ],
    )