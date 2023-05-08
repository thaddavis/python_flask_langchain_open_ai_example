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
        docker run -d -p 9000:8080 -e OPENAI_API_KEY=${OPENAI_API_KEY} --name lambda_func_container -v ${PWD}/package:/var/task/package lambda_func_image

        curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @test_payload.json &

        docker logs --follow lambda_func_container
        ```
    - And FINALLY: `pnpm dev`


#### For manual testing

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @test_payload.json

#### Upload layer

- run `pnpm build_package`
- cd <PROJECT_ROOT>
- cp -r package python
- zip -r layer.zip python 
<!-- - zip python_lambda_layer.zip lambda_handler.py -->
- aws lambda publish-layer-version --layer-name open_ai_prompt_template_layer \
    --description "open_ai_prompt_template_layer" \
    --license-info "MIT" \
    --zip-file fileb://layer.zip \
    --compatible-runtimes python3.9 \
    --compatible-architectures "arm64" \
    --profile aws_lambda_101 --region us-east-1
- aws lambda update-function-configuration --function-name open_ai_prompt_template --layers arn:aws:lambda:us-east-1:333427308013:layer:open_ai_prompt_template_layer:4 --profile aws_lambda_101 --region us-east-1

#### Tweak the lambda function `Configuration`

- set the OPENAI_API_KEY

ie: aws lambda update-function-configuration --function-name open_ai_prompt_template --environment '{"Variables":{"OPENAI_API_KEY":"$OPENAI_API_KEY"}}' --profile aws_lambda_101 --region us-east-1

- increase the timeout to 10 seconds

ie: aws lambda update-function-configuration --function-name open_ai_prompt_template --timeout 20 --profile aws_lambda_101 --region us-east-1

- set the reserved concurrency

ie: aws lambda put-function-concurrency --function-name open_ai_prompt_template --reserved-concurrent-executions 5 --profile aws_lambda_101 --region us-east-1

#### Invoke the function

- aws lambda invoke --function open_ai_prompt_template response.json
- aws lambda invoke --function open_ai_prompt_template --cli-binary-format raw-in-base64-out --payload file://test_payload.json response.json --profile aws_lambda_101 --region us-east-1