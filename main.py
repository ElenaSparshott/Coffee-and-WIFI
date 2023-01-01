from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), url()])
    coffee = SelectField('Coffee', choices=['', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    power = SelectField('Power', choices=['', '️🔌', '🔌🔌', '🔌🔌🔌️', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    wifi = SelectField('Wifi', choices=['', '️💪', '💪💪', '💪💪💪', '💪💪💪💪️', '💪💪💪💪💪'])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        name = form.data["cafe"]
        location = form.data['location']
        coffee = form.data['coffee']
        power = form.data['power']
        wifi = form.data['wifi']

        f = open("cafe-data.csv", "a")
        f.write(f'\n{name},{location},{coffee},{wifi},{power}')
        f.close()

        return redirect(url_for('add_cafe'))

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        rowcount = 0
        list_of_rows = []
        for row in csv_data:
            if rowcount == 0:
                header = row
            else:
                list_of_rows.append(row)
            rowcount += 1
    return render_template('cafes.html', cafes=list_of_rows, header=header)


if __name__ == '__main__':
    app.run(debug=True)
