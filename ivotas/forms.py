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


class CreateFacultyForm(Form):
    name = StringField('Nome', [validators.required(), validators.Length(min=1, max=100)])


class ChangeFacultyForm(Form):
    faculty = SelectField(label='Faculdade', coerce=int)
    new_name = StringField('Nome Novo', [validators.required(), validators.Length(min=1, max=100)])


class DeleteFacultyForm(Form):
    faculty = SelectField(label='Faculdade', coerce=int)


# TODO refactor only needs one form
class CreateDepartmentForm(Form):
    faculty = SelectField(label='Faculdade', coerce=int)
    name = StringField('Nome', [validators.required(), validators.Length(min=1, max=100)])


class ChooseDepartmentForm(Form):
    department = SelectField(label='Departamento', coerce=int)


class ChangeDepartmentForm(Form):
    faculty = SelectField(label='Faculdade', coerce=int)
    name = StringField('Nome', [validators.required(), validators.Length(min=1, max=100)])


class DeleteDepartmentForm(Form):
    department = SelectField(label='Departamento', coerce=int)

# TODO refactor only needs one form
class CreateVotingTableForm(Form):
    election = SelectField(label='Eleição', coerce=int)
    organic_unit = SelectField(label='Unidade Orgânica', coerce=int)


class ChooseVotingTableForm(Form):
    voting_table = SelectField(label='Mesa de voto', coerce=int)


class ChangeVotingTableForm(Form):
    election = SelectField(label='Nova Eleicão', coerce=int)
    organic_unit = SelectField(label='Nova Unidade Orgânica', coerce=int)


class DeleteVotingTableForm(Form):
    voting_table = SelectField(label='Voting Table', coerce=int)