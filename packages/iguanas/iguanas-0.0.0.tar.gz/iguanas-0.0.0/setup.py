# Authors: James Laidler <jlaidler@paypal.com>
# License: BSD 3 clause
import setuptools
with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name="iguanas",
    version="0.0.0",
    author="James Laidler",
    description="Rule generation, optimisation, filtering and scoring library",
    packages=setuptools.find_packages(exclude=['examples']),
    install_requires=['category-encoders==2.0.0', 'matplotlib==3.0.3',
                      'seaborn==0.9.0', 'numpy==1.19.4', 'pandas==1.1.4',
                      'hyperopt==0.2.5', 'joblib==0.16.0', 'pytest==6.0.1',
                      'requests==2.20.1', 'httpretty==1.0.5',
                      'scikit-learn==0.23.2', 'scipy==1.7.1'],
    extras_require={
        'dev': ['pytest==6.0.1', 'check-manifest==0.47'],
        'spark': ['koalas==1.8.1', 'pyspark==3.1.2']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
