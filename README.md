# Insights Network

Aplicação desenvolvida para compartilhamento de insights e atribuir tags a eles, além de permitir a consulta de insights
a partir de suas tags.

A aplicação utiliza uma base de dados SQLite para armazenar seus dados, sendo desenvolvida na lingugem python 3.7, em um
computador com o sistema operacional Windows 10.

Para executa-la, basta entrar na pasta /backend e instalar as dependencias com o comando:

```bash
pip install -r requirements.txt
```

E então executar com o comando:

```bash
uvicorn main:app
```

A aplicação irá executar na porta 8000, podendo acessar a documentação pelo navegador clicando
[aqui](http://127.0.0.1:8000/docs).

A aplicação utiliza as libs:

* [FastAPI](https://fastapi.tiangolo.com/) para desenvolvimento de APIs com alta performance e com boas práticas
* [SqlAlchemy](https://www.sqlalchemy.org/) para orms flexíveis com alta eficiência e performance
* [Pydantic](https://pydantic-docs.helpmanual.io/) para valicação e manipulação de dados

Além disso, podemos verificar os testes unitários para o crud na pasta ./backend/back_unittest, para executa-los basta
usar o comando:

```bash
python -m unittest orm.ORMTestCase
```

Ou se quiser somente um teste em específico:

```bash
python -m unittest orm.ORMTestCase.[NOME DO TESTE]
```