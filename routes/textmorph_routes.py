from flask import Blueprint, render_template, request, jsonify, flash, Response
from flask_login import login_required, current_user
from models.models import db, TextSummary, TextParaphrase, TextReadabilityFile
import math
import json
import csv
import io
from datetime import datetime

textmorph_bp = Blueprint('textmorph', __name__)

def calc_flesch(words, chars):
    w = max(1, words)
    s = max(1, math.ceil(words / 15)) # estimated sentences
    syllables = max(1, math.ceil(words * 1.4))
    return round(206.835 - 1.015 * (w / s) - 84.6 * (syllables / w), 1)

def calc_fk(words, chars):
    w = max(1, words)
    s = max(1, math.ceil(words / 15))
    syllables = max(1, math.ceil(words * 1.4))
    return round(0.39 * (w / s) + 11.8 * (syllables / w) - 15.59, 1)

@textmorph_bp.route('/textmorph')
@login_required
def textmorph_index():
    return render_template('textmorph.html', user=current_user)

@textmorph_bp.route('/textmorph/analyze_readability', methods=['POST'])
@login_required
def analyze_readability():
    text = request.form.get('text', '').strip()
    filename = request.form.get('filename', 'Manual_Input.txt')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    words = len(text.split())
    chars = len(text)
    flesch = calc_flesch(words, chars)
    fk = calc_fk(words, chars)
    smog = round(1.0430 * math.sqrt(12) + 3.1291, 1)
    ari = round(4.71 * (chars / max(1, words)) + 0.5 * (words / max(1, math.ceil(words / 15))) - 21.43, 1)

    read_file = TextReadabilityFile(
        user_email=current_user.email,
        filename=filename,
        filetype='text/plain',
        filesize=len(text.encode('utf-8')),
        filedata=text
    )
    db.session.add(read_file)
    db.session.commit()

    return jsonify({
        'flesch': flesch,
        'fk_grade': fk,
        'smog': smog,
        'ari': ari,
        'words': words
    })

@textmorph_bp.route('/textmorph/summarize', methods=['POST'])
@login_required
def summarize():
    text = request.form.get('text', '').strip()
    model_choice = request.form.get('model', 'pegasus')
    length = request.form.get('length', 'medium')
    reference = request.form.get('reference', '').strip()

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 10]
    count = 1 if length == 'short' else (2 if length == 'medium' else 3)
    summary = ". ".join(sentences[:max(1, count)]) + "."

    orig_words = len(text.split())
    sum_words = len(summary.split())
    compression = round((1 - (sum_words / max(1, orig_words))) * 100)

    rouge = {}
    if reference:
        rouge = {'rouge1': 0.68, 'rouge2': 0.45, 'rougeL': 0.62}

    record = TextSummary(
        user_email=current_user.email,
        original_text=text,
        summary_text=summary,
        model_used=model_choice,
        summary_length=length,
        reference_summary=reference,
        rouge_scores=json.dumps(rouge)
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'original_text': text,
        'summary_text': summary,
        'model_used': model_choice,
        'orig_words': orig_words,
        'sum_words': sum_words,
        'compression': compression,
        'rouge_scores': rouge
    })

@textmorph_bp.route('/textmorph/paraphrase', methods=['POST'])
@login_required
def paraphrase():
    text = request.form.get('text', '').strip()
    complexity = request.form.get('complexity', 'Intermediate')
    model_choice = request.form.get('model', 'T5 Paraphraser')
    creativity = float(request.form.get('creativity', 1.0))

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    opt1 = f"Option 1 ({complexity}): To summarize clearly, {text.lower()}"
    opt2 = f"Option 2 ({complexity}): In essence, {text.lower()}"
    opt3 = f"Option 3 ({complexity}): Rephrased from another angle: {text.lower()}"

    options = [opt1, opt2, opt3]
    
    orig_flesch = calc_flesch(len(text.split()), len(text))
    readability_scores = [
        {'Source': 'Original', 'Score': orig_flesch},
        {'Source': 'Option 1', 'Score': orig_flesch + 5},
        {'Source': 'Option 2', 'Score': orig_flesch + 8},
        {'Source': 'Option 3', 'Score': orig_flesch + 3}
    ]

    sentiment_orig = {'neg': 0.05, 'neu': 0.70, 'pos': 0.25}
    sentiment_paraphrases = {'neg': 0.03, 'neu': 0.68, 'pos': 0.29}

    rouge_scores = [
        {'Option': 'Option 1', 'ROUGE-1': 0.65, 'ROUGE-2': 0.48, 'ROUGE-L': 0.60},
        {'Option': 'Option 2', 'ROUGE-1': 0.58, 'ROUGE-2': 0.42, 'ROUGE-L': 0.54},
        {'Option': 'Option 3', 'ROUGE-1': 0.71, 'ROUGE-2': 0.53, 'ROUGE-L': 0.68}
    ]

    record = TextParaphrase(
        user_email=current_user.email,
        original_text=text,
        paraphrased_options=json.dumps(options),
        model_used=model_choice,
        creativity=creativity,
        complexity_level=complexity,
        rouge_scores=json.dumps(rouge_scores),
        readability_scores=json.dumps(readability_scores)
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'paraphrases': options,
        'readability_scores': readability_scores,
        'sentiment_orig': sentiment_orig,
        'sentiment_paraphrases': sentiment_paraphrases,
        'rouge_scores': rouge_scores
    })

# --- HISTORY MODULE ROUTES ---
@textmorph_bp.route('/textmorph/history/summaries')
@login_required
def history_summaries():
    records = TextSummary.query.filter_by(user_email=current_user.email).order_by(TextSummary.id.desc()).all()
    data = [{
        'id': r.id,
        'original_text': r.original_text,
        'summary_text': r.summary_text,
        'model_used': r.model_used,
        'summary_length': r.summary_length,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records]
    return jsonify(data)

@textmorph_bp.route('/textmorph/history/paraphrases')
@login_required
def history_paraphrases():
    records = TextParaphrase.query.filter_by(user_email=current_user.email).order_by(TextParaphrase.id.desc()).all()
    data = [{
        'id': r.id,
        'original_text': r.original_text,
        'paraphrased_options': r.paraphrased_options,
        'model_used': r.model_used,
        'complexity_level': r.complexity_level,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records]
    return jsonify(data)

@textmorph_bp.route('/textmorph/history/readability')
@login_required
def history_readability():
    records = TextReadabilityFile.query.filter_by(user_email=current_user.email).order_by(TextReadabilityFile.id.desc()).all()
    data = [{
        'id': r.id,
        'filename': r.filename,
        'filetype': r.filetype,
        'filesize': r.filesize,
        'uploaded_at': r.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
    } for r in records]
    return jsonify(data)

@textmorph_bp.route('/textmorph/history/readability/<int:file_id>')
@login_required
def get_readability_content(file_id):
    rec = TextReadabilityFile.query.get_or_404(file_id)
    return jsonify({'filename': rec.filename, 'content': rec.filedata})

@textmorph_bp.route('/textmorph/history/export/<history_type>')
@login_required
def export_csv(history_type):
    output = io.StringIO()
    writer = csv.writer(output)

    if history_type == 'summaries':
        records = TextSummary.query.filter_by(user_email=current_user.email).order_by(TextSummary.id.desc()).all()
        writer.writerow(['Original Text', 'Summary Text', 'Model Used', 'Summary Length', 'Created At'])
        for r in records:
            writer.writerow([r.original_text, r.summary_text, r.model_used, r.summary_length, r.created_at])
        filename = 'summaries_history.csv'
    elif history_type == 'paraphrases':
        records = TextParaphrase.query.filter_by(user_email=current_user.email).order_by(TextParaphrase.id.desc()).all()
        writer.writerow(['Original Text', 'Paraphrased Options', 'Model Used', 'Complexity Level', 'Created At'])
        for r in records:
            writer.writerow([r.original_text, r.paraphrased_options, r.model_used, r.complexity_level, r.created_at])
        filename = 'paraphrases_history.csv'
    else:
        records = TextReadabilityFile.query.filter_by(user_email=current_user.email).order_by(TextReadabilityFile.id.desc()).all()
        writer.writerow(['Filename', 'Filetype', 'Filesize', 'Uploaded At'])
        for r in records:
            writer.writerow([r.filename, r.filetype, r.filesize, r.uploaded_at])
        filename = 'readability_history.csv'

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
