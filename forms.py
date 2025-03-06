from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class SignUpForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()], render_kw={"autocomplete": "off"})
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Register")


class SignInForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()], render_kw={"autocomplete": "off"})
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log in")
    
    
class EnlistBookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    authors = StringField("Authors", validators=[DataRequired()])
    description = TextAreaField("Brief Description", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()], choices=[
        ('', 'Select a Category'),
        ('Computer Science', 'Computer Science'),
        ('law', 'Law'),
        ('Economics', 'Economics'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Medicine and Surgery', 'Medicine and Surgery'),
        ('Artificial Intelligence and Robotics', 'Artificial Intelligence and Robotics'),
        ('Data Science', 'Data Science'),
        ('Mathematics', 'Mathematics'),
        ('other', 'Other')
    ])
    other_category = StringField("Specify Other Category")
    book_format = SelectField("Book Format", validators=[DataRequired()], choices=[
        ('', 'Select a Format'),
        ('hard_copy', 'Hard Copy'),
        ('soft_copy', 'Soft Copy')
    ])
    location = StringField("Location Name", validators=[DataRequired()])
    cover_img = StringField("Enter Book Thumbnail URL", validators=[DataRequired()])
    ratings = SelectField("Ratings", validators=[DataRequired()], choices=[
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
    ])
    submit = SubmitField("Submit Post")
    
   
