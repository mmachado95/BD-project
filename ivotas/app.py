from flask import Flask
from ivotas import models


app = Flask(__name__)


@app.route("/")
def hello():
    models.create_tables()
    models.seed_tables()
    models.create_faculty('TestingFaculty')
    models.create_faculty('TestingFaculty2')
    models.create_department(2, 'TestingDepartment')
    models.create_department(1, 'TestingDepartment2')
    models.create_election(None, 1, 'Testing NEI ELECTION', 'Nucleo de estudantes', '2017-11-20 22:00:00', '2017-11-20 22:30:00', False, 2)
    models.create_list(2, 'Hey there awesome list', 2, [2, 3])
    models.create_voting_table(2, 1)
    models.create_voting_terminal(2)
    models.create_vote(1, 2, 1)
    models.create_list_results(1, 23, 50)
    models.create_results(1, 1)
    print(models.search_faculty())
    print(models.search_department())
    print(models.search_user())
    print(models.search_faculty(nome='FCTUC'))
    print(models.search_department(nome='Economia'))
    print(models.search_user(nome='Miguel'))
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
