from flask import Flask , render_template , redirect , url_for 
from flask_wtf import FlaskForm
from wtforms import StringField , SelectField ,SubmitField 
from wtforms.validators import InputRequired
import pyowm
import time 

# Flask app initialisation
app = Flask(__name__)

# take cofiguration from config.cfg
app.config.from_pyfile('config.cfg')

# OWM API and config
api_key = "f8b0c8978211db711199ec4a17834237"
owm_obj = pyowm.OWM(api_key)

# all world wide country code
countryCode = ['af', 'al', 'dz', 'as', 'ad', 'ao', 'ai', 'aq', 'ag', 'ar',
     'am', 'aw', 'au', 'at', 'az', 'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 
     'bj', 'bm', 'bt', 'bo', 'ba', 'bw', 'bv', 'br', 'io', 'bn', 'bg', 'bf', 
     'bi', 'kh', 'cm', 'ca', 'cv', 'ky', 'cf', 'td', 'cl', 'cn', 'cx', 'cc', 'co',
      'km', 'cg', 'ck', 'cr', 'ci', 'hr', 'cu', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 
      'ec', 'eg', 'sv', 'gq', 'er', 'ee', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'fx', 
      'gf', 'pf', 'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gd', 'gp', 
      'gu', 'gt', 'gn', 'gw', 'gy', 'ht', 'hm', 'hn', 'hk', 'hu', 'is', 'in', 'id', 
      'ir', 'iq', 'ie', 'il', 'it', 'jm', 'jp', 'jo', 'kz', 'ke', 'ki', 'kp', 'kr', 
      'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mo', 'mk', 
      'mg', 'mw', 'my', 'mv', 'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'fm', 
      'md', 'mc', 'mn', 'ms', 'ma', 'mz', 'mm', 'na', 'nr', 'np', 'nl', 'an', 'nc',
       'nz', 'ni', 'ne', 'ng', 'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw', 'pa', 'pg', 
       'py', 'pe', 'ph', 'pn', 'pl', 'pt', 'pr', 'qa', 're', 'ro', 'ru', 'rw', 'sh', 
       'kn', 'lc', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'sc', 'sl', 'sg', 'sk',
        'si', 'sb', 'so', 'za', 'es', 'lk', 'sd', 'sr', 'sj', 'sz', 'se', 'ch', 'sy', 
        'tw', 'tj', 'tz', 'th', 'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc', 'tv', 
        'ug', 'ua', 'ae', 'gb', 'us', 'um', 'uy', 'uz', 'vu', 'va', 've', 'vn', 'vg',
         'vi', 'wf', 'eh', 'ye', 'yu', 'zr', 'zm', 'zw']


# Search form by Flask-wtf
class SearchBarre(FlaskForm):
    sbarre = StringField(validators=[InputRequired()])
    country_code = SelectField(u'Country code', choices=[] , validators=[InputRequired()])
    submit = SubmitField('Search')

# Home route /
@app.route('/' , methods=['GET','POST'])
def home():
    form = SearchBarre() # our Form 
    weather_info = {} # empty dictionary for weather info
    index_page = True
    
    form.country_code.choices = [(code.upper() , code.upper())for code in countryCode ]

    if form.validate_on_submit():

        obs_obj = owm_obj.weather_at_place(str(form.sbarre.data)+ ',' + str(form.country_code.data)) # getting the place from user input
        weather = obs_obj.get_weather() # find weather for user input
        city = str(form.sbarre.data) # city name from user input
        index_page = False 
        now = time.strftime('%c')

        weather_info = {
            'timing':str(now),
            'statu' : str(weather.get_status()),
            'detailed-statu': str(weather.get_detailed_status()),
            'temperature':str(weather.get_temperature(unit='celsius')['temp']) + '°',
            'temp-max':str(weather.get_temperature(unit='celsius')['temp_max']) + '°',
            'temp-min':str(weather.get_temperature(unit='celsius')['temp_min']) + '°',
            'humidity': str(weather.get_humidity()) + ' %',
            'pressure': str(weather.get_pressure()['press']) + ' hpa',
            'wind': str(weather.get_wind()['speed']) + ' m/s ',
            'sun-rise': weather.get_sunrise_time(timeformat='iso').split(),
            'sun-set': weather.get_sunset_time(timeformat='iso').split(),
        }

        return render_template('index.html', weather_info = weather_info , city = city ,form=form , index_page = index_page)
    
    return render_template('index.html', weather_info = weather_info , form=form , index_page = index_page)




if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True , debug=True , port=5000)
