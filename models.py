# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # Relationship: One Episode has many Appearances
    # cascade="all, delete-orphan" ensures if Episode is deleted, appearances go too.
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    
    # Association proxy (optional but helpful, though not strictly required by prompt)
    guests = association_proxy('appearances', 'guest')

    # Serialization rules to prevent infinite recursion
    # We want to see appearances, but inside appearances, we don't want to see the episode again.
    serialize_rules = ('-appearances.episode',)
  
    def __repr__(self):
        return f'<Episode {self.id} {self.number}>'


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    # Relationship: One Guest has many Appearances
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')
    
    episodes = association_proxy('appearances', 'episode')

    # Serialize rules: inside appearances, don't show the guest again
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.id} {self.name}>'


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign Keys
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')

    # Serialize rules: We want to see the guest and episode details when we look at an appearance
    serialize_rules = ('-episode.appearances', '-guest.appearances')

    # Validation: Rating must be between 1 and 5
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= int(rating) <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def __repr__(self):
        return f'<Appearance {self.id} Rating: {self.rating}>'