FROM public.ecr.aws/lambda/python:3.10

RUN yum install -y gcc python27 python27-devel postgresql-devel

COPY requirements.txt  .
RUN pip3 install wheel && pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY . ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
