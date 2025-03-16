from setuptools import setup
from mkdocs_simple_blog import __version__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="mkdocs-simple-blog",
    fullname='mkdocs-simple-blog',
    author='Fernando Celmer',
    version=__version__,
    author_email='email@fernandocelmer.com',
    url='https://github.com/FernandoCelmer/mkdocs-simple-blog',
    description="Mkdocs Blog Theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        'mkdocs>=1.6.1'
    ],
    packages=["mkdocs_simple_blog"],
    package_data={'mkdocs_simple_blog': ['*', '*/*', '*/*/*']},
    include_package_data=True,
    python_requires=">=3.8",
    zip_safe=True,
    entry_points={
        'mkdocs.themes': [
            'simple-blog = mkdocs_simple_blog',
        ]
    },
)
