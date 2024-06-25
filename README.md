<p align="center"><img src="https://img.shields.io/badge/Blinhares-white?logo=github&logoColor=181717&style=for-the-badge&label=git" /><p align="center">

# Tornando um Streamlit App em um Executável com PyInstaller

Este projeto visa ajudar as pessoas que, por algum motivo, precisam tornar os seu aplicativo `Streamlit` executável.

Pesquisei bastante até chegar a uma solução que veio do @valerius21. A solução é super util e funcional e se quiser, vou deixar o link [aqui](https://github.com/valerius21/minimal-streamlit-pyinstaller-starter).

Mas antes, da uma olhada no que deixei por aqui porque tentei deixar tudo bem explicadinho...

## Ferramentas Utilizadas

[![Python](https://img.shields.io/badge/PYTHON-white?style=for-the-badge&logo=python&logoColor=3776AB)](https://www.python.org/)
[![streamlit](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)


## Utilização

### Clonando Repositório

```bash
git clone 
```

### Dependências

Existem algumas dependências necessárias para rodar o projeto, e vamos resolver isso facilmente com a instalação do poetry. Poetry é uma ferramenta interessante e recomendo conhece-la caso não tenha familiaridade.

__obs.:__ Os comandos abaixo podem ser substituídos por um comando a seguir(estando na raiz do projeto):

```bash
make
```

```bash
pip install poetry
```

Acesse a pasta onde o repositório foi clonado. Estando na mesma pasta em que os arquivos `poetry.lock e pyproject.toml` execute o comando:

```bash
poetry install
```

Pronto, ambiente virtual criado e dependências instaladas.

### Configuração

O coracao do nosso projeto esta nos passos a seguir com a criação e configuracao do arquivo `.spec`.

Há um arquivo de exemplo chamado `streamlit_app.spec_exemplo`, mas vou explicar a criação dele abaixo.

#### Criando o Arquivo

Crie um arquivo chamado `streamlit_app.spec`.

Abra o editor de texto e cole o cabeçalho abaixo.

```bash
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata
```

A seguir vamos fazer nossa primeira alteração.

```bash
datas = [
    # We need to include the streamlit_app.py file and the streamlit package
    ("main.py", "."),
    # assuming, your virtual environment is in the .venv directory
    ("/home/bruno/Documentos/Python/tornando_Streamlit_app_execu/.venv/lib/python3.10/site-packages/streamlit/runtime", "./streamlit/runtime")
    ]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")
```

`"main.py"` - nome do arquivo principal do seu app. No nosso caso adotamos o nome `main.py`. Recomendo adotar esse padrao para n mudar muito mais coisas.

`"/home/bruno/Documentos/Python/tornando_Streamlit_app_execu/.venv/lib/python3.10/site-packages/streamlit/runtime"` - Aqui algo importante, note que esse é o caminho para uma basta do streamlit dentro da sua instalação do python. Nesse caso estamos usando um ambiente virtual, logo a pasta deve apontar para ele.
__atenção__: o diretório varia de computador pra computador e de versão do python.

a proxima parte é a seguinte:

```bash

block_cipher = None

a = Analysis(
    # The path to the main script
    ['run.py'],
    # https://pyinstaller.org/en/stable/man/pyi-makespec.html?highlight=pathex#what-to-bundle-where-to-search
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    # include the custom hooks
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)
```

Aqui se poderia alterar varias coisas, mas não é recomendado.
O arquivo `run.py` faz referencia ao `main.py` então, caso realize alguma alteração, lembre-se disso.

Por fim, uma parte que vc com certeza vai querer mudar...

```bash

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    # The name of the executable file
    name='MeuStreamlitApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

O campo `name` define o nome do app, então altere como quiser.

O arquivo final deve ser exatamente igual a esse:

```bash
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [
    # We need to include the streamlit_app.py file and the streamlit package
    ("main.py", "."),
    # assuming, your virtual environment is in the .venv directory
    ("/home/bruno/Documentos/Python/tornando_Streamlit_app_execu/.venv/lib/python3.10/site-packages/streamlit/runtime", "./streamlit/runtime")
    ]
datas += collect_data_files("streamlit")
datas += copy_metadata("streamlit")

block_cipher = None

a = Analysis(
    # The path to the main script
    ['run.py'],
    # https://pyinstaller.org/en/stable/man/pyi-makespec.html?highlight=pathex#what-to-bundle-where-to-search
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    # include the custom hooks
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    # The name of the executable file
    name='MeuStreamlitApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

```

Voce ainda pode personalizar ícone e outras coisas. A documentação do Pyinstaller é bem extensa e te da muitas possibilidades.

### Buildando

Dentro da pasta do arquivo `.spec` faça:

```bash
pyinstaller streamlit_app.spec --clean --noconfirm
```

Apos o processo terminar, voce deve ter seu executável dentro da pasta `dist`.

 ![visitors](https://visitor-badge.laobi.icu/badge?page_id=blinhares.sistema_recomendacao_de_produtos_por_frequencia)
