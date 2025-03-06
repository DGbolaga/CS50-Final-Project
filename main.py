from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from flask import session
from flask_gravatar import Gravatar
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
import csv 
import os 
import urllib.parse
from urllib.parse import urlencode
import hashlib

from forms import SignInForm, SignUpForm, EnlistBookForm
from helpers import User


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

# Configure gravatar
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='mp',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CREATE DATABASE
db = SQL("sqlite:///books.db")

# CREATE login decorator
@login_manager.user_loader
def load_user(user_id):
    user = db.execute('SELECT * FROM users WHERE user_id = ?', user_id)
    
    if user:
        return User(
            id=user[0]['user_id'],
            name=user[0]['name'],
            email=user[0]['email'],
            password=user[0]['password']
        )
    return None

# custom admin decorator
def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # id must be 1 to continue
        if current_user.id == 1:
            return func(*args, **kwargs)
        else:
            abort(403, 'Must be an admin to delete book!')
    return decorated_function

def load_books_db():
    try: 
        # only run if database is created for the first time.
        book_count = db.execute('SELECT COUNT(*) FROM books')
        
        if book_count[0]['COUNT(*)'] == 0:
            with open('csv_files/updated_books_without_errors.csv', mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'cover_img' in row and row['cover_img']:
                        db.execute('INSERT INTO books (title, authors, description, category, cover_img, location, book_format, ratings, added_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', row['book_title'], row['authors'], row['description'], row['category'], row['cover_img'], row['location'], row['book_format'], row['ratings'], 1)
                print('Books successfully loaded')
        else:
            print("Database already contains books.")
                
    except Exception as e:
        print(f'An error occurred: {e}')
        
 
def get_gravatar_url(email, size=30):
    """Generate Gravatar URL for a given email"""
    # AI assistance: Helped in generating the Gravatar URL logic
    email = email.lower().encode('utf-8')
    email_hash = hashlib.md5(email).hexdigest()
    params = urlencode({'s': str(size), 'd': 'mp'})
    return f'https://www.gravatar.com/avatar/{email_hash}?{params}'
        
@app.template_filter('stars')
def stars(ratings):
    return '⭐' * int(ratings)


def get_map_url(place_name):
    ''' Function to generate the map URL '''
    # AI assistance: Helped in generating function to get map url
    encoded_place = urllib.parse.quote(place_name)
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return f"https://www.google.com/maps/embed/v1/place?q={encoded_place}&zoom=15&key={api_key}"


def fetch_books(searched_book=None, search_by_category=None):
    ''' Function to get book(s) from books database. '''
    # AI assistance: Helped in debugging code

    books_info = []
    
    if searched_book:
        searched_book_lower = searched_book.lower()
        books = db.execute('SELECT * FROM books WHERE LOWER(title) = ?', searched_book_lower)
    elif searched_book is None:
        books = db.execute('SELECT * FROM books ORDER BY RANDOM()')
    if search_by_category:
        books = db.execute('SELECT * FROM books WHERE category = ? ORDER BY RANDOM()', search_by_category)

    for book in books:
        # Fetch seller's email for each book
        seller_email = db.execute('SELECT email FROM users WHERE user_id = ?', book['added_by'])[0]['email']
        
        # Truncate description and author if they exceed the character limit
        description = book['description']
        if len(description) > 22:
            description = description[:22] + '...'

        books_info.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'authors': book['authors'],
            'description': description,
            'category': book['category'],
            'cover_img': book['cover_img'],
            'location': book['location'],
            'gravatar_url': get_gravatar_url(seller_email)
        })
    
    return books_info

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    # AI assistance: Suggested clearing flash messages before logout
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        # AI assistance: Helped in validating user registration logic
        user = db.execute('SELECT * FROM users WHERE email = ?', form.email.data)
        if user:
            flash("You have already registered with that email, Log in instead!")
            return redirect(url_for('login'))

        hash_and_salt_password = generate_password_hash(
            password=form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        # Insert user once and get the ID
        user_id = db.execute('INSERT INTO users (name, password, email) VALUES (?, ?, ?)', form.name.data, hash_and_salt_password, form.email.data)

        new_user = User(
            id=user_id,
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salt_password
        )
        
        login_user(new_user)
        flash('Successfully registered!', 'success')
        
        return redirect(url_for('show_all_books'))
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        user = db.execute('SELECT * FROM users WHERE email = ?', form.email.data)
        
        if not user:
            flash("Email doesn't exist. Try again")
            return redirect(url_for('login'))
        elif not check_password_hash(user[0]['password'], form.password.data):
            flash("Incorrect password. Try again")
            return redirect(url_for('login'))
        else:
            new_user = User(
                id=user[0]['user_id'],
                name=user[0]['name'],
                email=user[0]['email'],
                password=user[0]['password']
            )
            login_user(new_user)
            return redirect(url_for("show_all_books"))
       
    return render_template('login.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/book_details/<int:book_id>')
@login_required
def book_details(book_id):
    id = int(book_id)
    current_book = db.execute('SELECT * FROM books WHERE book_id = ?', id)
    seller_email = db.execute('SELECT * FROM users WHERE user_id = ?', current_book[0]['added_by'])
    book = []
    book.append({
        'book_id': current_book[0]['book_id'],
        'title': current_book[0]['title'],
        'authors': current_book[0]['authors'],
        'description': current_book[0]['description'],
        'location': current_book[0]['location'],
        'category': current_book[0]['category'],
        'cover_img': current_book[0]['cover_img'], 
        'book_format': current_book[0]['book_format'], 
        'ratings': current_book[0]['ratings'],
        'seller_email': seller_email,
        # 'location_url': "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3964.046772803067!2d3.387269773729729!3d6.51576432325581!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x103b8d24c04d3e75%3A0x7347f1a6be13e004!2sUniversity%20of%20Lagos!5e0!3m2!1sen!2sng!4v1735921845473!5m2!1sen!2sng"
        'location_url': get_map_url(current_book[0]['location'])
    })
    
    print(book)
    return render_template('room.html', book=book)

@app.route('/show_all_books', methods=['GET', 'POST'])
@login_required
def show_all_books():    
    # set admin to true if the user is logged in and is an admin
    is_admin = current_user.is_authenticated and current_user.id == 1
    if request.method == 'GET':
        load_books_db()
        categories = db.execute('SELECT DISTINCT category FROM books')
        book_details = fetch_books() 
        return render_template('all_books.html', book_details=book_details, categories=categories, is_admin=is_admin)
    else:
        categories = db.execute('SELECT DISTINCT category FROM books')
        selected_category = request.form.get('selected_category')
        book_details = fetch_books(search_by_category=selected_category)
        return render_template('all_books.html', book_details=book_details, categories=categories, is_admin=is_admin)   
    
@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        searched_book = request.form.get('search')
        if searched_book:
            book_details = fetch_books(searched_book=searched_book)  # Fetch books based on user search
            return render_template('all_books.html', book_details=book_details)

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_books():
    form = EnlistBookForm()
    # AI assistance: Received suggestions for form handling.
    if form.validate_on_submit():
        # Update fieldnames to include 'ratings'
        fieldnames = ['book_title', 'authors', 'description', 'category', 'cover_img', 'location', 'book_format', 'ratings']
        if form.category.data == 'other':
            category = form.other_category.data
        else:
            category =  form.category.data
        with open('csv_files/added_books.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header only if the file is new
            if csvfile.tell() == 0:
                writer.writeheader()
           
            # Fix line breaks.
            description = form.description.data.replace('\n', ' ').replace('\r', ' ')
              
            # Write the form data to the CSV
            writer.writerow({
                'book_title': form.title.data.strip(),
                'authors': form.authors.data.strip(),
                'description': description,
                'category': category,
                'cover_img': form.cover_img.data.strip(),
                'location': form.location.data,
                'book_format': form.book_format.data,
                'ratings': form.ratings.data
            })
            # Write the form to db
            db.execute('INSERT INTO books (title, authors, description, category, cover_img, location, book_format, ratings, added_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', form.title.data.strip(), form.authors.data.strip(), description, category, form.cover_img.data.strip(), form.location.data, form.book_format.data, form.ratings.data, current_user.id)
            flash('Book listed successfully!', 'success')   
        
        return redirect(url_for('show_all_books'))
            
    return render_template('sell.html', form=form)
    

@app.route('/delete_book/<int:book_id>')
@is_admin
@login_required
def delete_book(book_id):
    id = int(book_id)
    current_book = db.execute('SELECT * FROM books WHERE book_id = ?', id)
    
    if current_book:
        fieldnames = ['book_title', 'authors', 'description', 'category', 'cover_img', 'location', 'book_format', 'ratings']
        with open('csv_files/deleted_books.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header only if the file is new
            if csvfile.tell() == 0:
                writer.writeheader()
                
            # Write the form data to the CSV
            writer.writerow({
                'book_title': current_book[0]['title'],
                'authors': current_book[0]['authors'],
                'description': current_book[0]['description'],
                'category': current_book[0]['category'],
                'cover_img': current_book[0]['cover_img'],
                'location': current_book[0]['location'],
                'book_format': current_book[0]['book_format'],
                'ratings': current_book[0]['ratings']
            })
        
        db.execute('DELETE FROM books WHERE book_id = ?', id)
        flash('Book deleted successfully!', 'success')   
        
    return redirect(url_for('show_all_books'))
    

if __name__ == '__main__':
    app.run(debug=True)