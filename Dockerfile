FROM public.ecr.aws/lambda/python:3.9-arm64

VOLUME ${LAMBDA_TASK_ROOT}/

COPY requirements.txt ${LAMBDA_TASK_ROOT}/

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt
# ^ for running locally and testing ^
# v HACK for getting the packages for then uploading as layer to AWS lambda : )
# RUN pip install --target ./package -r requirements.txt

# Copy function code
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_handler.lambda_handler" ]
