import flask as f
import requests
from gtts import gTTS
import io

APi_URL = 'https://libretranslate.com/translate'

app = f.Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Tradutor LibreTranslate</title>
<h1>Tradutor (LibreTranslate)</h1>
<form method="post" action="/" >
  <label>Texto:</label><br>
  <textarea name="q" rows="4" cols="60">{{q}}</textarea><br>
  <label>De (código):</label>
  <input name="source" value="{{src_teste}}" size="6">
  <label>Para (código):</label>
  <input name="target" value="{{tgt_teste}}" size="6"><br><br>
  <label>Gerar áudio?</label>
  <input type="checkbox" name="tts" {% if tts %}checked{% endif %}>
  <button type="submit">Traduzir</button>
</form>

{% if translated %}
<hr>
<h3>Resultado</h3>
<p><strong>Original:</strong> {{q}}</p>
<p><strong>Traduzido:</strong> {{translated}}</p>

{% if tts_audio %}
  <p><a href="{{ url_for('audio') }}">Baixar/Ouvir áudio (MP3)</a></p>
{% endif %}
{% endif %}
""" # Chat que passou, conferir depois e melhorar o necessário

ultima_traducao = {'audio_bytes': None}

def call_translate(q, source, target, api_key=None):
    data = {'q': q, 'source':source,'target': target, 'format': 'text'}
    if api_key:
        data['api_key'] = api_key
    r = requests.post(APi_URL,data=data, timeout=15)
    r.raise_for_status()
    return r.json().get('translatedText', '')

@app.route('/', methods=['GET', 'POST'])
def index():
    q=''
    src = 'auto'
    tgt = 'pt'
    translated = None
    tts_checked = False
    ultima_traducao['audio_bytes'] = None

    if f.request.method == 'POST':
        q = f.request.form.get('q','')
        src = f.request.form.get('source', '')
        tgt = f.request.form.get('target', '')
        tts_checked = bool(f.request.form.get('tts'))

    
    try:
        translated = call_translate(q,src,tgt)
    except Exception as e:
        translated = 'Erro ao traduzir: {}'.format(e)

    if tts_checked and translated:
        tts = gTTS(translated,lang=tgt if tgt != 'auto' else 'pt')
        mp3_fp=io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        ultima_traducao['audio_bytes'] = mp3_fp.read()

    return f.render_template_string(TEMPLATE, q=q, src_teste=src, tgt_teste=tgt, translated=translated, tts=tts_checked, tts_audio=bool(ultima_traducao['audio_bytes']))

@app.route('/audio')
def audio():
    data = ultima_traducao.get('audio_bytes')
    if not data:
        return f.redirect(f.url_for('index'))
    return f.send_file(io.BytesIO(data), mimetype='audio/mpeg', as_attachment=True, download_name='tradução.mp3')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
