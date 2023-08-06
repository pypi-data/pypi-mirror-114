from setuptools import setup, find_packages


setup(
    name='zeit.msal',
    version='1.1.0',
    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    url='https://github.com/ZeitOnline/zeit.msal',
    description='Microsoft Azure AD authentication helper for CLI applications',
    long_description='\n\n'.join(
        open(x).read() for x in ['README.rst', 'CHANGES.txt']),
    namespace_packages=['zeit'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'click',
        'msal',
        'setuptools',
    ],
    entry_points={'console_scripts': [
        'msal-token=zeit.msal.cli:cli'
    ]}
)
