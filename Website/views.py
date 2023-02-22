from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Book, Author, User
from .schemas import BookSchema
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
        print(authors)
        available=request.form.get('available')
        for item in request.form.items():
            if not item[1]:
                flash(f'missing required field "{item[0].capitalize()}"', category='error')
        if all(request.form.values()):
            new_book=Book(title=title, available=available)
            books=Book.query.all()
            if books:
                book_id=books[-1].id+1
            else:
                book_id=1
            for item in authors.strip().split(','):
                author=Author(name=item.strip(), book=book_id)
                if author not in [author.name for author in Author.query.all()]:
                    db.session.add(author)
            db.session.add(new_book)
            db.session.commit()
            flash(f'book added (Title:{new_book.title})')
            books=Book.query.all()
            for book in books:
                print(book_id)
            books_list=[]
            for book in books:
                books_list.append(BookSchema(book))
            return render_template('home.html', books=books_list, books_no=len(books))
    return render_template('add.html')

@views.route('/edit', methods=['GET', 'POST'])

def edit():
    if request.method=='POST':
        book_id=request.form.get('id')
        new_title=request.form.get('title')
        new_authors=request.form.get('authors')
        new_available=request.form.get('available')
        book=Book.query.get(book_id)
        if book:
            book=Book.query.get(book_id)
            db.session.delete(book)
            db.session.commit()
        new_book=Book(title=new_title, available=new_available)
        db.session.add(new_book)
        db.session.commit()
        books=Book.query.all()
        new_book=books[-1]
        book_id=new_book.id
        for item in new_authors.strip().split(','):
            author=Author(name=item.strip(), book=book_id)
            db.session.add(author)               
        db.session.commit()
        flash(f'book updated ({new_title})')
        return home()
    else:
        book=None
        if request.args:
            book=BookSchema(Book.query.get(request.args['id']))
        return render_template('edit.html', book=book)
    
@views.route('/lend', methods=['GET', 'POST'])

def lend():
    if request.method=='POST':
        new_id=request.form.get('id')
        new_available=request.form.get('available')
        new_user=request.form.get('user')
        book=Book.query.get(new_id)
        if book:
            book=Book.query.get(new_id)
            user=User(name=new_user, book=new_id)
            if new_user not in [user.name for user in User.query.all()]:
                book.available=new_available
                db.session.add(user)
                db.session.commit()
                flash(f'book lent ({book.title} -> {new_user})')
            else:
                flash('user already has another book')
        return home()
    else:
        book=None
        if request.args:
            book=BookSchema(Book.query.get(request.args['id']))
        return render_template('lend.html', book=book)
    
@views.route('/return', methods=['GET', 'POST'])

def return_book():
    new_id=request.args['id']
    new_user=request.args['user']
    book=Book.query.get(new_id)
    if book:
        book=Book.query.get(new_id)
        book.available='on'
        if new_user:
            user=User.query.get(new_user)
            db.session.delete(user)
        db.session.commit()
        flash('book returned')
    else:
        flash('something wrong!')
    return redirect(url_for('views.home'))


