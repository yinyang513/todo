# It should allow a client to create a Todo Note, add Todos to a note, complete Todos for a note, list all Todos and delete both Todos and Notes.
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo-db"
mongo = PyMongo(app)
todos = mongo.db.todos
notes = mongo.db.notes

@app.route('/')
def home():
    return 'Todo List'

@app.route('/create-note',methods=['POST'])
def create_note():
    note = request.args.get('note')
    notes.insert({'note': note})
    allTodos = todos.find()
    allNotes = notes.find()
    for todo in allTodos:
        print(todo)
    print()
    for notea in allNotes:
        print(notea)
    return note

@app.route('/add-todo',methods=['POST'])
def add_todo():
    todo = request.args.get('todo')
    note = request.args.get('note')
    # notess = notes.find()
    # for note in notess:
    #     print(note)

    find_note = notes.find_one({'note': note})
    # print(find_note)
    if find_note:
        todos.insert({'note': note,'todo': todo, 'complete': False})
    allTodos = todos.find()
    allNotes = notes.find()
    for todo in allTodos:
        print(todo)
    print()
    for note in allNotes:
        print(note)
    # print(lol)
    return 'inserted note'

@app.route('/complete-todo',methods=['POST'])
def complete_todo():
    complete = request.args.get('complete') # boolean
    todo = request.args.get('todo')
    
    temp = todos.update({'todo': todo}, {'$set': {'complete': complete}})
    # temp['complete'] = complete
    print(temp)
    allTodos = todos.find()
    allNotes = notes.find()
    for todo in allTodos:
        print(todo)
    print()
    for note in allNotes:
        print(note)
    return 'completed'

@app.route('/get-all-todos',methods=['GET'])
def get_todos():
    all_todos = todos.find()
    ret = []
    for todo in all_todos:
        ret.append({
            'note': todo['note'],
            'todo': todo['todo']
        })
    print(ret)
    return jsonify(ret)

@app.route('/delete',methods=['POST'])
def delete_todos():
    note = request.args.get('note')
    todo = request.args.get('todo')
    if todo:
        todos.remove({'todo': todo})
    if note:
        notes.remove({'note': note})
        todos.remove({'note': note})
    allTodos = todos.find()
    allNotes = notes.find()
    for todo in allTodos:
        print(todo)
    print()
    for note in allNotes:
        print(note)
    return 'delete'

if __name__ == "__main__": 
    app.run(port=5000)