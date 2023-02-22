from . import db


class Book(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    authors=db.relationship("Author", backref='owner')
    available=db.Column(db.String(20))
    user=db.relationship("User", backref='user')

class Author(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    book=db.Column(db.Integer, db.ForeignKey('book.id'))

    def __str__(self):
        return f'{self.name}'

class User(db.Model):
    name=db.Column(db.String(100), primary_key=True)
    book=db.Column(db.Integer, db.ForeignKey('book.id'))

    def __str__(self):
        return f'{self.name}'