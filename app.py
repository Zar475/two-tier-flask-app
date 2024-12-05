from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'mysql'  # Assuming your MySQL container is named "mysql" in docker-compose
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'devops'

mysql = MySQL(app)

# Initialize the database and create the messages table if it doesn't exist
def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        );''')
        mysql.connection.commit()
        cur.close()

@app.route('/')
def hello():
    # Fetch all messages from the database to render on the homepage
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()

    # Fetch all messages after adding the new message
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()

    # Return the updated messages as JSON so the client can dynamically update
    return jsonify({'messages': [message[0] for message in messages]})

@app.route('/data')
def get_data():
    # This endpoint will return the latest messages in JSON format
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return jsonify([message[0] for message in messages])

if __name__ == '__main__':
    init_db()  # Initialize DB on first run
    app.run(host='0.0.0.0', port=5000, debug=True)

