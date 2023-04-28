from flask import Flask, request
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.llms import OpenAI
from flask_cors import CORS, cross_origin

from examples import examples

app = Flask(__name__)
cors = CORS(app)

@app.route("/",  methods = ['POST'])
@cross_origin()
def hello_world():
    content_type = request.headers.get('Content-Type')
    query = None
    if (content_type == 'application/json'):
        json = request.json
        query = json['prompt']
    else:
        return 'Content-Type not supported!'


    # Instantiate LLM
    llm = OpenAI(temperature=0)
    # Prompt Template

    formatted_template = """
    Can you return an array of objects as a JSON formatted string that are geographically relevant information to an arbitrary query?
    REQUIREMENTS:
    - Each object in the array should contain 3 keys
    - lon is the longitude of the coords for each match to the query
    - lat is the latitude of the coords for each match to the query
    - blurb is the 1-3 sentence answer to the query along with information about the environmental concerns of the city or region in which the coords exist
    - The array should be max length 3
    - the overall length of the answer should be maximum 500 characters and a fully parsable JSON string
    - if you cannot provide accurate information then please provide your best guess along with a disclaimer
    
    The arbitrary query is below\n {query}\n{answer}\n
    """

    prompt_tmplt = PromptTemplate(
        input_variables=["query", "answer"],
        template=formatted_template,
    )

    # print(prompt_tmplt)

    prompt_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=prompt_tmplt
    )

    # print(prompt_selector)

    dynamic_prompt = FewShotPromptTemplate(
        example_selector=prompt_selector,
        example_prompt=prompt_tmplt,
        prefix="""Answer each query""",
        suffix="Query: {input}\n",
        input_variables=["input"],
        example_separator="\n\n",
    )

    # print('dynamic_prompt', dynamic_prompt)

    prompt = dynamic_prompt.format(input=f'{query}')
    
    resp = llm(prompt)
    print('resp', resp)
    # print(json.loads(resp))

    # JSONresp = json.loads(resp)
    return resp