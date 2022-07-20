FROM python:3.8.13-buster
COPY ./app /root/reviews/
WORKDIR /root/reviews/
RUN pip3 install -r requirements.txt

CMD ["bash", "entrypoint_start.sh"]