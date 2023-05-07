docker stop lambda_func_container
docker rm lambda_func_container
docker build -t lambda_func_image .
docker run -d -p 9000:8080 -e OPENAI_API_KEY=${OPENAI_API_KEY} --name lambda_func_container -v ${PWD}/package:/var/task/package lambda_func_image

YELLOW="\033[33m"
NORMAL="\033[0;39m"

curl -s -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d @test_payload.json &

docker logs --follow lambda_func_container

