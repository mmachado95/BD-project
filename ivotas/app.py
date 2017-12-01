from flask import Flask, render_template
from ivotas import models


app = Flask(__name__)


@app.route("/")
def hello():
    models.create_tables()
    models.seed_tables()
    models.create_organic_unit('TestingFaculty')
    models.create_organic_unit('TestingFaculty2')
    models.create_organic_unit('TestingDepartment')
    models.create_organic_unit('TestingDepartment2')
    models.create_faculty(7)
    models.create_faculty(8)
    models.create_department(9, 1)
    models.create_department(10, 2)
    models.create_election('Testing NEI ELECTION', 'Nucleo de estudantes', '2017-11-20 22:00:00', '2017-11-20 22:30:00', False, 2)
    models.create_list(2, 'Hey there awesome list', 2, [2, 3])
    models.create_voting_table(2, 1)
    models.create_voting_terminal(2)
    models.create_vote(1, 1)
    models.update_organic_unit('1', nome='total change')
    return render_template('main.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
