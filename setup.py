from setuptools import setup

setup(
    name='lnt',
    version='0.2.1',
    packages=['lnt', 'lnt.commands', 'lnt.rpc', 'lnt.graphics', 'lnt.commands.utils'],
    include_package_data=True,
    install_requires=[
        'click',
        'grpcio-tools',
        'grpcio',
        'PyInquirer',
    ],
    entry_points='''
        [console_scripts]
        lnt=lnt.cli:main
    ''',
)
