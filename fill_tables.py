import sqlite3
import os
import random
from faker import Faker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

db_instance = os.getenv("DB_INSTANCE")
fake = Faker()

def insert_dummy_data():
    conn = sqlite3.connect(db_instance)
    cursor = conn.cursor()

    # Insérer des utilisateurs factices
    users = []
    for _ in range(10):  # 10 utilisateurs factices
        last_name = fake.last_name()
        first_name = fake.first_name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d')
        email = fake.unique.email()
        phone = fake.unique.phone_number()
        address = fake.address().replace("\n", ", ")
        zip_code = fake.postcode()
        city = fake.city()
        spoken_languages = ",".join(fake.random_elements(elements=["French", "English", "Spanish", "German"], length=random.randint(1, 3), unique=True))
        avatar_url = fake.image_url()
        boat_license_number = str(fake.random_int(10000000, 99999999))  # 8 chiffres
        insurance_number = str(fake.random_int(100000000000, 999999999999))  # 12 chiffres
        password = fake.password()

        cursor.execute('''INSERT INTO users (lastName, firstName, birth_date, email, phone, address, zip_code, city, spoken_languages, avatar_url, boat_license_number, insurance_number, password)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       (last_name, first_name, birth_date, email, phone, address, zip_code, city, spoken_languages, avatar_url, boat_license_number, insurance_number, password))
        users.append(cursor.lastrowid)  # Stocker les ID insérés

    # Insérer des bateaux factices
    boats = []
    boat_types = ["Yacht", "Fishing Boat", "Speedboat", "Sailboat"]
    for _ in range(5):  # 5 bateaux factices
        name = fake.word().capitalize() + " " + fake.word().capitalize()
        type_boat = random.choice(boat_types)
        capacity = random.randint(2, 10)
        location = fake.city()
        owner_id = random.choice(users)

        cursor.execute('''INSERT INTO boats (name, type, capacity, location, owner_id)
                          VALUES (?, ?, ?, ?, ?)''', 
                       (name, type_boat, capacity, location, owner_id))
        boats.append(cursor.lastrowid)

    # Insérer des sorties de pêche factices
    fishing_trips = []
    fishing_types = ["Deep-sea", "Fly Fishing", "Shore Fishing", "Spearfishing"]
    for _ in range(8):  # 8 sorties de pêche factices
        date = fake.date_between(start_date="-1y", end_date="today").strftime('%Y-%m-%d')
        location = fake.city()
        fishing_type = random.choice(fishing_types)
        boat_id = random.choice(boats)

        cursor.execute('''INSERT INTO fishing_trips (date, location, fishing_type, boat_id)
                          VALUES (?, ?, ?, ?)''', 
                       (date, location, fishing_type, boat_id))
        fishing_trips.append(cursor.lastrowid)

    # Insérer des réservations factices
    for _ in range(15):  # 15 réservations factices
        user_id = random.choice(users)
        fishing_trip_id = random.choice(fishing_trips)
        status = random.choice(['pending', 'confirmed', 'canceled'])

        cursor.execute('''INSERT INTO reservations (user_id, fishing_trip_id, status)
                          VALUES (?, ?, ?)''', 
                       (user_id, fishing_trip_id, status))

    # Insérer des logs de pêche factices
    fish_types = ["Salmon", "Tuna", "Trout", "Bass", "Mackerel", "Cod"]
    for _ in range(20):  # 20 entrées de journal de pêche
        fishing_trip_id = random.choice(fishing_trips)
        fish_type = random.choice(fish_types)
        quantity = random.randint(1, 5)

        cursor.execute('''INSERT INTO fishing_logs (fishing_trip_id, fish_type, quantity)
                          VALUES (?, ?, ?)''', 
                       (fishing_trip_id, fish_type, quantity))

    # Insérer des pages de journaux de pêche factices
    for _ in range(10):  # 10 pages de journaux de pêche
        user_id = random.choice(users)
        title = fake.sentence(nb_words=6)
        content = fake.text(max_nb_chars=200)

        cursor.execute('''INSERT INTO fishing_logs_pages (user_id, title, content)
                          VALUES (?, ?, ?)''', 
                       (user_id, title, content))

    conn.commit()
    conn.close()
    print("Données factices insérées avec succès!")

if __name__ == "__main__":
    insert_dummy_data()
