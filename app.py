from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

init_db()

# -------------------------
# LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        student = conn.execute(
            "SELECT * FROM students WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if student:
            session['user'] = student['email']
            return redirect(url_for('dashboard'))
        else:
            flash("Email ou mot de passe incorrect", "error")

    return render_template("login.html")


# -------------------------
# REGISTER
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        adresse = request.form['adresse']
        annee = request.form['annee']

        if not email.endswith("@esisa.com"):
            flash("Email doit se terminer par @esisa.com", "error")
            return redirect(url_for('register'))

        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO students (nom, prenom, email, password, adresse, annee)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, prenom, email, password, adresse, annee))
            conn.commit()
        except:
            flash("Email déjà utilisé", "error")
            conn.close()
            return redirect(url_for('register'))

        conn.close()
        flash("Compte créé avec succès", "success")
        return redirect(url_for('login'))

    return render_template("register.html")


# -------------------------
# DASHBOARD
# -------------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("dashboard.html", students=students)

#Add-----------------
@app.route('/add_student', methods=['POST'])
def add_student():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    password = request.form['password']
    adresse = request.form['adresse']
    annee = request.form['annee']

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO students (nom, prenom, email, password, adresse, annee)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, prenom, email, password, adresse, annee))
        conn.commit()
        flash("Étudiant ajouté avec succès", "success")
    except sqlite3.IntegrityError:
        flash("Email déjà utilisé", "error")
    finally:
        conn.close()

    return redirect(url_for('dashboard'))
# -------------------------
# DELETE
# -------------------------
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


# -------------------------
# EDIT
# -------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        adresse = request.form['adresse']
        annee = request.form['annee']

        conn.execute("""
            UPDATE students
            SET nom=?, prenom=?, email=?, adresse=?, annee=?
            WHERE id=?
        """, (nom, prenom, email, adresse, annee, id))
        conn.commit()
        conn.close()
        flash("Étudiant modifié avec succès", "success")
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template("edit_student.html", student=student)

    return redirect(url_for('dashboard'))


# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Vercel fournit le PORT
    app.run(host="0.0.0.0", port=port)