FROM python:3

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD petition_counts /app

ENV FLASK_APP /app/__init__.py
ENV FLASK_ENV production

EXPOSE 3000
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
