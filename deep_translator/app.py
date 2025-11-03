import flask as f
from gtts import gTTS
import io
from deep_translator import GoogleTranslator as gl
import base64

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
""" 

ultima_traducao = {'audio_bytes': None}

def call_translate(q, source, target):
    try:
        if not source:
            source = 'auto'
        if not target:
            target = 'pt'
        return gl(source=source, target=target).translate(q)
    except Exception as e:
        return 'Erro ao traduzir: {}'.format(e)
    
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

        translated = call_translate(q,src,tgt)

        if tts_checked and translated and not translated.startswith('Erro'):
            tts = gTTS(translated,lang=tgt if tgt != 'auto' else 'pt')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            ultima_traducao['audio_bytes'] = mp3_fp.read()

    return f.render_template_string(
        TEMPLATE,
        q=q,
        src_teste=src,
        tgt_teste=tgt,
        translated=translated,
        tts=tts_checked,
        tts_audio=bool(ultima_traducao['audio_bytes']))

@app.route('/audio')
def audio():
    data = ultima_traducao.get('audio_bytes')
    if not data:
        return f.redirect(f.url_for('index'))
    return f.send_file(io.BytesIO(data), mimetype='audio/mpeg', as_attachment=True, download_name='tradução.mp3')


@app.route('/api/translate/', methods=['POST'])
def api_translate():
    data = f.request.get_json()
    text = data.get('text', '')
    src = data.get('source', 'auto')
    tgt = data.get('target', 'pt')
    tts_enabled = data.get('tts', False)

    if not text:
        return f.jsonify({'error': 'Campo "text" é obrigatório.'}), 400
    
    translated = call_translate(q,src,tgt)
    response = {'translated': translated}

    if tts_enabled and not translated.startswith('Erro'):
        try:
            tts_obj = gTTS(translated, lang=tgt if tgt != 'auto' else 'pt')
            mp3_fp = io.BytesIO()
            tts_obj.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            response['audio_base64'] = base64.b64encode(mp3_fp.read()).decode('utf-8')
        except Exception as e:
            response['tts_error'] = str(e)
    
    return f.jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
