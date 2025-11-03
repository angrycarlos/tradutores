# Tradutor Python

Este repositório contém **duas versões de um tradutor em Python**:

1. **Versão com API** (LibreTranslate)  
2. **Versão usando a biblioteca `deep_translator`**  

Ambas permitem:  
- Traduzir texto entre idiomas  
- Gerar áudio do texto traduzido usando `gTTS` (Google Text-to-Speech)  
- Interface CLI e web via Flask

---

## 👂 Estrutura do Repositório

```
tradutor/
│
├── api/                  # Versão com API LibreTranslate
│   ├── translate_CLI.py  # CLI
│   ├── app.py            # Web app Flask
│   └── requirements.txt
│
├── deep_translator/      # Versão usando deep_translator
│   ├── translate_cli.py  # CLI
│   ├── app.py            # Web app Flask
│   └── requirements.txt
│
└── README.md
```

---

## 1️⃣ Versão com API (LibreTranslate)

Esta versão consome a API gratuita do [LibreTranslate](https://libretranslate.com/).

### Requisitos

- Python 3.8+  
- Bibliotecas:

```bash
pip install requests flask gtts
```

### Uso - CLI

```bash
python translate_CLI.py en pt "Hello world"
```

- `en` → idioma de origem  
- `pt` → idioma de destino  
- `"Hello world"` → texto a traduzir  

**Saída esperada:**  
```
Olá mundo
```

### Uso - Web

```bash
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

- Digite o texto, selecione os idiomas  
- Marque a opção **Gerar áudio** para baixar/escutar MP3  

⚠️ **Nota:** Se estiver atrás de proxy corporativo, configure `HTTP_PROXY` e `HTTPS_PROXY`.

---

## 2️⃣ Versão com biblioteca `deep_translator`

Esta versão **não depende de API externa** e utiliza [`deep_translator`](https://pypi.org/project/deep-translator/) para tradução via Google Translate.

### Requisitos

- Python 3.8+  
- Bibliotecas:

```bash
pip install deep-translator flask gtts
```

### Uso - CLI

```bash
python translate_cli.py
```

O programa solicitará:

- Idioma de origem (ex: `it`)  
- Idioma de destino (ex: `pt`)  
- Texto a traduzir

### Uso - Web

```bash
python app.py
```

Acesse no navegador:

```
http://127.0.0.1:5000
```

- Digite o texto, selecione os idiomas  
- Marque a opção **Gerar áudio** para baixar/escutar MP3  

**Vantagens:**

- Funciona sem conexão com API externa  
- Sem problemas de proxy  
- Tradução rápida para diversos idiomas

---

## 💡 Dicas e Observações

- **Áudio:** Gera arquivo `.mp3` usando `gTTS`.  
- **Idiomas:** Consulte a [lista de códigos ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).  
- **Proxy:** Para a versão API, se houver erro `407 Authentication Required`, configure proxy ou use a versão `deep_translator`.  
- **Templates Flask:** Ambos os apps web usam `render_template_string`, simplificando o projeto (não precisam de arquivos HTML separados).

---

## 📝 Licença

MIT License

