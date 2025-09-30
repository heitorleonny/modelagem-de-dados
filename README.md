# Modelagem de Dados - PMFS_AMAZONAS

Este projeto realiza a modelagem e a popularização de dados de um banco MySQL para o sistema PMFS_AMAZONAS, utilizando Python e a biblioteca Faker para geração de dados fictícios.

## Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- **Python 3.11 ou superior**
- **MySQL** 
- **pip** (gerenciador de pacotes do Python)

## Instalação dos pacotes Python

Abra o terminal na pasta do projeto e execute:

```sh
pip install pymysql faker
```

## Configuração do Banco de Dados

1. **Crie o banco e as tabelas:**
   - Execute o script `scripts_sql/create.sql` no MySQL Workbench ou outro cliente MySQL para criar o banco `PMFS_AMAZONAS` e suas tabelas.

2. **Ajuste as credenciais de acesso ao banco:**
   - No arquivo `main.py`, confira se os dados de conexão estão corretos:
     ```python
     host="localhost",
     user="root",
     password="root",
     database="PMFS_AMAZONAS"
     ```
   - Altere conforme sua configuração local.

## Como rodar o projeto

1. **Limpe e popule o banco de dados:**
   - No terminal, execute:
     ```sh
     python main.py
     ```
   - O script irá apagar todos os dados das tabelas e popular com dados fictícios.

2. **Verifique os dados:**
   - Acesse o MySQL Workbench ou outro cliente e confira os dados inseridos nas tabelas do banco `PMFS_AMAZONAS`.

## Estrutura do Projeto

- `main.py`: Script principal para popular o banco.
- `scripts_sql/create.sql`: Script SQL para criar o banco e as tabelas.
- `README.md`: Este arquivo de instruções.

## Observações

- O script utiliza a biblioteca Faker para gerar dados aleatórios e fictícios.
- Caso queira alterar a quantidade de dados inseridos, modifique os parâmetros das funções no `main.py`.
- Certifique-se de que o MySQL está rodando antes de executar o script.

