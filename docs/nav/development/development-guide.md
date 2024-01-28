Last updated January 28, 2024

---

## How to test the local package?

#### Virtual environment

- Create your virtual environment.

```bash
python -m venv venv
```

#### Environment activation

- Activate the virtual environment.

```bash
source venv/bin/activate
```

#### Install the requirements

- Install the necessary requirements to be able to test the application.

```bash
pip install -r requirements.txt --no-cache-dir
```

#### Development

- Make your changes as desired in the `./mkdocs_simple_blog` folder. You can enjoy and change whatever you want, please have fun.

```bash
ls mkdocs_simple_blog
```

#### Build and Install

- Run the script that creates and installs the local package.


```bash
python scripts/install_local.py
```

#### Test

- Run the following command to run the server.

```bash
mkdocs serve
```

#### View Template

- Now you can access the [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Commit Style

- ⚙️ FEATURE
- 📝 PEP8
- 📌 ISSUE
- 🪲 BUG
- 📘 DOCS
- 📦 PyPI
- ❤️️ TEST
- ⬆️ CI/CD
- ⚠️ SECURITY

## License

![GitHub](https://img.shields.io/github/license/FernandoCelmer/mkdocs-simple-blog?style=flat-square)

This project is licensed under the terms of the MIT license.