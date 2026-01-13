# seed.py
from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    print("Deleting existing data...")
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    print("Creating episodes...")
    ep1 = Episode(date="1/11/99", number=1)
    ep2 = Episode(date="1/12/99", number=2)
    db.session.add_all([ep1, ep2])
    db.session.commit()

    print("Creating guests...")
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="Comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")
    db.session.add_all([g1, g2, g3])
    db.session.commit()

    print("Creating appearances...")
    a1 = Appearance(rating=4, episode_id=ep1.id, guest_id=g1.id)
    a2 = Appearance(rating=5, episode_id=ep2.id, guest_id=g3.id)
    db.session.add_all([a1, a2])
    db.session.commit()

    print("Seeding done!")