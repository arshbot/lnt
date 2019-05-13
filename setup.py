from setuptools import setup

setup(
    name='lnt',
    version='0.1',
    packages=['lnt', 'lnt.commands'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        lnt=lnt.cli:main
    ''',
)
