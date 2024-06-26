# Migração de Dados do MongoDB para MySQL

## Descrição
Este projeto realiza a migração de dados de uma coleção MongoDB para um esquema relacional em MySQL. O objetivo é transformar os documentos do MongoDB em um formato relacional adequado para análises futuras, mantendo a integridade e a estrutura dos dados.

## Estrutura do Banco de Dados

### Tabela `users`
Esta tabela armazena as informações dos usuários.

| Coluna            | Tipo        | Descrição                      |
|-------------------|-------------|--------------------------------|
| id                | Integer     | Chave primária                 |
| user_id           | String(36)  | Identificador único do usuário |
| name              | String(100) | Nome do usuário                |
| email             | String(100) | Email do usuário               |
| address           | String(200) | Endereço do usuário            |
| date_of_birth     | DateTime    | Data de nascimento             |
| gender            | String(10)  | Gênero                         |
| phone_number      | String(20)  | Número de telefone             |
| profile_picture   | String(200) | URL da foto de perfil          |
| account_status    | String(20)  | Status da conta                |
| last_access       | DateTime    | Último acesso                  |
| preferences       | Text        | Preferências                   |
| privacy_settings  | String(20)  | Configurações de privacidade   |
| book_count        | Integer     | Contagem de livros             |
| registration_date | DateTime    | Data de registro               |

### Tabela `banking_details`
Esta tabela armazena os detalhes bancários dos usuários.

| Coluna         | Tipo        | Descrição                      |
|----------------|-------------|--------------------------------|
| id             | Integer     | Chave primária                 |
| user_id        | Integer     | Chave estrangeira para `users` |
| account_number | String(20)  | Número da conta                |
| bank_name      | String(100) | Nome do banco                  |
| swift_code     | String(20)  | Código SWIFT                   |

### Tabela `books`
Esta tabela armazena as informações dos livros.

| Coluna | Tipo        | Descrição                    |
|--------|-------------|------------------------------|
| id     | Integer     | Chave primária               |
| title  | String(200) | Título do livro              |
| author | String(100) | Autor do livro               |
| isbn   | String(36)  | ISBN do livro                |
| year   | Integer     | Ano de publicação (opcional) |

### Tabela `userbooks`
Esta tabela armazena a relação entre usuários e livros.

| Coluna  | Tipo    | Descrição                      |
|---------|---------|--------------------------------|
| user_id | Integer | Chave estrangeira para `users` |
| book_id | Integer | Chave estrangeira para `books` |

## Configuração

### Dependências
Instale as dependências usando o `requirements.txt`:

```sh
pip install -r requirements.txt
