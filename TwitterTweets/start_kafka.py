'''from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('main.html')

@app.route('/StartKafka/')
def start_kafka():
    os.chdir('kafka')
    print('Starting Kafka Server')
    os.system('bin\windows\kafka-server-start config\server.properties')

if __name__ == '__main__':
  app.run(debug=True)
'''
import os
os.chdir('kafka')
print('Starting Kafka Server')
os.system('bin\windows\kafka-server-start config\server.properties')
