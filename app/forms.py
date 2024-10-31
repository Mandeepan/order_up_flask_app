from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    employee_number = StringField("Employee number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", coerce=int, validators=[DataRequired()])
    servers = SelectField("Servers", coerce=int, validators=[DataRequired()])
    assign = SubmitField("Assign")

class MenuItemAssignmentForm(FlaskForm):
    menu_item_ids = SelectMultipleField("Menu items", coerce=int)
    add_to_order = SubmitField("Add to Order")

class CloseTableForm(FlaskForm):
    close = SubmitField("Close Table")