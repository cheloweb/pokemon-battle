from flask import Flask, render_template, request, jsonify
from flask_babel import Babel, gettext
import pandas as pd
import pickle
import os
import joblib

app = Flask(__name__)

# Configuración de Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
babel = Babel(app)

# Cargar datos de Pokémon
pokemon_df = pd.read_csv('data/pokemons.csv')

# Cargar modelo de predicción
model_path = 'model/pokemon_battle_model.pkl'
model = joblib.load(model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_pokemons', methods=['GET'])
def get_all_pokemons():
    pokemons = pokemon_df['name'].tolist()
    return jsonify(pokemons)

@app.route('/get_pokemon_info', methods=['POST'])
def get_pokemon_info():
    name = request.json['name']
    pokemon = pokemon_df[pokemon_df['name'] == name].iloc[0]
    pokemon_info = {
        'Name': str(pokemon['name']),
        'Generation': int(pokemon['generation']),
        'Type': str(pokemon['type1']) + (' / ' + str(pokemon['type2']) if pd.notna(pokemon['type2']) else ''),
        'Height': float(pokemon['height']),
        'Weight': float(pokemon['weight']),
        'HP': int(pokemon['hp'])
    }
    return jsonify(pokemon_info)

@app.route('/predict_winner', methods=['POST'])
def predict_winner():
    data = request.get_json()
    pokemon1 = data['pokemon1']
    pokemon2 = data['pokemon2']

    # Obtener características
    p1 = pokemon_df[pokemon_df['name'] == pokemon1].iloc[0]
    p2 = pokemon_df[pokemon_df['name'] == pokemon2].iloc[0]

    features = pd.DataFrame([{
        'hp1': p1['hp'], 'attack1': p1['attack'], 'defense1': p1['defense'],
        'sp_atk1': p1['sp_atk'], 'sp_def1': p1['sp_def'], 'speed1': p1['speed'],
        'hp2': p2['hp'], 'attack2': p2['attack'], 'defense2': p2['defense'],
        'sp_atk2': p2['sp_atk'], 'sp_def2': p2['sp_def'], 'speed2': p2['speed']
    }])

    # Realizar la predicción
    winner = model.predict(features)[0]
    winner_name = pokemon1 if winner == 1 else pokemon2

    return jsonify({'winner': winner_name})

if __name__ == '__main__':
    app.run(debug=True)
