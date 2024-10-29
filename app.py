from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Bienvenue sur le serveur Flask avec SQLite !"

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing data"}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created", "email": email}), 201


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
