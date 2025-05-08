from flask import Flask, render_template, session, redirect, url_for
from routes.auth_routes import auth_routes
from routes.crud_routes import crud_routes
from routes.admin_routes import admin_routes
from routes.trend_routes import trend_routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Public Routes
@app.route('/')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login_page'))
    return render_template('home.html')

@app.route('/trends')
def trends():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login_page'))
    return render_template('trends.html')

@app.route('/predict')
def predict():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login_page'))
    return render_template('predict.html')

# Register blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(crud_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(trend_routes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
