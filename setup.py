from setuptools import setup
from simple_blog import __version__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="mkdocs-simple-blog",
    version=__version__,
    author='Fernando Celmer',
    author_email='email@fernandocelmer.com',
    url='https://github.com/FernandoCelmer/mkdocs-simple-blog',
    include_package_data=True,
    description="Mkdocs Blog Theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=True,
    python_requires=">=3.6",
    install_requires=[
        'mkdocs>=1.4.2'
    ],
    entry_points={
        'mkdocs.themes': [
            'simple-blog = mkdocs_simple_blog',
        ]
    },
)
