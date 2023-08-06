from setuptools import setup,find_packages

setup(
        name='tutorial-diameter_nora',    # This is the name of your PyPI-package.
        version='1.0.0',    # Update the version number for new releases
        # The name of your script, and also the command you'll be using for calling it
        # Also other executables needed
        scripts=['nw_diameter',],
        description='Compute diameter of (largest pairwise distance within) a newick tree',
        long_description='This small script computes diameter of a newick tree.\
            Diameter is defined as the largest path distance between any pair of\
            leaves in tree.',
        long_description_content_type='text/plain',
        url='https://github.com/balabanmetin/pip-conda-tutorial-diameter',
        author='Metin Balaban, Uyen Mai',
        author_email='balaban@ucsd.edu, umai@eng.ucsd.edu',
        packages=find_packages(),
        zip_safe = False,
        install_requires=['treeswift'],
        include_package_data=True
)
