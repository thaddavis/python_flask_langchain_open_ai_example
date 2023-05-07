from flask import Flask, request
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts.example_selector import LengthBasedExampleSelector

from examples import examples

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

    formatted_template = '''{example_query} {example_response}'''
    prompt_tmplt = PromptTemplate(
        input_variables=["example_query", "example_response"],
        template=formatted_template,
    )

    prompt_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=prompt_tmplt
    )

    print()
    print('prompt_selector', prompt_selector)
    print()

    # example_text_lengths will count the tokens (or word count) of each example (query + response)

    dynamic_prompt = FewShotPromptTemplate(
        example_selector=prompt_selector,
        example_prompt=prompt_tmplt,
        prefix="""Can you return an array of objects as a JSON formatted string that are geographically relevant to an arbitrary query?

        REQUIREMENTS:
        - Each object in the array should contain 3 keys: lon, lat, blurb
        - lon is the longitude of the coords for each match to the query
        - lat is the latitude of the coords for each match to the query
        - blurb is the 1-3 sentence answer to the query along with information about the environmental concerns of the city or region in which the coords exist
        - The array should be max length 3 items
        - the overall length of the answer should be maximum 500 characters and should be a fully parsable JSON string
        - if you cannot provide accurate information then please provide your best guess along with a disclaimer
        """,
        suffix="Here is the arbitrary query...\n\n{input}\n",
        input_variables=["input"],
        example_separator="\n\n",
    )

    final_prompt = dynamic_prompt.format(input=f'{prompt}')

    print()
    print('final_prompt')
    print()
    print(final_prompt)
    print()

    resp = llm([HumanMessage(content=final_prompt)])
    
    return {
        'statusCode': 200,
        'body': resp.content
    }

'''test cURL
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What is the greatest country in the history of mankind?\"}" localhost:5000/query_open_ai 
curl -XPOST --header "Content-Type: application/json" -d "{\"prompt\":\"What are the hottest cities in America?\"}" localhost:5000/query_open_ai 
'''
