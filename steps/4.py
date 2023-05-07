from flask import Flask, request
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

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

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    
    formatted_template = f'Please respond as Donald Trump would to the following query: {prompt}'
    resp = llm([HumanMessage(content=formatted_template)])

    return {
        'statusCode': 200,
        'body': resp.content
    }


'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What is the color of an orange?\"}" localhost:5000/query_open_ai 
'''
