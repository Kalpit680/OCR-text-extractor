import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import Flask, render_template, request
import easyocr

app = Flask(__name__)

reader = easyocr.Reader(['en'])

@app.route('/', methods=['GET', 'POST'])
def home():

    extracted_text = ""

    if request.method == 'POST':

        file = request.files['image']

        if file:

            filepath = file.filename
            file.save(filepath)

            results = reader.readtext(filepath)

            text_list = []

            for result in results:
                text_list.append(result[1])

            extracted_text = "\n".join(text_list)

            try:
                os.remove(filepath)
            except:
                pass

    return render_template("index.html", extracted_text=extracted_text)


if __name__ == '__main__':
    app.run(debug=True)