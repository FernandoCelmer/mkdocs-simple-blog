# Testes Unitários - mkdocs-simple-blog

Este diretório contém os testes unitários para o tema mkdocs-simple-blog.

## Estrutura de Testes

```
tests/
├── __init__.py              # Inicialização do pacote de testes
├── conftest.py              # Configuração e fixtures do pytest
├── test_theme_config.py     # Testes de configuração do tema
├── test_templates.py        # Testes dos templates Jinja2
├── test_modules.py          # Testes dos módulos do tema
├── test_assets.py           # Testes dos assets (CSS, JS, imagens)
└── test_package.py         # Testes da estrutura do pacote
```

## Instalação

Instale as dependências de desenvolvimento:

```bash
pip install -e ".[dev]"
```

Ou usando poetry:

```bash
poetry install
```

## Executando os Testes

### Todos os testes

```bash
pytest
```

### Com cobertura de código

```bash
pytest --cov=mkdocs_simple_blog --cov-report=html
```

### Testes específicos

```bash
# Apenas testes de templates
pytest tests/test_templates.py

# Apenas testes de configuração
pytest tests/test_theme_config.py

# Teste específico
pytest tests/test_templates.py::test_base_template_renders
```

### Modo verboso

```bash
pytest -v
```

## Tipos de Testes

### 1. Testes de Configuração (`test_theme_config.py`)
- Validação do arquivo `mkdocs_theme.yml`
- Verificação de valores padrão
- Registro do tema como plugin

### 2. Testes de Templates (`test_templates.py`)
- Existência dos templates
- Renderização dos templates
- Inclusão de recursos (Bootstrap, Highlight.js)
- Estrutura HTML básica

### 3. Testes de Módulos (`test_modules.py`)
- Existência de todos os módulos
- Validação de estrutura HTML
- Carregamento como templates Jinja2

### 4. Testes de Assets (`test_assets.py`)
- Existência de diretórios (CSS, JS, img)
- Arquivos obrigatórios presentes
- Arquivos não vazios

### 5. Testes de Pacote (`test_package.py`)
- Estrutura do pacote
- Metadados (versão, autor)
- Arquivos obrigatórios

## Fixtures Disponíveis

- `temp_dir`: Diretório temporário para testes
- `mkdocs_config`: Configuração mínima do MkDocs
- `mock_page`: Objeto de página mock
- `theme_dir`: Caminho do diretório do tema
- `template_env`: Ambiente Jinja2 para templates
- `modules_dir`: Diretório de módulos
- `assets_dir`: Diretório de assets

## Adicionando Novos Testes

1. Crie um novo arquivo `test_*.py` no diretório `tests/`
2. Importe as fixtures necessárias de `conftest.py`
3. Escreva funções de teste começando com `test_`
4. Execute os testes para verificar

Exemplo:

```python
def test_my_feature(theme_dir):
    """Test my new feature."""
    assert theme_dir.exists()
```

## Cobertura de Código

O pytest está configurado para gerar relatórios de cobertura. Após executar os testes com `--cov`, você pode visualizar o relatório HTML em `htmlcov/index.html`.

