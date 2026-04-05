from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Load data
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Save data
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Restaurant page
@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')

# Add food
@app.route('/add_food', methods=['POST'])
def add_food():
    data = load_data()

    quantity = int(request.form['quantity'])
    if quantity > 20:
        suggestion = "Reduce cooking quantity tomorrow"
    else:
        suggestion = "Good job minimizing waste"

    food = {
        "restaurant": request.form['restaurant'],
        "food": request.form['food'],
        "quantity": quantity,
        "location": request.form.get('location','Not provided'),
        "impact": quantity * 2,
        "badge": "Gold Donor" if quantity > 10 else "Contributor",
        "suggestion" : suggestion
    }

    data.append(food)
    save_data(data)

    return redirect('/ngo')

# NGO page
@app.route('/ngo')
def ngo():
    data = load_data()
    return render_template('ngo.html', foods=data)

@app.route('/leaderboard')
def leaderboard():
    data = load_data()
    sorted_data = sorted(data, key=lambda x: x['impact'], reverse=True)
    return render_template('leaderboard.html', foods=sorted_data)

# Run app
app.run(debug=True)