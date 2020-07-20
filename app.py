# importing flask dependency

from flask import Flask

# new flask instance (singular version)
# using double underscores as magic methods

app = Flask(__name__)

# creating routes(pathways)

@app.route('/')

# putting code that runs in this specific route under it 

def hello_world():
    return 'Hello World'

@app.route('/test')

def route_test():
    return 'come and peak me, please!!!!!'