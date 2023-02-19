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

@views.route('/edit', methods=['GET', 'POST'])

def edit():
    if request.method=='POST':
        new_title=request.form.get('title')
        new_available=request.form.get('available')
        book=Book.query.get(new_title)
        if book:
            book=Book.query.get(new_title)
            book.available=new_available
            db.session.commit()
            flash(f'book updated ({new_title})')
        return home()
    else:
        book=None
        if request.args:
            book=BookSchema(Book.query.get(request.args['title']))
        return render_template('edit.html', book=book)
    
@views.route('/lend', methods=['GET', 'POST'])

def lend():
    if request.method=='POST':
        new_title=request.form.get('title')
        new_available=request.form.get('available')
        new_user=request.form.get('user')
        book=Book.query.get(new_title)
        if book:
            book=Book.query.get(new_title)
            user=User(name=new_user, book=new_title)
            if new_user not in [user.name for user in User.query.all()]:
                book.available=new_available
                db.session.add(user)
                db.session.commit()
                flash(f'book lent ({new_title} -> {new_user})')
            else:
                flash('user already has another book')
        return home()
    else:
        book=None
        if request.args:
            book=BookSchema(Book.query.get(request.args['title']))
        return render_template('lend.html', book=book)
    
@views.route('/return', methods=['GET', 'POST'])

def return_book():
    new_title=request.args['title']
    new_user=request.args['user']
    book=Book.query.get(new_title)
    if book:
        book=Book.query.get(new_title)
        book.available='on'
        user=User.query.get(new_user)
        db.session.delete(user)
        db.session.commit()
        flash('book returned')
    else:
        flash('something wrong!')
    return redirect(url_for('views.home'))


