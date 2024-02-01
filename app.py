from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

# Set the secret key to enable the Flask Debug Toolbar
app.config['SECRET_KEY'] = 'oh-so-secret'

# Enable the Flask Debug Toolbar
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/", methods=['GET', 'POST'])
def start_survey():
    if request.method == 'POST':
        # Initialize an empty list in the session for responses
        session['responses'] = []
        # Redirect to the first question
        return redirect(url_for('question', question_id=0))

    # Pass survey title and instruction to the template
    return render_template("start.html", survey=satisfaction_survey)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    # Use session to store and retrieve responses
    responses = session.get('responses', [])

    if len(responses) == len(satisfaction_survey.questions):
        flash('Survey completed. Thank you!','success')
        return redirect(url_for('thank_you'))

    if question_id != len(responses):
        # Redirect the user to the next unanswered question
        return redirect(url_for('question', question_id=len(responses)))

    if request.method == 'POST':
        try:
            response = request.form['choice']
            responses.append(response)
            session['responses'] = responses
            if len(responses) == len(satisfaction_survey.questions):
                return redirect(url_for('thank_you'))
            else:
                return redirect(url_for('question', question_id=len(responses)))
        except KeyError:
            flash('Please select a choice before proceeding.', 'error')
            return redirect(url_for('question', question_id=len(responses)))

    return render_template('question.html', question=satisfaction_survey.questions[question_id], question_id=question_id)


@app.route('/thank-you')
def thank_you():
    # Retrieve responses from the session
    responses = session.get('responses', [])
    # Render a thank-you page
    return render_template('thank_you.html', responses=responses)