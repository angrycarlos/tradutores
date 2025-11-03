import requests
import sys

API_URL = 'https://libretranslate.com/translate'

def traduzir(texto: str, source: str, target: str, api_key:str | None = None):
    data = {
        'q': texto,
        'source': source,
        'target': target,
        'format': 'text'
    }
    headers ={'Accept': 'application/json'}
    if api_key:
        data['api_key'] = api_key

    resp = requests.post(API_URL,data=data, headers=headers, timeout=15)
    resp.raise_for_status()
    res = resp.json()
    return res.get('traslatedText','')

def main():
    if len(sys.argv)<4:
        print('Uso: pyhton translate_CLI.py <source> <target> <texto>')
        print('Ex: python translate_CLI.py en pt \'Hello World\'')
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]
    texto = ' '.join(sys.argv[3:])

    try:
        traducao =traduzir(texto, source, target)
        print('\nTexto original: ', texto)
        print('Traduzindo: ', traducao)
    except requests.HTTPError as e:
        print('Erro HTTP:', e)
    except Exception as e:
        print('Erro:', e)

if __name__ == '__main__':
    main()