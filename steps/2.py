from flask import Flask
from langchain.llms import OpenAI

app = Flask(__name__)

@app.route("/query_open_ai",  methods = ['POST'])
def query_open_ai():
    llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo')

    print(llm("What is 2 + 2?"))

    return {
        'statusCode': 500,
        'body': 'TODO'
    }


'''test cURL
curl -XPOST localhost:5000/query_open_ai
'''

'''
pip install openai langchain

or

poetry add openai langchain
'''
