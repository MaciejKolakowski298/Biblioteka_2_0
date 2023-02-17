from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, Author, User
from .schemas import BookSchema
import requests
from . import db

views=Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])

def home():
    books=Book.query.all()
    books_list=[]
    for book in books:
        books_list.append(BookSchema(book))
    return render_template('home.html', books=books_list, books_no=len(books))

@views.route('/add', methods=['GET', 'POST'])

def add():
    if request.method=='POST':
        title=request.form.get('title')
        authors=request.form.get('authors')
        available=request.form.get('available')
        for item in request.form.items():
            if not item[1]:
                flash(f'missing reqired field "{item[0].capitalize()}"', category='error')
        if all(request.form.values()):
            new_book=Book(title=title, available=available)
            author=Author(name=authors, book=title)
            db.session.add(author)
            db.session.add(new_book)
            db.session.commit()
            flash(f'book added (Title:{new_book.title})')
            books=Book.query.all()
            books_list=[]
            for book in books:
                books_list.append(BookSchema(book))
            return render_template('home.html', books=books_list, books_no=len(books))
    return render_template('add.html')