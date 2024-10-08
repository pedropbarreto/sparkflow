
# Projeto Airflow com PySpark e Docker

Este repositório contém um pipeline de dados usando **Airflow**, **PySpark** e **Docker** para coletar dados de uma API pública, transformá-los e salvá-los em diferentes camadas de processamento (bronze, silver, gold) utilizando o formato **Parquet**.

## Pré-requisitos

Certifique-se de que você tem as seguintes ferramentas instaladas:

- **Docker** e **Docker Compose**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Python 3.9** ou superior (opcional para testes locais sem Docker)

## Estrutura do Projeto

```
├── airflow                 # Diretório de configuração e execução do Airflow
│   ├── dags                # DAGs do Airflow
│   └── logs                # Logs do Airflow
├── bronze                  # Diretório para armazenar dados da camada bronze
├── silver                  # Diretório para armazenar dados da camada silver
├── gold                    # Diretório para armazenar dados da camada gold
├── Dockerfile              # Arquivo Dockerfile para configurar o ambiente
├── docker-compose.yml      # Arquivo Docker Compose para subir os serviços
└── README.md               # Documentação do projeto
```

## Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Construa a imagem Docker

Construa a imagem personalizada do projeto com base no `Dockerfile`:

```bash
docker build -t workspace:v001 .
```

### 3. Suba o ambiente com Docker Compose

Suba os serviços (Airflow e Spark) usando Docker Compose:

```bash
docker-compose up
```

Isso vai iniciar o Airflow e o Spark. A interface do Airflow estará disponível em [http://localhost:8080](http://localhost:8080).

### 4. Gerar uma Fernet Key (Opcional)

Se precisar gerar uma nova chave **Fernet** para o Airflow, execute o seguinte comando:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Adicione essa chave no arquivo `docker-compose.yml` ou `Dockerfile`, conforme necessário.

## Executando o Pipeline

### Acessar o Airflow

Após subir o ambiente, acesse o Airflow através do navegador em [http://localhost:8080](http://localhost:8080).

1. Faça login com as credenciais padrão: **airflow/airflow**.
2. No painel do Airflow, ative a DAG chamada **BREWERIES_PIPELINE**.
3. Execute a DAG manualmente para iniciar o pipeline de extração e processamento de dados.

### Dados Processados

Os dados serão processados e armazenados nas seguintes camadas:

- **Bronze**: Dados brutos coletados da API são salvos em `/bronze/breweries`.
- **Silver**: Dados transformados são salvos em `/silver/breweries`.
- **Gold**: Dados finalizados são salvos em `/gold/breweries`.

## Variáveis de Ambiente

Aqui estão as principais variáveis de ambiente que podem ser configuradas:

- `AIRFLOW__CORE__FERNET_KEY`: Chave utilizada para criptografia no Airflow.
- `JAVA_HOME`: Diretório do Java, necessário para o PySpark.
- `AIRFLOW__CORE__LOAD_EXAMPLES`: Para desativar as DAGs de exemplo no Airflow.

Essas variáveis podem ser configuradas no **Dockerfile** ou no **docker-compose.yml**.

## Estrutura do Código

### Dockerfile

O **Dockerfile** configura o ambiente Airflow com PySpark, instalando as dependências necessárias e definindo variáveis de ambiente como a chave Fernet e o Java Home.

```dockerfile
FROM apache/airflow:2.6.3-python3.9

USER root

RUN apt-get update --allow-releaseinfo-change &&     apt-get install -y gcc python3-dev openjdk-11-jdk git apt-transport-https ca-certificates curl &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# Definir variáveis de ambiente
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV AIRFLOW__CORE__FERNET_KEY='sua-chave-fernet-aqui'

USER airflow

# Instalar pacotes necessários
RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark
```

### Docker Compose

O **docker-compose.yml** define os serviços necessários para o ambiente de execução, incluindo o Airflow e os volumes locais para persistência de dados.

```yaml
version: '3'

services:
  sleek-airflow:
    image: workspace:v001
    environment:
      - AIRFLOW__CORE__FERNET_KEY=sua-chave-fernet-aqui
      - AIRFLOW__CORE__LOAD_EXAMPLES=False
      - JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    volumes:
      - ./airflow:/opt/airflow  
      - ./bronze:/bronze
      - ./silver:/silver
      - ./gold:/gold
    ports:
      - "8080:8080"
    command: airflow standalone
```

## Contribuindo

1. Faça um **fork** do projeto.
2. Crie uma **branch** para sua feature (`git checkout -b feature/nova-feature`).
3. **Commit** suas alterações (`git commit -am 'Adiciona nova feature'`).
4. **Envie** para a branch principal (`git push origin feature/nova-feature`).
5. Crie um novo **Pull Request**.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
