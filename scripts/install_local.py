from pip import main
from os import system
from pathlib import Path
from shutil import rmtree


CONTEXT = Path.cwd()


def install_package() -> None:
    version = open(file='LAST_VERSION').read().replace('-', '.')

    main(['uninstall', 'mkdocs-simple-blog', '-y'])
    main(['install', f'dist/mkdocs-simple-blog-{version}.tar.gz', '--no-cache-dir'])


def build_package() -> None:
    system('python -m build')


def install_requirements() -> None:
    main(['install', '--upgrade', 'pip'])
    main(['install', 'build'])


def remove_tree(path: Path) -> None:
    rmtree(path=path)


if __name__ == '__main__':
    _folders = [
        CONTEXT.joinpath('dist'),
        CONTEXT.joinpath('mkdocs_simple_blog.egg-info')
    ]

    for folder in _folders:
        if folder.exists():
            remove_tree(path=folder)

    install_requirements()
    build_package()
    install_package()
