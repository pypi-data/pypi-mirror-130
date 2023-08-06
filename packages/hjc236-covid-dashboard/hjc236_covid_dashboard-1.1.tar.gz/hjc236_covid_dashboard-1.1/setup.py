import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name = 'hjc236_covid_dashboard',
    version = '1.1',
    author = 'hjc236',
    author_email = '',
    description = 'A python project which generates a web dashboard with COVID-19 data and relevant news articles.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/hjc236/hjc236_covid_dashboard/',
    packages = setuptools.find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
)