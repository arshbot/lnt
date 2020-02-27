from setuptools import setup

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='lnt',
    version='1.1.1',
    author="arshbot",
    author_email="harshagoli@gmail.com",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thesis/lnt",
    packages=['lnt', 'lnt.commands', 'lnt.rpc', 'lnt.graphics', 'lnt.commands.utils'],
    install_requires=[
        'click',
        'grpcio-tools',
        'grpcio',
        'PyInquirer',
        'googleapis-common-protos',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        lnt=lnt.cli:main
    ''',
)
