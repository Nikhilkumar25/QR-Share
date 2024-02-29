from flask import Flask, render_template, request, send_file, make_response
from io import BytesIO
import qrcode
import base64 # Import the base64 module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            img = qrcode.make(link)
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            # Use base64 to encode the image for embedding in HTML
            img_url = f'data:image/png;base64,{base64.b64encode(img_io.getvalue()).decode()}'
            return render_template('index.html', img_url=img_url)
    return render_template('index.html')

@app.route('/download/<path:path>')
def download(path):
    img_io = BytesIO()
    img = qrcode.make(path)
    img.save(img_io, 'PNG')
    img_io.seek(0)
    response = make_response(img_io.getvalue())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename='qrcode.png')
    return response

if __name__ == '__main__':
    app.run(debug=True)

