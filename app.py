import os
from flask import Flask, render_template, request, flash
from decouple import config
import requests

app = Flask(__name__)
app.secret_key = 'some_secret_key'
API_KEY = config('OPEN_WEATHER_API_KEY', default='')
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


def get_temperature_details(celsius: float) -> str:
    if 28 <= celsius <= 32:
        return {'icon': 'melting.png', 'text': 'Certamente, está todo mundo começando a derreter!'}
    elif 32 <= celsius <= 45:
        return {'icon': 'extreme_heat.png', 'text': 'Observamos aqui, uma mostra gràtis do inferno!'}
    elif 10 <= celsius < 16:
        return {'icon': 'extreme_cold.png', 'text': 'A Elsa passou e deixou o LERIGOOU!'}
    elif 16 <= celsius < 20:
        return {'icon': 'moderate_cold.png', 'text': 'Que tal um chocolate quente e Netflix ?'}
    elif 20 <= celsius < 28:
        return {'icon': 'pleasant.png', 'text': 'Levanta da cadeira e vai levar seu Pet pra passear, o clima ta bom pra isso!'}
    else:
        return {'icon': 'default_icon.png', 'text': 'Quem dera se todos os dias fossem assim, não acha ?'}

def get_weather(city: str) -> dict:
    response = requests.get(API_URL.format(city, API_KEY))
    if response.status_code == 200:
        data = response.json()
        kelvin = data['main']['temp']
        celsius = kelvin - 273.15
        temp_details = get_temperature_details(celsius)
        icon_name = temp_details['icon']
        temp_text = temp_details['text']
        
        return {
            'city': data['name'],
            'temperature': "{:.1f}°C".format(celsius),
            'icon': icon_name,
            'temp_text': temp_text,
        }
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash('Por favor, insira o nome de uma cidade', 'warning')
        else:
            weather = get_weather(city)
            if not weather:
                flash('Não foi possível obter a previsão para essa cidade', 'danger')
    else:
        weather = get_weather('Rio de Janeiro')

    return render_template('home.html', weather=weather)

if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)