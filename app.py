from flask import Flask, request, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

submissions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['name']
    assignment_code = request.form['code']

    # Write code to a temporary file
    with open('submission.py', 'w') as f:
        f.write(assignment_code)

    # Evaluate the code by running predefined test cases
    result = evaluate_code()

    # Store the submission and result
    submissions.append({'name': student_name, 'code': assignment_code, 'result': result})
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html', submissions=submissions)

def evaluate_code():
    try:
        result = subprocess.run(['python3', 'submission.py'], capture_output=True, text=True)
        output = result.stdout
    except Exception as e:
        output = str(e)
    return output

if __name__ == '__main__':
    app.run(debug=True)

