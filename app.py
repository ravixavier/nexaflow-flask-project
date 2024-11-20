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
    return jsonify({'message': 'Nova tarefa criada com sucesso!', 'id': new_task.id})

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

@app.route('/tasks/<int:id_task>', methods=["PUT"])
def update_task(id_task):
    task = None
    for t in tasks:
        if t.id == id_task:
            task = t
            break

# aqui caso eu não queira usar o 'task = None', eu posso usar uma expressão geradora
# com o next(), Ex: task = next((t for t in tasks if t.id == id_task), None)
# Essa é uma expressão geradora que percorre a lista tasks.
# Para cada item t em tasks, verifica se a condição t.id == id_task é verdadeira.
# Se encontrar um objeto que satisfaça a condição, ele "produz" esse objeto e para a execução.
# Por exemplo:
# Se tasks = [task1, task2, task3] e id_task = 2, a expressão geradora retornará o objeto task2 (se
# task2.id == 2).
# next() tenta obter o primeiro valor gerado pela expressão geradora.
# Se a expressão geradora não produzir nenhum valor (ou seja, se nenhum objeto satisfizer a condição
# t.id == id_task), next retorna o valor padrão fornecido como segundo argumento (None).

    print(task)
    if task is None:
        return jsonify({'message': 'Nenhuma tarefa correspondente foi encontrada.'}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    print(task)
    return jsonify({'message': 'Tarefa atualizada com sucesso.'})

@app.route('/tasks/<int:id_task>', methods=['DELETE'])
def delete_task(id_task):
    # aqui está o exemplo de como eu poderia ter escrito no metodo PUT
    task = next((t for t in tasks if t.id == id_task), None)

    if task is None:
        return jsonify({'message': 'Nenuma tarefa correspondente foi encontrada.'}), 404

    tasks.remove(task)
    return jsonify({'message': 'Tarefa deletada com sucesso!😊'})

if __name__ == '__main__':
    app.run(debug=True)
