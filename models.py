from app import db

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # autres champs...

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'email': self.email
        }

# class Bateau(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(50), nullable=False)
#     capacite = db.Column(db.Integer, nullable=False)
#     # autres champs...

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'nom': self.nom,
#             'capacite': self.capacite
#         }

# class SortiePeche(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.Date, nullable=False)
#     bateau_id = db.Column(db.Integer, db.ForeignKey('bateau.id'), nullable=False)
#     # autres champs...

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'date': self.date,
#             'bateau_id': self.bateau_id
#         }

# class Reservation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sortie_peche_id = db.Column(db.Integer, db.ForeignKey('sortie_peche.id'), nullable=False)
#     utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
#     # autres champs...

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'sortie_peche_id': self.sortie_peche_id,
#             'utilisateur_id': self.utilisateur_id
#         }

# class CarnetPeche(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
#     details = db.Column(db.Text, nullable=False)
#     # autres champs...

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'utilisateur_id': self.utilisateur_id,
#             'details': self.details
#         }
