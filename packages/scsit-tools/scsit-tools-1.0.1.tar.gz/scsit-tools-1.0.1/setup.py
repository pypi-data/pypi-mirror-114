import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scsit-tools",
    packages=['scsit'],
    # packages=setuptools.find_packages(),
    include_package_data=True,
    # package_data={
    #      './scsit/cfunction.so',
    # },
    version='1.0.1',
    license='MIT',
    author='HNU_XIE_LAB',
    author_email='susiew01@163.com',
    description='Biological gene analyse tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/shang-qian/SCSit',
    scripts=['bin/scsit'],
    keywords=['scsit', 'scsit-tools'],
    python_requires='>=2.7',
    install_requires=[ 
    ],
)
