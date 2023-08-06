from setuptools import setup  # type: ignore


with open('readme.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()


setup(
    name='ytrssil',
    author='Pavle Portic',
    author_email='git@theedgeofrage.com',
    description=(
        'Subscribe to YouTube RSS feeds and keep track of watched videos'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=('LICENSE',),
    homepage='https://gitea.theedgeofrage.com/TheEdgeOfRage/ytrssil',
    repository='https://gitea.theedgeofrage.com/TheEdgeOfRage/ytrssil',
    documentation='https://gitea.theedgeofrage.com/TheEdgeOfRage/ytrssil',
    version='0.1.0',
    packages=['ytrssil'],
    package_data={'': ['py.typed']},
    include_package_data=True,
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ytrssil = ytrssil.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
    ],
)
