# Cliente MQTT Seguro em Python

Este projeto tem como objetivo implementar um **cliente MQTT em Python para teste** capaz de:

- Conectar-se a brokers MQTT na nuvem;
- Publicar mensagens em tópicos;
- Subscrever-se e receber mensagens de tópicos;
- Estabelecer conexão segura com **TLS** e **SNI** (Server Name Indication), como exigido por brokers gratuitos **serverless** (ex: HiveMQ Cloud, emqx cloud, etc).

---

## 🛠 Tecnologias e bibliotecas

- Python 3.10+
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) – biblioteca MQTT para Python
- TLS via biblioteca padrão `ssl` do Python

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
- Certificados CA válidos (por padrão os brokers ja oferencem o certificado para cer baixado e usado)

---

## 🚀 Como rodar o projeto

1. **Clone o repositório**
    ```bash
        git clone https://github.com/seu-usuario/meu_cliente_mqtt.git
    cd meu_cliente_mqtt
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
4. **Edite as configurações de conexão no main.py**

    Preencha com os dados do broker MQTT na nuvem (host, porta, usuário, senha, etc).
5. **Execute o programa**
    ```bash
    python src/meu_cliente_mqtt/main.py
    ```
---
🧪 Exemplos de brokers gratuitos para teste

| Broker |  Porta TLS | Requer usuário/senha? |   Observações|
|:-----:|:-------:|:----------:|:----------------------------------------:|
HiveMQ Cloud |	8883 |	Sim |	TLS com SNI obrigatório
|Mosquitto (Eclipse)|	8883 |	Não |	TLS com SNI
AWS IoT Core |	8883 |	Sim (com certificados)|	Integração mais avançada
EMQX cloud | 8883 | não é obrigatório mas é recomendado | TLS com SNI obrigatório

