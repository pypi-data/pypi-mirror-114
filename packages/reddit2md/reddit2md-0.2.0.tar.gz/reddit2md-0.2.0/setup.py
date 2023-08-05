import setuptools

setuptools.setup(
    name='reddit2md',
    version='0.2.0',
    author='Lewis Lee',
    author_email='lewislee@lewislee.net',
    packages=['reddit2md'],
    url='https://github.com/lewisleedev/reddit2md',
    license='LICENSE',
    description='Useful towel-related stuff.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "praw >= 7.3.0",
        "pytz == 2021.1"
    ],
)