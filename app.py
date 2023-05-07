from flask import Flask, request
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
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

    formatted_template = '''Please respond as Donald Trump would.\n{example_query} {example_response}'''
    prompt_tmplt = PromptTemplate(
        input_variables=["example_query", "example_response"],
        template=formatted_template,
    )

    print()
    print('prompt_tmplt formatted')
    print()
    print(prompt_tmplt.format(example_query='What is 2 + 2?', example_response='4'))
    print()
    print(prompt_tmplt.format(example_query='What color is an orange?', example_response='Well my friends, the color of an orange is orange of course.'))
    print()

    return {
        'statusCode': 500,
        'body': 'TODO'
    }


'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"\"}" localhost:5000/query_open_ai 
'''
