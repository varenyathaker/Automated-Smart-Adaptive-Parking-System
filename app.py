from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import sql
import requests

app = Flask(__name__)
GOOGLE_MAPS_API_KEY = 'AIzaSyDqlgjgW4XiLsJM33jY8voBIjGUQswKd_I'

###########################################################################################################
class Routes:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/index', 'index', self.home)
        self.app.add_url_rule('/login', 'login', self.login, methods=['GET', 'POST'])
        self.app.add_url_rule('/signup', 'signup', self.signup, methods=['GET', 'POST'])
        self.app.add_url_rule('/about_us', 'about_us', self.about_us)
        self.app.add_url_rule('/contact_us', 'contact_us', self.contact_us)
        self.app.add_url_rule('/geocode', 'geocode', self.geocode)
        self.app.add_url_rule('/directions', 'directions', self.directions)
        self.app.add_url_rule('/map', 'map', self.map)
        self.app.add_url_rule('/', 'static_files', self.static_files)
        self.app.add_url_rule('/book', 'book', self.book)

    def home(self):
        return render_template('index.html', google_maps_api_key=GOOGLE_MAPS_API_KEY)

    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Check login credentials
            if sql.check_login(username, password):
                return render_template('useracc.html', google_maps_api_key=GOOGLE_MAPS_API_KEY,user_name=username)
            else:
                return "Login failed. Please check your credentials."

        return render_template('login.html')

    def signup(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']  # Adjusted to match the HTML form field name

            # Add user to database
            if sql.add_user(username, password, email, full_name):
                return redirect(url_for('login'))  # Redirect to login page after successful signup
            else:
                return "Failed to sign up. Please try again."

        return render_template('signup.html')

    def about_us(self):
        return render_template('about_us.html')

    def contact_us(self):
        return render_template('contact_us.html')

    def geocode(self):
        address = request.args.get('address')
        data = geocode_address(address, GOOGLE_MAPS_API_KEY)
        return jsonify(data)

    def directions(self):
        start = request.args.get('start')
        end = request.args.get('end')
        data = get_directions(start, end, GOOGLE_MAPS_API_KEY)
        return jsonify(data)

    def map(self):
        return render_template('map.html')

    def static_files(self, filename):
        return send_from_directory(app.static_folder, filename)
    
    def user_account(self):
        # Logic to fetch user data or perform actions related to user account
        return render_template('useracc.html')
    
    def book(self):
        return render_template('book.html')

    



def geocode_address(address, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_directions(start, end, api_key):
    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': start,
        'destination': end,
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.json()

##########################################################################################################
# Instantiate the Routes class
Routes(app)

if __name__ == '__main__':
    app.run(debug=True)







