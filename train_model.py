import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Cargar los datos de Pokémon
df = pd.read_csv('data/pokemons.csv')

# Supongamos que tenemos un DataFrame `battles` con el siguiente formato:
# | pokemon1 | pokemon2 | winner |
# |----------|----------|--------|
# | Bulbasaur| Ivysaur  | Ivysaur|

battles = pd.read_csv('data/battles.csv')

# Combinar las estadísticas de ambos Pokémon en una sola fila
def get_features(row):
    p1 = df[df['dexnum'] == row['pokemon1']].iloc[0]
    p2 = df[df['dexnum'] == row['pokemon2']].iloc[0]
    return pd.Series({
        'hp1': p1['hp'], 'attack1': p1['attack'], 'defense1': p1['defense'],
        'sp_atk1': p1['sp_atk'], 'sp_def1': p1['sp_def'], 'speed1': p1['speed'],
        'hp2': p2['hp'], 'attack2': p2['attack'], 'defense2': p2['defense'],
        'sp_atk2': p2['sp_atk'], 'sp_def2': p2['sp_def'], 'speed2': p2['speed']
    })

# Aplicar la función a cada fila del DataFrame
features = battles.apply(get_features, axis=1)

# Crear la columna de etiquetas (1 si el ganador es pokemon1, 0 si es pokemon2)
labels = (battles['winner'] == battles['pokemon1']).astype(int)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Entrenar el modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Guardar el modelo
joblib.dump(model, 'model/pokemon_battle_model.pkl')

# Evaluar el modelo
accuracy = model.score(X_test, y_test)
print(f'Accuracy: {accuracy}')
