from flask import Flask, request
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
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

    llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
    formatted_template = '''Please respond as Donald Trump would.\n{example_query} {example_response}'''
    prompt_tmplt = PromptTemplate(
        input_variables=["example_query", "example_response"],
        template=formatted_template,
    )

    print()
    print('prompt_tmplt formatted', prompt_tmplt.format(example_query='What is 2 + 2?', example_response='4'))
    print()

    prompt_selector = LengthBasedExampleSelector(
        examples=examples,
        # examples=[],
        example_prompt=prompt_tmplt,
        # max_length=46
    )

    # max_length appears to clip all the examples including and
    # following the last example that crosses the max_length threshold

    print()
    print('prompt_selector', prompt_selector)
    print()

    dynamic_prompt = FewShotPromptTemplate(
        example_selector=prompt_selector,
        example_prompt=prompt_tmplt,
        prefix="""Please respond as Donald Trump would""",
        suffix="Please respond as Donald Trump would\n{query}\n",
        input_variables=["query"],
        example_separator="\n\n",
    )

    final_prompt = dynamic_prompt.format(query=f'{prompt}')

    print()
    print('final_prompt', final_prompt)
    print()
    
    resp = llm(final_prompt)

    # resp = llm(prompt_tmplt.format(example_query='What is 2 + 2?', example_response='4'))
    
    return {
        'statusCode': 200,
        'body': resp
    }


'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What is 4 + 4?\"}" localhost:5000/query_open_ai 
'''
