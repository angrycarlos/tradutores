from deep_translator import GoogleTranslator as gl

def traduzir(texto, source, target):
    try:
        return gl(source=source, target=target).translate(texto)
    except Exception as e:
        return 'Erro ao traduzir: {}'.format(e)
    
def main():
    source=input('Idioma de origem (ex: it(italiano), auto(automatico), en(ingles): ')
    target=input('Idioma de destino (Ex: pt(portugues), auto(automatico), en(ingles):  )')
    texto=input('Dgite o texto a ser traduzido: ')

    traducao = traduzir(texto, source,target)
    print('\nTexto original:', texto)
    print('Traduzido:',traducao)

if __name__ == '__main__':
    main()
