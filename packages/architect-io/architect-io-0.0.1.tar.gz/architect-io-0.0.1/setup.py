from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='architect-io',
    version='0.0.1',
    description='',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/AhmadLabs/Architect',
    license='MIT',
    author='Hamza Ahmad',
    author_email='hamza.ahmad@me.com',
    packages=find_packages(),
    install_requires=[],
    extras_require={'dev': []},
    include_package_data=True,
    zip_safe=False,
    classifiers=[],
    keywords='python',
)
