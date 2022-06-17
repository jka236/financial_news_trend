package org.apache.beam.examples;
import com.google.common.collect.ImmutableMap;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.kafka.KafkaIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.*;
import org.apache.beam.sdk.values.KV;
import org.apache.kafka.common.serialization.LongDeserializer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.LongSerializer;
import org.apache.kafka.common.serialization.StringSerializer;
import java.time.*;
import java.util.*;
import org.joda.time.Duration;
import org.apache.beam.sdk.transforms.Count;
import java.text.SimpleDateFormat;
import org.apache.beam.sdk.io.mongodb.MongoDbIO;
import org.bson.Document;

public class MinimalWordCount {
    static final String TOKENIZER_PATTERN = "[^\\p{L}]+";

    public static void main(String[] args) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date date = new Date();
        LocalDate today = LocalDate.now();
        long numberOfDays = today.toEpochDay();
        String stringDate = dateFormat.format(date);
        PipelineOptions options = PipelineOptionsFactory.create();

        // Create the Pipeline object with the options we defined above.
        Pipeline p = Pipeline.create(options);
        Duration maxTime = Duration.standardMinutes(15);

        p.apply(KafkaIO.<Long, String>read()
                .withBootstrapServers("localhost:9093")
                .withTopic("article_title")
                .withKeyDeserializer(LongDeserializer.class)
                .withValueDeserializer(StringDeserializer.class)
                // .updateConsumerProperties(ImmutableMap.of("receive.buffer.bytes", 1024 *
                // 1024))
                // .updateConsumerProperties(ImmutableMap.of("auto.offset.reset",
                // (Object)"earliest"))/
                // .withMaxNumRecords(3)
                .withMaxReadTime(maxTime)
                .withoutMetadata() // PCollection<KV<Long, String>>
        )
                .apply(Values.<String>create())
                .apply("ExtractWords", ParDo.of(new DoFn<String, String>() {

                    @ProcessElement
                    public void processElement(ProcessContext c) {
                        for (String word : c.element().split(TOKENIZER_PATTERN)) {
                            if (!word.isEmpty()) {
                                c.output(word.toLowerCase());
                            }
                        }
                    }
                }))
                .apply(Count.perElement())
                .apply("ConvertToJson", MapElements.via(
                        new SimpleFunction<KV<String, Long>, Document>() {
                            public Document apply(KV<String, Long> input) {
                                return Document
                                        .parse(String.format("{word : '%s', count: '%s', date: '%d'}", input.getKey(),
                                                input.getValue(), numberOfDays));
                            }
                        }))
                .apply(MongoDbIO.write()
                        .withUri(
                                "mongodb+srv://rss_feed:rss_feed@cluster0.46sfz.mongodb.net/?retryWrites=true&w=majority")
                        .withDatabase("rss_feed")
                        .withCollection("rss_feed_write"));

        p.run().waitUntilFinish();

        // .apply(MapElements.into(TypeDescriptors.strings())
        // .via((KV<String, Long> wordCount) -> wordCount.getKey() + ": " +
        // wordCount.getValue()))
        // .via((KV<String, Long> wordCount) -> String.format("{word : %s, count: %s,
        // date: %s}",wordCount.getKey(), wordCount.getValue(), stringDate)))

        // .apply("ExtractPayload",
        // ParDo.of(new DoFn<String, KV<String, String>>() {
        // @ProcessElement
        // public void processElement(ProcessContext c)
        // throws Exception {
        // c.output(KV.of(String.format("{\"article_title\": \"test\"}"),
        // String.format("{\"word\": \"%s\"}", c.element())));
        // }
        // }))

        // .apply("FormatToWord", MapElements.via(new SimpleFunction<String, KV<String,
        // String>>(){
        // @Override
        // public String apply(String token_word){
        // // return String.format("{\"article_title\": \"%s\"}", token_word);
        // return KV.of("article_title", token_word);
        // }}
        // ))

        // .apply(TextIO.write().to("wordcounts"));

        // .apply(ElasticsearchIO.write().withConnectionConfiguration(
        // ElasticsearchIO.ConnectionConfiguration.create(new String[]
        // {"http://localhost:9200"}, "words", "words")));

        // .apply(KafkaIO.<String, String>write()
        // .withBootstrapServers("localhost:9093")
        // .withTopic("rss_feed")
        // .withKeySerializer(StringSerializer.class)
        // .withValueSerializer(StringSerializer.class));

        // p.run().waitUntilFinish();
        // p.run();

    }
}