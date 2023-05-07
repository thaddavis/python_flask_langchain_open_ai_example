from flask import Flask, request
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts.example_selector import LengthBasedExampleSelector

from examples_test import examples

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

    prompt_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=prompt_tmplt,
        max_length=42
    )

    print()
    print('prompt_selector', prompt_selector)
    print()

    # example_text_lengths will count the tokens (or word count) of each example (query + response)

    dynamic_prompt = FewShotPromptTemplate(
        example_selector=prompt_selector,
        example_prompt=prompt_tmplt,
        prefix="""Answer each query""",
        suffix="Please respond as Donald Trump would.\n{input}\n",
        input_variables=["input"],
        example_separator="\n",
    )

    final_prompt = dynamic_prompt.format(input=f'{prompt}')

    print()
    print('final_prompt')
    print()
    print(final_prompt)
    print()

    return {
        'statusCode': 500,
        'body': 'TODO'
    }


'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What is the greatest country in the history of mankind?\"}" localhost:5000/query_open_ai 
'''
