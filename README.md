# README

## Flask

- poetry run flask run -p 3000
- poetry run flask --debug run

# AWS Lambda

## with AWS Console...

This is not a video about AWS lambda but I will quickly show you how to incorporate this in your apps...

- go to the lambda console - https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions
- Click `Create function`
- `Author from scratch`
- Name your function whatever you want: `open_ai_prompt_template`
- Choose environment: `Python 3.9`
- Architecture choose `arm64`
- copy the contents of `lambda_handler.py` into the `Code source` editor

### Create a layer from the `my-deployment-package.zip` directory

#### Creating the layer locally...

##### Tips for testing the lambda function locally

TLDR:
    - all of the following should be performed in the <PROJECT_DIR>
    - we will use Node.js software to watch our project files and rebuild/run a Docker container each time files change
    - pnpm i nodemon
    - add the following build script to the package.json file
        ```
        "scripts": {
            "dev": "nodemon --watch '**/*' -e py --exec ./build.sh"
        },
        ```
    - touch build.sh && chmod +x build.sh
    - add the following commands to the build.sh
        ```
        docker stop lambda_func_container
        docker rm lambda_func_container
        docker build -t lambda_func_image .
        docker run -p 9000:8080 -e OPENAI_API_KEY=${OPENAI_API_KEY} --name lambda_func_container -v ${PWD}/package:/var/task/package lambda_func_image
        ```

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @test_payload.json

#### Upload layer

- Click `Add a layer`
- Choose `Custom layer`
- Select the layer in the dropdown that includes the `openai` and `langchain` modules


