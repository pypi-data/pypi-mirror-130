from setuptools import setup

with open("README.md", "r", encoding="utf8") as readme:
    description = readme.read()

with open("version.txt", "r") as version:
    version_x = version.read()
    version_x = version_x.strip()

requirements = [
    "."
]

setup(
    name='heroku_flask',
    version=version_x,
    packages=requirements,
    url='https://github.com/AbhimanyuHK/heroku-flask',
    author='Abhimanyu HK',
    author_email='manyu1994@hotmail.com',
    description='Heroku setup for flask application',
    long_description=description,
    long_description_content_type="text/markdown",
    scripts=["script/heroku_flask.bat", "script/heroku_flask.sh"],
)
