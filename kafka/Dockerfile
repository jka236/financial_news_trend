FROM bitnami/kafka:latest

ADD create_default_topic.sh .

USER root

RUN chmod +x ./create_default_topic.sh

CMD [ "./create_default_topic.sh" ]