from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
from datetime import datetime
from app.models import db, WeatherData
import os

weather_bp = Blueprint('weather', __name__)


OPENWEATHER_API_KEY = "50b0d05643a2bf7b3d43f6b55f33286f"

@weather_bp.route('/weather', methods=['GET'])
@jwt_required()
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    try:
        weather_data = fetch_weather_from_api(lat, lon)  # your current API fetch function
        save_weather_to_db(weather_data)  # function to save to DB
        return jsonify(weather_data)

    except Exception as api_error:
        # Log API failure
        print(f"API fetch failed: {api_error}")

        try:
            # Pull the most recent weather data from the DB
            latest = WeatherData.query.order_by(WeatherData.date_recorded.desc()).first()

            if latest:
                return jsonify({
                    'location': latest.county,
                    'temperature': latest.temperature,
                    'humidity': latest.humidity,
                    'wind_speed': latest.wind_speed,
                    'date': latest.date_recorded.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return jsonify({'error': 'No weather data available in database.'}), 500

        except Exception as db_error:
            print(f"DB fallback failed: {db_error}")
            return jsonify({'error': 'Unable to retrieve weather data.'}), 500
