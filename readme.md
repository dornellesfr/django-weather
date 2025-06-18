# Django Weather

Aplicação web Django para exibir informações meteorológicas usando a API Open-Meteo.

##  Sobre o Projeto

Projeto com o objetivo de selecionar uma localidade e pegar a informação de temperatura dela a cada período determinado.

##  Tecnologias Utilizadas

- **Python 3.13**
- **Django 5.2+**
- **SQLite** 
- **Docker & Docker Compose**
- **UV** (gerenciador de dependências)

## Como Executar

### Pré-requisitos

- Docker
- Docker Compose

### Executando com Docker

1. **Clone o repositório:**
```bash
ssh:
git clone git@github.com:dornellesfr/django-weather.git
```
```bash
https:
git clone https://github.com/dornellesfr/django-weather.git
```
```bash
cd django-weather
```

2. **Execute o projeto:**
```bash
docker-compose up --build
```

3. **Acesse a aplicação:**
```
http://localhost:8000
```

### Executando Localmente (Desenvolvimento)

1. **Instale o UV:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Instale as dependências:**
```bash
uv sync
```

3. **Execute as migrações:**
```bash
task migrations
```

4. **Execute o servidor de desenvolvimento:**
```bash
task dev
```

## Como utilizar o sistema

Você deve prencher os dados pedidos na página '/weather', como a localidade - nome por extenso  seu email, a temperatura máxima que pode ser atingida e a quantidade de tempo de intervalo para receber atualizações. 

Ao settar o alerta, você será redirecionado para a página de '/weather/history', a qual você pode colocar o email que foi usado e toda vez que quiser ver no geral o histórico de temperaturas daquela localidade.

Toda vez que emitir um alerta, um email será disparado para o endereço que você colocou no campo email em '/weather'

## Como parar o sistema

Você deve na página '/weather/history' colocar seu email e pesquisar. Após isso você tem de clicar no botão 'Stop monitoring' para ele cancelar a ação de ficar monitorando.


## Autor

**Fernando Dornelles Rocha**
- Email: fdornellesr@gmail.com
- GitHub: [@dornellesfr](https://github.com/dornellesfr)
