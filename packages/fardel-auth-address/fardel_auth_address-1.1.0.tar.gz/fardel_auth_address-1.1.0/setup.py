from setuptools import setup, find_packages

setup(
    name='fardel_auth_address',
    version='1.1.0',
    description='Address extension for FardelCMS users',
    author='Sepehr Hamzehlouy',
    author_email='s.hamzelooy@gmail.com',
    url='https://github.com/FardelCMS/fardel_auth_address',
    packages=find_packages(".", exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.7',
    ],
)
