#from app import create_app

#app = create_app()

#if __name__ == "__main__":
 #   app.run(debug=True)


from flask import Flask, render_template
#import os

# Create Flask application instance
app = Flask(__name__, template_folder="templates")


# A simple signup route to test rendering the template
@app.route('/signup', methods=['GET'])
def signup():
     # Render the signup.html template
    return render_template('signup.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('index.html')


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
