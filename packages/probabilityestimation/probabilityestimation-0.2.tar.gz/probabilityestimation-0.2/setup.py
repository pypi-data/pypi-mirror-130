from setuptools import setup, find_packages
setup(
    name='probabilityestimation',
    version='0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package for computing information about Poisson, Gamma, and Exponential distributions.',
    install_requires=[
    'numpy',
    'pandas', 
    'scipy',
    'matplotlib',
    'plotly'
    ],
    url='https://github.com/SaraAnnHall/533Lab4_SaraJustine.git',
    author='Sara Hall and Justine Filion',
    author_email='saraannh@student.ubc.ca, filionjustine05@gmail.com'
)
