FROM tiangolo/uwsgi-nginx-flask:python3.7-2019-10-14
WORKDIR /usr/src/app/client
COPY . .
RUN pip3 install -r ./requirements.txt
ENV FLASK_APP ./main.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
