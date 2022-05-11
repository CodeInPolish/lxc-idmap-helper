from setuptools import setup, find_packages


setup(
    name='lxd-idmap-helper',
    version='0.1',
    license='MIT',
    author="Marcin Krasowski",
    author_email='marcin.krasowski@hotmail.fr',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/CodeInPolish/lxd-idmap-helper',
    keywords='lxd idmap'
)