from wtforms import Form, StringField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField


class RegisterUserForm(Form):
    name = StringField('Nome', [validators.required(), validators.Length(min=4, max=100)])
    organic_unit = SelectField(label='Unidade Orgânica', coerce=int)
    password = PasswordField('Password', [validators.required(), validators.Length(min=1, max=100)])
    contact = StringField('Contacto', [validators.required(), validators.Length(min=4, max=100)])
    address = StringField('Morada', [validators.required(), validators.Length(min=4, max=100)])
    cc = StringField('cc', [validators.required(), validators.Length(min=4, max=10)])
    end_date = DateField('Data de Validade', [validators.required()], format='%Y-%m-%d')
    type = SelectField(label='Tipo', choices=[(1, 'Professor'), (2, 'Funcionário'), (3, 'Estudante')], coerce=int)
