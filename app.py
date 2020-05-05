from flask import Flask , render_template , redirect , url_for , request 
from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField 
from wtforms.validators import InputRequired


# Flask app initialisation
app = Flask(__name__)

# take cofiguration from config.cfg
app.config.from_pyfile('config.cfg')


class SearchBarre(FlaskForm):
    sbarre = StringField(validators=[InputRequired()])
    submit = SubmitField('Search')

@app.route('/')
def home():
    form = SearchBarre()
    weather = "flurries"
    return render_template('index.html', weather=weather , form=form)



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True , debug=True , port=5000)
