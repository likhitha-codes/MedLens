import os
import json
from flask import Flask, request, jsonify, send_from_directory
from functools import wraps
from models import init_db, Session, Patient, Report, Finding
from report_parser import parse_report_text

API_TOKEN = os.environ.get("MEDLENS_API_TOKEN", "dev-token")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__, static_folder='static')
init_db()

def require_token(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({"error": "missing token"}), 401
        token = auth.split(' ', 1)[1]
        if token != API_TOKEN:
            return jsonify({"error": "invalid token"}), 403
        return f(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/patients', methods=['POST'])
@require_token
def create_patient():
    data = request.json or {}
    with Session() as s:
        p = Patient(**{
            'name': data.get('name'),
            'age': data.get('age'),
            'sex': data.get('sex'),
            'notes': data.get('notes'),
        })
        s.add(p)
        s.commit()
        return jsonify({'id': p.id}), 201

@app.route('/api/patients/<int:pid>/reports', methods=['POST'])
@require_token
def upload_report(pid):
    # Accept raw text or file (text/plain)
    text = None
    if 'text' in request.form:
        text = request.form['text']
    elif 'file' in request.files:
        f = request.files['file']
        text = f.read().decode(errors='ignore')
    else:
        return jsonify({'error': 'no text or file provided'}), 400

    structured = parse_report_text(text)

    with Session() as s:
        rep = Report(patient_id=pid, raw=text)
        s.add(rep)
        s.commit()
        for fl in structured['findings']:
            f = Finding(report_id=rep.id, name=fl['name'], value=fl.get('value'), unit=fl.get('unit'),
                        reference_range=fl.get('reference_range'), flag=fl.get('flag'), provenance=json.dumps(fl.get('provenance', {})))
            s.add(f)
        s.commit()

    return jsonify({'report_id': rep.id, 'structured': structured}), 201

@app.route('/api/reports/<int:rid>/summary', methods=['GET'])
@require_token
def ai_summary(rid):
    # Returns a short patient-friendly summary using OpenAI if available
    with Session() as s:
        rep = s.get(Report, rid)
        if not rep:
            return jsonify({'error': 'not found'}), 404
        findings = s.query(Finding).filter_by(report_id=rid).all()
        structured = [{ 'name': f.name, 'value': f.value, 'unit': f.unit, 'flag': f.flag } for f in findings]

    prompt = "Provide a concise, patient-friendly summary of these findings without medical advice:\n" + json.dumps(structured)
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role':'user','content':prompt}], temperature=0.2)
            summary = resp.choices[0].message.content.strip()
        except Exception as e:
            summary = f"(AI error: {e})"
    else:
        summary = "OpenAI key not configured; summary unavailable."

    return jsonify({'summary': summary, 'structured': structured})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
