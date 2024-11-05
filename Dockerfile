#
FROM python:3.10
#
WORKDIR /task-management
#
COPY ./requirements.txt /task-management/requirements.txt
#
RUN pip install --no-cache-dir --upgrade -r /customore_problem1/requirements.txt
#
COPY ./.env /task-management/.env
COPY api/common /task-management/common
COPY api/routers /task-management/routers
COPY api/serializers /task-management/serializers
COPY api/services /task-management/services
COPY ./main.py /task-management/main.py
#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]