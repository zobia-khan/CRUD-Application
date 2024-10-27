from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database" for storing tasks
tasks = {}
next_id = 1

# Route for the home page to display tasks
@app.route('/')
def index():
    # Sort open tasks first, then completed tasks, by ID (oldest tasks first)
    open_tasks = {task_id: task for task_id, task in tasks.items() if not task['completed']}
    completed_tasks = {task_id: task for task_id, task in tasks.items() if task['completed']}
    
    sorted_open_tasks = sorted(open_tasks.items(), key=lambda x: x[0])
    sorted_completed_tasks = sorted(completed_tasks.items(), key=lambda x: x[0])

    return render_template('index.html', open_tasks=sorted_open_tasks, completed_tasks=sorted_completed_tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add():
    global next_id
    task_name = request.form['task']
    
    if task_name:
        tasks[next_id] = {
            'id': next_id,
            'task': task_name,
            'completed': False
        }
        next_id += 1
    
    return redirect(url_for('index'))

# Route to mark a task as completed
@app.route('/complete/<int:task_id>')
def complete(task_id):
    if task_id in tasks:
        tasks[task_id]['completed'] = True
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if task_id in tasks:
        del tasks[task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
