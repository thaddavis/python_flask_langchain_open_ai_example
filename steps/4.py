from flask import Flask, request
from langchain.llms import OpenAI

app = Flask(__name__)

@app.route("/query_open_ai",  methods = ['POST'])
def query_open_ai():
    content_type = request.headers.get('Content-Type')
    prompt = None
    if (content_type == 'application/json'):
        json_payload = request.json
        prompt = json_payload['prompt']
    else:
        return 'Content-Type not supported!'

    llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
    formatted_template = f'Please respond as Donald Trump would to the following query: {prompt}'
    resp = llm(formatted_template) 

    print()
    print(formatted_template)
    print()
    print(resp)
    print()

    return {
        'statusCode': 200,
        'body': resp
    }


'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What is 4 + 4?\"}" localhost:5000/query_open_ai 
'''
