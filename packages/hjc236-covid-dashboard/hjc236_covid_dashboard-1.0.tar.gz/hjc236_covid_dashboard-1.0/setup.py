from distutils.core import setup
from pathlib import Path

# Get README file and pass this so it displays on PyPi
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'hjc236_covid_dashboard',
    packages = ['hjc236_covid_dashboard'],
    version = '1.0',
    license='MIT',
    description = 'A python project which generates a web dashboard with COVID-19 data and relevant news articles.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'hjc236',
    author_email = '',
    url = 'https://github.com/hjc236/hjc236_covid_dashboard',
    download_url = 'https://github.com/hjc236/hjc236_covid_dashboard/archive/refs/tags/v1.0.tar.gz',
    keywords = ['coronavirus', 'event-driven', 'dashboard'],
    install_requires=[
        'uk_covid19',
        'flask',
        'pytest'

    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)