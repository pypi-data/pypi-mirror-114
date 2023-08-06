import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(name='gym_tic_tac_toe3D',
      version='0.0.2',
      description='Gym Environment for 3D Tic Tac Toe',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Brandon Morgan',
      author_email="morganscottbrandon@gmail.com",
      license="MIT",
      install_requires=['gym',
                        'matplotlib',
                        'numpy']
      )