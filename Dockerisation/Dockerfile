FROM ubuntu:20.04

ADD ./  /fichiers/

#ADD app/requirements.txt app/main.py  app/SGD_model.pkl app/GAUSSIANNB_modelbis.pkl \
#    app/LOGIT_model.pkl app/churn.csv /fichiers/

WORKDIR fichiers

RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0

#FROM ubuntu:20.04

#ADD ./ /app

#WORKDIR /app

#RUN apt update \
#&& apt install python3-pip -y \
#&& pip install -r requirements.txt

#EXPOSE 8000

#CMD uvicorn main:app --host 0.0.0.0