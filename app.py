from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for, render_template
from flask_cors import CORS
import requests
import json
import os
import logging
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = 'your-secret-key-here'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenWeatherMap API Configuration
API_KEY = "dca478dcafaad5fd0beff0f1f4a33752"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_API_KEY = "dca478dcafaad5fd0beff0f1f4a33752"

# World locations dictionary with coordinates
world_locations = {
    # North America
    "New York, USA": {"lat": 40.7128, "lon": -74.0060},
    "Los Angeles, USA": {"lat": 34.0522, "lon": -118.2437},
    "Chicago, USA": {"lat": 41.8781, "lon": -87.6298},
    "Toronto, Canada": {"lat": 43.6532, "lon": -79.3832},
    "Vancouver, Canada": {"lat": 49.2827, "lon": -123.1207},
    "Mexico City, Mexico": {"lat": 19.4326, "lon": -99.1332},

    # South America
    "Rio de Janeiro, Brazil": {"lat": -22.9068, "lon": -43.1729},
    "Buenos Aires, Argentina": {"lat": -34.6037, "lon": -58.3816},
    "Lima, Peru": {"lat": -12.0464, "lon": -77.0428},
    "Santiago, Chile": {"lat": -33.4489, "lon": -70.6693},
    "Bogota, Colombia": {"lat": 4.7110, "lon": -74.0721},

    # Europe
    "London, UK": {"lat": 51.5074, "lon": -0.1278},
    "Paris, France": {"lat": 48.8566, "lon": 2.3522},
    "Berlin, Germany": {"lat": 52.5200, "lon": 13.4050},
    "Rome, Italy": {"lat": 41.9028, "lon": 12.4964},
    "Madrid, Spain": {"lat": 40.4168, "lon": -3.7038},
    "Amsterdam, Netherlands": {"lat": 52.3676, "lon": 4.9041},
    "Moscow, Russia": {"lat": 55.7558, "lon": 37.6173},
    "Stockholm, Sweden": {"lat": 59.3293, "lon": 18.0686},
    "Athens, Greece": {"lat": 37.9838, "lon": 23.7275},

    # Asia
    "Tokyo, Japan": {"lat": 35.6762, "lon": 139.6503},
    "Beijing, China": {"lat": 39.9042, "lon": 116.4074},
    "Shanghai, China": {"lat": 31.2304, "lon": 121.4737},
    "Seoul, South Korea": {"lat": 37.5665, "lon": 126.9780},
    "Mumbai, India": {"lat": 19.0760, "lon": 72.8777},
    "Delhi, India": {"lat": 28.6139, "lon": 77.2090},
    "Bangkok, Thailand": {"lat": 13.7563, "lon": 100.5018},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Dubai, UAE": {"lat": 25.2048, "lon": 55.2708},
    "Istanbul, Turkey": {"lat": 41.0082, "lon": 28.9784},

    # Africa
    "Cairo, Egypt": {"lat": 30.0444, "lon": 31.2357},
    "Lagos, Nigeria": {"lat": 6.5244, "lon": 3.3792},
    "Nairobi, Kenya": {"lat": -1.2921, "lon": 36.8219},
    "Cape Town, South Africa": {"lat": -33.9249, "lon": 18.4241},
    "Johannesburg, South Africa": {"lat": -26.2041, "lon": 28.0473},
    "Casablanca, Morocco": {"lat": 33.5731, "lon": -7.5898},

    # Oceania
    "Sydney, Australia": {"lat": -33.8688, "lon": 151.2093},
    "Melbourne, Australia": {"lat": -37.8136, "lon": 144.9631},
    "Brisbane, Australia": {"lat": -27.4705, "lon": 153.0260},
    "Auckland, New Zealand": {"lat": -36.8509, "lon": 174.7645},
    "Wellington, New Zealand": {"lat": -41.2866, "lon": 174.7756},

    # India (Additional major cities)
    "Bangalore, India": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad, India": {"lat": 17.3850, "lon": 78.4867},
    "Chennai, India": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata, India": {"lat": 22.5726, "lon": 88.3639},
    "Pune, India": {"lat": 18.5204, "lon": 73.8567},
    "Ahmedabad, India": {"lat": 23.0225, "lon": 72.5714},
    "Tumkur, India": {"lat": 13.3379, "lon": 77.1173},
    
    # Additional Major World Cities
    "Vienna, Austria": {"lat": 48.2082, "lon": 16.3738},
    "Brussels, Belgium": {"lat": 50.8503, "lon": 4.3517},
    "São Paulo, Brazil": {"lat": -23.5505, "lon": -46.6333},
    "Montreal, Canada": {"lat": 45.5017, "lon": -73.5673},
    "Prague, Czech Republic": {"lat": 50.0755, "lon": 14.4378},
    "Copenhagen, Denmark": {"lat": 55.6761, "lon": 12.5683},
    "Helsinki, Finland": {"lat": 60.1699, "lon": 24.9384},
    "Frankfurt, Germany": {"lat": 50.1109, "lon": 8.6821},
    "Hong Kong": {"lat": 22.3193, "lon": 114.1694},
    "Jakarta, Indonesia": {"lat": -6.2088, "lon": 106.8456},
    "Tel Aviv, Israel": {"lat": 32.0853, "lon": 34.7818},
    "Milan, Italy": {"lat": 45.4642, "lon": 9.1900},
    "Osaka, Japan": {"lat": 34.6937, "lon": 135.5023},
    "Kuwait City, Kuwait": {"lat": 29.3759, "lon": 47.9774},
    "Kuala Lumpur, Malaysia": {"lat": 3.1390, "lon": 101.6869},
    "Manila, Philippines": {"lat": 14.5995, "lon": 120.9842},
    "Warsaw, Poland": {"lat": 52.2297, "lon": 21.0122},
    "Lisbon, Portugal": {"lat": 38.7223, "lon": -9.1393},
    "Doha, Qatar": {"lat": 25.2854, "lon": 51.5310},
    "Riyadh, Saudi Arabia": {"lat": 24.7136, "lon": 46.6753},
    "Barcelona, Spain": {"lat": 41.3851, "lon": 2.1734},
    "Geneva, Switzerland": {"lat": 46.2044, "lon": 6.1432},
    "Zurich, Switzerland": {"lat": 47.3769, "lon": 8.5417},
    "Taipei, Taiwan": {"lat": 25.0330, "lon": 121.5654},
    "Abu Dhabi, UAE": {"lat": 24.4539, "lon": 54.3773},
    "Ho Chi Minh City, Vietnam": {"lat": 10.8231, "lon": 106.6297}
}

# Sample data for recommendations
recommendations = [
    {
        "title": "Recommendation 1",
        "image": "static/images/recommendation1.jpg",  # Path to your image
        "description": "Description of recommendation 1."
    },
    {
        "title": "Recommendation 2",
        "image": "static/images/recommendation2.jpg",
        "description": "Description of recommendation 2."
    },
    # Add more recommendations as needed
]

@app.route('/get_locations', methods=['GET'])
def get_locations():
    """Return the list of available locations"""
    return jsonify(list(world_locations.keys()))

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    location = data.get('location')
    
    if location not in world_locations:
        return jsonify({'error': 'Location not found'}), 404
        
    coords = world_locations[location]
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        if weather_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
        
        return jsonify({
            'weather': {
                'condition': weather_data['weather'][0]['main'],
                'temperature': weather_data['main']['temp']
            }
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Weather API error: {str(e)}'}), 500

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if not all(k in data for k in ['username', 'password', 'age', 'gender']):
            return jsonify({'error': 'Missing required fields'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            password=hashed_password,
            age=int(data['age']),
            gender=data['gender']
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 401

        if not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid password'}), 401

        session['user_id'] = user.id
        return jsonify({
            'message': 'Login successful',
            'user': {
                'username': user.username,
                'age': user.age,
                'gender': user.gender
            }
        })
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/user')
def get_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'username': user.username,
        'age': user.age,
        'gender': user.gender
    })

@app.route('/api/recommendations', methods=['POST'])
def recommend():
    """Get product recommendations based on weather."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        location = data.get('location')
        weather_condition = data.get('weather', '').lower()
        temperature = float(data.get('temperature', 20))

        # Define recommendations based on weather
        recommendations = {
            'rain': [
                {"name": "Umbrella", "price": 19.99, "image": "https://images.unsplash.com/photo-1558181048-e7631fe070a7?w=400"},
                {"name": "Rain Boots", "price": 39.99, "image": "https://images.unsplash.com/photo-1541726260-e6b6a6a08b27?w=400"},
                {"name": "Raincoat", "price": 49.99, "image": "https://images.unsplash.com/photo-1521223619409-8c925ee108eb?w=400"}
            ],
            'clear': [
                {"name": "Sunglasses", "price": 24.99, "image": "https://images.unsplash.com/photo-1577803645773-f96470509666?w=400"},
                {"name": "Sun Hat", "price": 19.99, "image": "https://images.unsplash.com/photo-1521223619409-8c925ee108eb?w=400"},
                {"name": "Sunscreen", "price": 15.99, "image": "https://images.unsplash.com/photo-1521223619409-8c925ee108eb?w=400"}
            ],
            'clouds': [
                {"name": "Light Jacket", "price": 45.99, "image": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400"},
                {"name": "Sweater", "price": 34.99, "image": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=400"},
                {"name": "Scarf", "price": 19.99, "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf9b0f?w=400"}
            ]
        }

        # Default products for unknown weather conditions
        default_products = [
            {"name": "Comfortable Clothes", "price": 29.99, "image": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=400"},
            {"name": "All-Weather Shoes", "price": 49.99, "image": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400"},
            {"name": "Versatile Jacket", "price": 59.99, "image": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400"}
        ]

        # Get weather-specific products
        weather_products = recommendations.get(weather_condition, default_products)

        # Get additional products based on temperature
        if temperature < 20:
            additional_products = [
                {"name": "Warm Jacket", "price": 59.99, "image": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400"},
                {"name": "Warm Socks", "price": 9.99, "image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400"}
            ]
        else:
            additional_products = [
                {"name": "T-Shirt", "price": 19.99, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"},
                {"name": "Shorts", "price": 24.99, "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400"}
            ]

        response_data = {
            'location': location,
            'weather': {
                'condition': weather_condition,
                'temperature': temperature
            },
            'recommendations': {
                'weather_products': weather_products,
                'additional_products': additional_products
            }
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    if 'user_id' not in session:
        return jsonify({"error": "User not logged in"}), 401

    try:
        data = request.get_json()
        if not data or 'location' not in data:
            return jsonify({"error": "Location is required"}), 400

        # Get user information
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Get weather data
        try:
            weather_data = requests.get(WEATHER_URL, params={"q": data['location'], "appid": API_KEY, "units": "metric"}).json()
            weather_condition = weather_data['weather'][0]['main']
            temperature = weather_data['main']['temp']
        except Exception as e:
            return jsonify({"error": "Weather service error", "details": str(e)}), 503

        # Load and filter weather-based recommendations
        recommendations = {
            "rain": [
                {"name": "Umbrella", "price": 10.99, "image": "https://images.unsplash.com/photo-1558181048-e7631fe070a7?w=400"},
                {"name": "Raincoat", "price": 50.99, "image": "https://images.unsplash.com/photo-1521223619409-8c925ee108eb?w=400"}
            ],
            "sunny": [
                {"name": "Sunglasses", "price": 9.99, "image": "https://images.unsplash.com/photo-1577803645773-f96470509666?w=400"},
                {"name": "Sun cool", "price": 20.99, "image": "https://images.unsplash.com/photo-1521223619409-8c925ee108eb?w=400"}
            ]
        }
        
        category = weather_condition.lower()
        
        weather_products = []
        if category in recommendations:
            weather_products = recommendations[category]
        
        # Get additional products
        additional_products = [
            {"name": "Water bottle", "price": 7.99, "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"},
            {"name": "Snacks", "price": 4.99, "image": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400"}
        ]

        # Combine both sets of recommendations
        all_recommendations = {
            "weather_based": weather_products,
            "additional": additional_products
        }

        response_data = {
            "weather": {
                "condition": weather_condition,
                "temperature": temperature,
                "location": data['location']
            },
            "user": {
                "age": user.age,
                "gender": user.gender
            },
            "recommendations": all_recommendations
        }

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/recommend')
def recommend_data():
    return render_template('recommend.html', recommendations=recommendations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
