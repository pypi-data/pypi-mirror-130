from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='adxbw',
    url='https://github.com/cs107-ucxbw/cs107-FinalProject/',
    author='Lanting Li, Jiaye Chen, Jenny Dong',
    author_email='lanting_li@hms.harvard.edu, jiaye_chen@hms.harvard.edu, wdong@hms.harvard.edu',
    # Needed to actually package something
    #packages=['numpy', 'pytest', 'setuptools'],
    packages = ['adxbw', 'adxbw.tests'],
    # Needed for dependencies
    install_requires=['numpy', 'pytest', 'setuptools'],
    # *strongly* suggested for sharing
    version='0.1.5',
    # The license can be anything you like
    license='MIT',
    description='Automated differentiation tool developed by ucxbw',
    # We will also need a readme eventually (there will be a warning)
    
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    package_dir={"adxbw": "adxbw", "adxbw.tests" : "adxbw/tests"},
    python_requires=">=3.8"
)
