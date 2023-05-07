from flask import Flask

app = Flask(__name__)

@app.route("/query_open_ai",  methods = ['POST'])
def query_open_ai():
    return {
        'statusCode': 500,
        'body': 'TODO'
    }


'''test cURL
curl -XPOST localhost:5000/query_open_ai
'''