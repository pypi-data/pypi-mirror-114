from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='csklearn',
    url='https://github.com/danielruneda/csklearn',
    author='Daniel Runeda',
    author_email='danielruneda@gmail.com',
    # Needed to actually package something
    packages=['csklearn'],
    # Needed for dependencies
    install_requires=[
        'numpy'
        ],
    # *strongly* suggested for sharing
    version='0.0.12',
    # The license can be anything you like
    # license='MIT',
    # description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    python_requires='>=3.6',
    # The package can not run directly from zip file
    zip_safe=False
)