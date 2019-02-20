__author__ = 'olga_danko'
from sklearn.externals import joblib
from flask import Flask, render_template, request
from sentiment_module import *

app = Flask(__name__)

classifier = joblib.load("./ppl.pkl")

@app.route("/", methods=["POST", "GET"])
def index_page(text="", message="", color=""):
    if request.method == "POST":
        text = request.form["text"]
        filtered_text = text_filter([text])
        prediction_class = classifier.predict(filtered_text)[0]
        if (prediction_class == 0):
                message = 'NEGATIVE'
                color = "red"
        else:
            message = 'POSITIVE'
            color = "green"

    return render_template('form.html', text=text, prediction_message=message, color=color)

if __name__ == "__main__":
    app.run(debug=True)



