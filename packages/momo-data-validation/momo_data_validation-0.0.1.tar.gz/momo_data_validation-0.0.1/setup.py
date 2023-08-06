from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Data Validation package'
LONG_DESCRIPTION = 'Extension of Tensorflow Data Validation'

# Setting up

setup(
    name='momo_data_validation',
    version=VERSION,
    author='Minh Dang',
    author_email='minh.dang4@mservice.com.vn',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages('', exclude=["tests", "docs", "BUILD", "dags"]),
    install_requires=[
      'google-cloud-bigquery',
      'tensorflow-data-validation==1.4.0'
    ],
    keywords=[
      'momo data validation'
    ],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: POSIX :: Linux',
      'Operating System :: Microsoft :: Windows',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3 :: Only',
      'Topic :: Scientific/Engineering',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Scientific/Engineering :: Mathematics',
      'Topic :: Software Development',
      'Topic :: Software Development :: Libraries',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
