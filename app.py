import subprocess
import uuid
import queue
import threading
import sys
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

# Store running tasks and their output queues
tasks = {}

def enqueue_output(out, q):
    """Read output line by line and put it into the queue."""
    for line in iter(out.readline, b''):
        q.put(line.decode('utf-8'))
    out.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required!"}), 400

    task_id = str(uuid.uuid4())
    print(f"Starting QEC Automation for user: {username} (Task: {task_id})")
    
    try:
        # Run with -u to unbuffer python output, redirect stdout and stderr to PIPEs
        proc = subprocess.Popen(
            [sys.executable, '-u', 'qec_auto.py', '--username', username, '--password', password],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1 # Line buffered
        )
        
        q = queue.Queue()
        t = threading.Thread(target=enqueue_output, args=(proc.stdout, q))
        t.daemon = True
        t.start()
        
        tasks[task_id] = {'process': proc, 'queue': q, 'thread': t}
        
        return jsonify({
            "status": "success", 
            "task_id": task_id,
            "message": "Automation started!"
        })
    except Exception as e:
        print(f"Error starting process: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stream/<task_id>')
def stream(task_id):
    def generate():
        if task_id not in tasks:
            yield f"data: Error: Task not found\n\n"
            return
            
        task = tasks[task_id]
        q = task['queue']
        proc = task['process']
        
        while True:
            try:
                # Read from queue with a timeout
                line = q.get(timeout=0.1)
                yield f"data: {line}\n\n"
            except queue.Empty:
                # Check if process ended
                if proc.poll() is not None:
                    # Drain any remaining lines
                    while not q.empty():
                        yield f"data: {q.get()}\n\n"
                    
                    if proc.returncode == 0:
                        yield f"data: [PROCESS_COMPLETED]\n\n"
                    else:
                        yield f"data: [PROCESS_FAILED]\n\n"
                    
                    # Cleanup
                    del tasks[task_id]
                    break

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)

