from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

#CRUD

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data.get('title'), description=data.get('description', ''))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({'message': 'Nova tarefa criada com sucesso!'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        'tasks': task_list,
        'total_tasks': len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:id_task>', methods=['GET'])
def get_single_task(id_task):
    for t in tasks:
        if t.id == id_task:
            return jsonify(t.to_dict())
    return jsonify({'message': 'Nenhuma tarefa correspondente foi encontrada.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
