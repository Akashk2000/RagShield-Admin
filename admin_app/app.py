from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = r'C:\\Users\\akash\\Desktop\\rag\\instance\\database.db'
ADMIN_SAFE_CODE = os.getenv('ADMIN_SAFE_CODE', 'ANTIRAG')  

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def admin_login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        code = request.form.get('code')
        agree = request.form.get('agree')
        if not agree:
            error = 'You must agree to the terms and conditions'
        elif code == ADMIN_SAFE_CODE:
            session['admin_logged_in'] = True
            return redirect(url_for('incidents'))
        else:
            error = 'Invalid safe code'
    return render_template('admin_login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/incidents')
@admin_login_required
def incidents():
    db = get_db()
    query = """
    SELECT incident.id, incident.description, incident.status, incident.admin_comment, incident.resolved_by, incident.resolved_at, user.college_name
    FROM incident
    JOIN user ON incident.user_id = user.id
    """
    cur = db.execute(query)
    incidents = cur.fetchall()
    return render_template('admin_incidents.html', incidents=incidents)

@app.route('/colleges')
@admin_login_required
def colleges():
    db = get_db()
    cur = db.execute("SELECT college_name, COUNT(*) as student_count FROM user GROUP BY college_name")
    colleges = cur.fetchall()
    return render_template('admin_colleges.html', colleges=colleges)

from datetime import datetime

@app.route('/resolve/<int:incident_id>', methods=['POST'])
@admin_login_required
def resolve_incident(incident_id):
    admin_comment = request.form.get('admin_comment', '')
    resolved_by = 'admin'  # This can be replaced with actual admin identifier from session if available
    resolved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()
    db.execute("""
        UPDATE incident
        SET status = 'resolved',
            admin_comment = ?,
            resolved_by = ?,
            resolved_at = ?
        WHERE id = ?
    """, (admin_comment, resolved_by, resolved_at, incident_id))
    db.commit()
    return redirect(url_for('incidents'))

@app.route('/')
def home():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
