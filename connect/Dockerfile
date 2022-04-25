FROM confluentinc/cp-kafka-connect-base:7.0.0

RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:1.7.0
RUN confluent-hub install --no-prompt jaredpetersen/jaredpetersen-redis-connector:1.2.0
# ENV CONNECT_BOOTSTRAP_SERVERS "kafka:9092"
# ENV CONNECT_CONFIG_STORAGE_TOPIC "connect-configs"
# ENV CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR "1"
# ENV CONNECT_OFFSET_STORAGE_TOPIC "connect-offsets"
# ENV CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR "1"
# ENV CONNECT_STATUS_STORAGE_TOPIC "connect-status"
# ENV CONNECT_STATUS_STORAGE_REPLICATION_FACTOR "1"
# ENV CONNECT_GROUP_ID "100"
# ENV CONNECT_KEY_CONVERTER "io.confluent.connect.avro.AvroConverter"
# ENV CONNECT_VALUE_CONVERTER "io.confluent.connect.avro.AvroConverter"
# ENV CONNECT_INTERNAL_KEY_CONVERTER "org.apache.kafka.connect.json.JsonConverter"
# ENV CONNECT_INTERNAL_VALUE_CONVERTER "org.apache.kafka.connect.json.JsonConverter"
# ENV CONNECT_PLUGIN_PATH "/usr/share/java,/usr/share/confluent-hub-components"

USER root
ADD connectors /etc/kafka-connect/connectors

WORKDIR /etc/kafka-connect/connectors

RUN chmod +x ./register_connectors.sh
USER cp-kafka-connect
CMD ["./register_connectors.sh"]