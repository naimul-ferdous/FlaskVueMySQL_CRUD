from flask import Flask, json, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app= Flask(__name__)

app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flask_vue'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql= MySQL(app)
CORS(app)

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    if request.method=='POST':
        cur= mysql.connection.cursor()
        title= request.get_json()['title']
        author= request.get_json()['author']
        temp= request.get_json()['read']
        reading= 1 if temp else 0
        cur.execute("INSERT INTO books(title, author, reading) VALUES('"+str(title)+"','"+str(author)+"','"+str(reading)+"')")
        mysql.connection.commit()
        result= {
            'title': title,
            'author': author,
            'reading': reading
        }
    else:
        cur= mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        result= cur.fetchall()
    return jsonify(result)

@app.route('/book/<id>', methods=['PUT', 'DELETE'])
def single_book(id):
    if request.method=='DELETE':
        cur= mysql.connection.cursor()
        response= cur.execute("DELETE FROM books WHERE id='"+id+"'")
        mysql.connection.commit()
        if response>0:
            result= {'message': 'Record deleted successfully'}
        else:
            result= {'error': 'Record not found'}
    else:
        cur= mysql.connection.cursor()
        title= request.get_json()['title']
        author= request.get_json()['author']
        temp= request.get_json()['read']
        reading= 1 if temp else 0
        cur.execute("UPDATE books SET title='"+str(title)+"', author='"+str(author)+"', reading='"+str(reading)+"' WHERE id='"+id+"'")
        mysql.connection.commit()
        result= {
            'title': title,
            'author': author,
            'reading': reading
        }
    return jsonify({'result': result})




if __name__== '__main__':
    app.run(debug=True)
