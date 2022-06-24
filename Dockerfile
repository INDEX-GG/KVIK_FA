FROM python:3.10.4
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ADD /var/www/KVIK_FA/app/core/config.py /code/app/core/config.py
RUN python -m unittest app.tests.test
CMD ["uvicorn", "app.main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]