
from flask import Flask
# from routes import contact_routes
from routes.contact_routes import contact_routes 

app = Flask(__name__)
app.register_blueprint(contact_routes)

if __name__ == "__main__":
    app.run(debug=True)