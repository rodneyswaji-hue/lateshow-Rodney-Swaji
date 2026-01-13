# 🎬 Late Show API (Flask)

A RESTful API built with **Flask**, **SQLAlchemy**, and **SQLite** to manage Episodes, Guests, and their Appearances on a late-night show.

This project demonstrates:
- Database relationships (one-to-many & many-to-many)
- Model validations
- REST API design
- JSON serialization
- API testing with Postman

---

## 📦 Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- SQLite
- Postman (for API testing)

---

## 📁 Project Structure

```
challenge-4-lateshow/
│
├── server/
│   ├── app.py          # Application routes
│   ├── models.py       # Database models
│   ├── config.py       # App and database configuration
│   ├── seed.py         # Seed data for development
│   └── migrations/     # Database migrations
│
├── instance/
│   └── app.db          # SQLite database
│
├── challenge-4-lateshow.postman_collection.json
├── Pipfile
├── Pipfile.lock
└── README.md
```

---

## 🗄️ Data Models & Relationships

### Episode
- Has many Guests through Appearances

### Guest
- Has many Episodes through Appearances

### Appearance
- Belongs to one Episode
- Belongs to one Guest
- Stores a `rating` (1–5)

### Relationships
- Episode ↔ Guest is **many-to-many**
- Deleting an Episode or Guest **cascades** to delete related Appearances

---

## ✅ Validations

The `Appearance` model enforces:
- `rating` must be **between 1 and 5** (inclusive)

If validation fails, the API returns an error response.

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/rodneyswaji-hue/challenge-4-lateshow.git
cd challenge-4-lateshow
```

### 2️⃣ Install Dependencies
```bash
pipenv install
pipenv shell
```

### 3️⃣ Database Setup
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4️⃣ Seed the Database
```bash
python server/seed.py
```

### 5️⃣ Run the Server
```bash
python server/app.py
```

The API will be available at:
```
http://localhost:5555
```

---

## 🔗 API Endpoints

### GET /episodes
Returns all episodes.

### GET /episodes/:id
Returns a single episode with its appearances and guests.

### DELETE /episodes/:id
Deletes an episode and all associated appearances.

### GET /guests
Returns all guests.

### POST /appearances
Creates a new appearance linking an episode and a guest.

---

## 🧪 Testing with Postman

1. Open **Postman**
2. Click **Import**
3. Upload `challenge-4-lateshow.postman_collection.json`
4. Ensure the Flask server is running
5. Send requests to test endpoints

---

## 🏁 Deliverables Checklist

- ✅ Models implemented with correct relationships
- ✅ Validations added
- ✅ All required routes implemented
- ✅ Cascade deletes configured
- ✅ JSON responses formatted correctly
- ✅ Postman collection works
- ✅ README is complete and well-documented

---

## 👤 Author

**Rodney Swaji**  
GitHub: [rodneyswaji-hue](https://github.com/rodneyswaji-hue)

---

## 📜 License

This project is for educational purposes.
