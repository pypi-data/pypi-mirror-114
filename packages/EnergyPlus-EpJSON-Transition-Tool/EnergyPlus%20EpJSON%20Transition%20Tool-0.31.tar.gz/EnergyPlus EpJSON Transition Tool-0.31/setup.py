import pathlib
from setuptools import setup


readme_file = pathlib.Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name="EnergyPlus EpJSON Transition Tool",
    version="0.31",
    description="A tool for converting EpJSON files which may need changing from one version to another",
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author='Edwin Lee, National Renewable Energy Laboratory, for United States Department of Energy',
    author_email='edwin_dot_lee@nrel.gov',
    url='https://energyplus.net',
    license='ModifiedBSD',
    entry_points={
        'console_scripts': ['epjson_transition=epjson_transition.transition:main']
    }
)
