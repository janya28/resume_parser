from flask import Flask, request, render_template
from docx import Document
import os

app = Flask(__name__)

def parse_resume(file_path):
    document = Document(file_path)
    data = {}
    current_section = None

    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            if text.endswith(':'):
                current_section = text[:-1]
                data[current_section] = []
            elif current_section:
                # Split details into bullet points if multiple lines are present
                points = text.split('. ')
                if len(points) > 1:
                    data[current_section].extend(points)
                else:
                    data[current_section].append(text)

    # Remove empty entries and convert lists of details into bullet points
    data = {k: [p.strip() for p in v if p.strip()] for k, v in data.items()}

    return data

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.docx'):
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            data = parse_resume(file_path)
            os.remove(file_path)  # Clean up the uploaded file

            return render_template('resume.html', data=data)

    return '''
    <!doctype html>
    <title>Upload Resume</title>
    <h1>Upload a Resume</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
