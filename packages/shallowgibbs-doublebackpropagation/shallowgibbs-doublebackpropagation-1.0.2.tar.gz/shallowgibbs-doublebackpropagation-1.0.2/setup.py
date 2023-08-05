from setuptools import setup, find_packages
import pathlib
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
#long_description = 'Package for Double Backpropagation with the Shallow Gibbs Model'


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE/"README.md").read_text()


setup(
        name ='shallowgibbs-doublebackpropagation',
        version ='1.0.2',
        author ='Alejandro, Murua and Alahassa, Nonvikan Karl-Augustt',
        author_email ='alahassa@dms.umontreal.ca',
        url ='https://github.com/kgalahassa/shallowgibbs-doublebackpropagation',
        description ='Shallow Gibbs Double Backpropagation',
        long_description = README,
        long_description_content_type ="text/markdown",
        license ='GNU General Public License v3.0',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'shallowgibbs-doublebackpropagation = shallowgibbs.doublebackpropagation:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
        ),
        keywords ='Shallow Gibbs, Neural Network, Double Backpropagation',
        install_requires = requirements,
        zip_safe = False
)