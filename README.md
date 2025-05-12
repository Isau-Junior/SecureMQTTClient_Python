# Cliente MQTT Seguro em Python

Este projeto tem como objetivo implementar um **cliente MQTT em Python para teste** capaz de:

- Conectar-se a brokers MQTT na nuvem;
- Publicar mensagens em tópicos;
- Subscrever-se e receber mensagens de tópicos;
- Estabelecer conexão segura com **TLS** e **SNI** (Server Name Indication), como exigido por brokers gratuitos **serverless** (ex: HiveMQ Cloud, emqx cloud, etc).
- Estabelece reconexões altomaticamente

---

## 🛠 Tecnologias e bibliotecas

- Python 3.10+
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) – biblioteca MQTT para Python
- TLS via biblioteca padrão `ssl` do Python
- [python-dotenv](https://pypi.org/project/python-dotenv/) – para carregar variáveis do arquivo `.env`

---

## 📁 Estrutura do Projeto
```bash
meu_cliente_mqtt/
├── src/
│   └── meu_cliente_mqtt/
│       ├── __init__.py
│       ├── mqtt_client.py    # Lógica principal de conexão MQTT, publicação e subscrição
│       └── main.py           # Script principal de execução
├── requirements.txt          # Dependências do projeto
├── .gitignore
└── README.md
```
---
## 🔐 Requisitos para conexões seguras

A maioria dos brokers gratuitos em nuvem exigem:

- Conexão com **TLS/SSL** (porta 8883)
- Uso de **SNI** (Server Name Indication) para validação do host
- Em alguns casos, autenticação por **usuário e senha**
- Certificados CA válidos (por padrão os brokers ja oferencem o certificado para ser baixado e usado)

---

## 🚀 Como executar o projeto

1. **Clone o repositório**
    ```bash
        git clone https://github.com/Isau-Junior/SecureMQTTClient_Python.git
        cd SecureMQTTCLIENT_Python
    ```

2. **Crie e ative o ambiente virtual**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```

3. **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure um broker MQTT em nuvem**
    Escolha e configure um broker MQTT serverless para conectar seu cliente.

    🧪 Exemplos de brokers gratuitos para teste

    | Broker |  Porta TLS | Requer usuário/senha? |   Observações|
    |:-----:|:-------:|:----------:|:----------------------------------------:|
    HiveMQ Cloud |	8883 |	Sim |	TLS com SNI obrigatório
    |Mosquitto (Eclipse)|	8883 |	Não |	TLS com SNI
    AWS IoT Core |	8883 |	Sim (com certificados)|	Integração mais avançada
    EMQX cloud | 8883 | não é obrigatório mas é recomendado | TLS com SNI obrigatório

5. **Adicionar o certificado TLS**
    - Baixe o certificado TLS fornecido pelo broker.
    - Crie uma pasta certs/ na raiz do projeto e mova o certificado para ela.

6. **Edite as configurações de conexão**
    Crie um arquivo .env na raiz do projeto com as variáveis necessárias:

    Exemplo:
    ```bash
        CLIENT_NAME=nome_para_o_seu_cliente-
        BROKER_HOST='URL_do_seu_eu-broker.cloud.com'
        PORT=8883
        USER_NAME='Nome_usuario'
        PASSWORD='Sua_senha'
        CERT_PATH='certs/seu_certificado.pem'
    ```

7. **Execute o programa**
    ```bash
    python src/meu_cliente_mqtt/main.py
    ```
---

## Observações

- O projeto ignora automaticamente arquivos sensíveis como .env e machine_id.txt (via .gitignore).
- A comunicação usa TLS com verificação de host via SNI, exigida por muitos brokers gratuitos.
- O projeto permite a subscrição em um tópico e entra em um loop infinito para que o usuario pubique mensagens nesse mesmo tópico
- comandos especificos como ```:sair``` ou ```:trocar``` para, respecticamente, encerrar o programa (```Ctrl + c``` também pode ser usado), ou trocar o tópico de subscrição
- Em caso de perda de conexão com o broker o sistema impede novas publicações e aguarda até que a conexão seja reestabelecida. 

