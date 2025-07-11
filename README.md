# 📦 Price Bot API

Um projeto de backend com **Python + FastAPI** que automatiza a coleta de preços em sites da web utilizando **Selenium** e disponibiliza os dados por meio de uma **API REST**. Os dados coletados são armazenados localmente em **CSV**, **JSON** e **SQLite**.

---

<!-- ## 🚀 Funcionalidades

- 🔍 Raspagem de preços com Selenium
- 🧠 Salvamento de dados em JSON, CSV e banco SQLite
- 🔌 API REST com FastAPI para consultar os produtos
- ⚙️ Rotas para busca, listagem e exportação de dados
- 💾 Estrutura limpa e extensível para novos recursos -->

---

##  Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [SQLite3](https://www.sqlite.org/index.html)
- [Pandas](https://pandas.pydata.org/)
- [Uvicorn](https://www.uvicorn.org/) (servidor ASGI para FastAPI)

---

##  Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/price-bot-api.git
cd price-bot-api
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Execute o servidor FastAPI
```bash
uvicorn app.main:app --reload
```
Acesse: http://127.0.0.1:8000
Swagger (docs da API): http://127.0.0.1:8000/docs