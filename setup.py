from setuptools import setup


setup(
    name='timetracker',
    version='0.1',
    packages=['commandline_client', 'entities', 'gateway', 'use_cases'],
    install_requires=['arrow', 'Click'],
    entry_points="""
        [console_scripts]
        timetrack=commandline_client.timetrack:cli
    """,
)
