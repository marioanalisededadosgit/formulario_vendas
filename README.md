# Sistema de Vendas da Amanda

Este é um sistema completo de gestão de vendas desenvolvido com Flask (Python) e interface web moderna. O sistema permite registrar vendas, cadastrar clientes, gerenciar produtos e visualizar relatórios detalhados.

## 🚀 Funcionalidades

- **Registro de Vendas**: Formulário completo com cálculo automático de valor total, sugestão de preço baseada no produto e validação de campos obrigatórios.
- **Cadastro de Clientes**: Formulário para adicionar novos clientes com validação de CPF.
- **Gestão de Produtos**: Cadastro e edição de produtos com preços sugeridos.
- **Dashboard Interativo**: Tela inicial com cards para acesso rápido às funcionalidades.
- **Relatórios Completos**:
  - Vendas por mês
  - Vendas por cliente
  - Vendas por produto
  - Vendas por status de pagamento
  - Vendas por condição (normal/promoção)
  - Ticket médio
  - Clientes com mais compras
  - Produtos mais vendidos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.10+, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Banco de Dados**: SQLite
- **Bibliotecas**: Pandas, openpyxl

## 📂 Estrutura do Projeto

```
formulario_vendas/
├── backend/
│   ├── app.py              # Aplicação Flask principal
│   ├── database.py         # Gerenciamento do banco de dados
│   ├── models.py           # Modelos de dados (Produto, Cliente, Venda)
│   ├── routes.py           # Rotas da API
│   └── utils.py            # Funções utilitárias
├── frontend/
│   ├── index.html          # Menu principal
│   ├── vendas.html         # Formulário de vendas
│   ├── clientes.html       # Formulário de clientes
│   ├── produtos.html       # Formulário de produtos
│   ├── relatorios.html     # Relatórios
│   └── style.css           # Estilos globais
├── data/
│   ├── vendas.db           # Banco de dados SQLite
│   └── produtos.xlsx       # Planilha de produtos (backup)
├── requirements.txt        # Dependências do Python
└── README.md               # Documentação do projeto
```

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd formulario_vendas
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o backend

```bash
cd backend
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

### 5. Acesse a aplicação

Abra o navegador e acesse: `http://localhost:5000`

## 📝 Como Usar

### Menu Principal (`/menu`)

- **Registrar Venda**: Leva ao formulário de vendas.
- **Cadastrar Cliente**: Leva ao formulário de cadastro de clientes.

### Formulário de Vendas (`/vendas`)

1. Selecione o produto desejado (preço sugerido aparece automaticamente).
2. Informe a quantidade e o preço unitário (pode ajustar o preço sugerido).
3. Preencha os dados do cliente.
4. Selecione o status do pagamento e a condição.
5. Clique em "Registrar Venda".

### Formulário de Clientes (`/clientes`)

1. Preencha o nome do cliente.
2. Informe o CPF (apenas números, validação automática).
3. Clique em "Cadastrar Cliente".

### Formulário de Produtos (`/produtos`)

1. Preencha o nome do produto.
2. Informe o preço sugerido.
3. Clique em "Adicionar Produto".

### Relatórios (`/relatorios`)

Nesta página você pode visualizar:
- Vendas por mês
- Vendas por cliente
- Vendas por produto
- Vendas por status de pagamento
- Vendas por condição
- Ticket médio
- Clientes com mais compras
- Produtos mais vendidos

## 📁 Estrutura do Banco de Dados

O banco de dados `vendas.db` contém as seguintes tabelas:

### Tabela `produtos`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária |
| nome | TEXT | Nome do produto |
| preco | REAL | Preço sugerido |

### Tabela `clientes`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária |
| nome | TEXT | Nome do cliente |
| cpf | TEXT | CPF do cliente (único) |

### Tabela `vendas`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Chave primária |
| produto | TEXT | Nome do produto |
| quantidade | INTEGER | Quantidade vendida |
| preco_unitario | REAL | Preço unitário |
| valor_total | REAL | Valor total da venda |
| cliente | TEXT | Nome do cliente |
| status_pagamento | TEXT | Pago ou Devendo |
| condicao | TEXT | Normal ou Promoção |
| data_venda | TEXT | Data da venda (YYYY-MM-DD) |
| data_registro | TEXT | Data de registro (timestamp) |

## 📊 Relatórios Disponíveis

### Vendas por Mês
Mostra o total de vendas realizadas em cada mês.

### Vendas por Cliente
Lista todos os clientes e o total de vendas realizadas para cada um.

### Vendas por Produto
Mostra todos os produtos e o total de vendas de cada um.

### Vendas por Status de Pagamento
Mostra o total de vendas pagas e devendo.

### Vendas por Condição
Mostra o total de vendas normais e em promoção.

### Ticket Médio
Calcula o valor médio de cada venda.

### Clientes com Mais Compras
Lista os clientes que mais compraram, ordenados por quantidade de vendas.

### Produtos Mais Vendidos
Lista os produtos mais vendidos, ordenados por quantidade vendida.

## 📝 Como Contribuir

1. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
2. Faça suas alterações
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código fechado.

## 👥 Autor

- **Mário** - Desenvolvedor

## 📞 Suporte

Para dúvidas ou problemas, entre em contato com o desenvolvedor.


## Agora vamos melhorar o visual do trabalho,  a cliente é uma biologa, que gosta de borboletas e bichinhos, vc teria uma ideia boa para me mostrar