from setuptools import setup, find_packages

setup(
    name='hello_zun',
    version='1.0',
    license='MIT',
    author="Zunnuran Ahmad",
    author_email='zunnuran.ahmad@invozone.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
#     url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],
)
