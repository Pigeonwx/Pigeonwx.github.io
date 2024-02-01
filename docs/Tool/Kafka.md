# Kafka

## 入门

### 定义

- 传统：分布式的基于发布/订阅模式的消息队列
- 最新：开源分布式事件流平台，存储分析应用

### 消息队列

- 场景
  - 大数据：Kafka
  - JavaEE：ActiveMQ\RabbitMQ\RocketMQ

- 应用特点
  - 缓冲/削峰
  - 异步
  - 解耦

- 模式
  - 点对点：用一个删一个
  - 发布/订阅模式：多个主题，按主题喜好订阅，不删除

### 基础架构

- 基本架构

  ![image-20230921145014004](/Users/xiangjianhang/Downloads/LN/Kafka/image-20230921145014004.png)

### 基本操作

- Topic
  - ![截屏2023-09-22 15.29.42](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-22 15.29.42.png)
  -  bin/kafka-topics.sh -bootstrap-server 192.168.1.100:58589 topic first -create -partitions 1 replication-factor 3
  - 分区只能增不能减，--alter ; 副本需要另外手段修改
- Producer
  -  bin/kafka-console-producer.sh --bootstrap-server 192.168.1.100:58589 --topic first
  - ![截屏2023-09-22 15.57.12](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-22 15.57.12.png)
  - 数据传递安全
    - 至少一次（At Least Once） =ACK级别设置为-1 + 分区副本大于等于2 + ISR里应答的最小副本数量大于等于2
    - 最多一次（At Most Once) = ACK级别设置为0
    - 总结：At Least Once可以保证数据不丢失，但是不能保证数据不重复；
      At Most Once可以保证数据不重复，但是不能保证数据不丢失。
    - 精确一次(Exactly Once) :对于一些非常重要的信息,比如和钱相关的数据,要求数据既不能重复也不丢失Kafka 0.11版本以后,引入了一项重大特性:幂等性和事务。
    - 幂等性就是指Producer不论向Broker发送多少次重复数据, Broker端都只会持久化一条,保证了不重复。精确一次（Exactly Once） = 幂等性 + 至少一次（ack=-1 + 分区副本数>=2 + ISR最小副本数量>=2）。重复数据的判断标准:具有<PID, Partition, SeqNumber>相同主键的消息提交时, Broker只会持久化一条。其 中PID是Kafka每次重启都会分配一个新的; Partition表示分区号; Sequence Number是单调自增的。所以幂等性只能保证的是在单分区单会话内不重复。
    - 事务：开启事务，必须开启幂等性
      
      ![截屏2023-09-26 16.24.24](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-26 16.24.24.png)
- Consumer
  -  bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.100:58589 --topic first --from-beginning

### Zookeeper & Kafak

- Relationship
  - ![截屏2023-09-26 19.09.50](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-26 19.09.50.png)

- Broker Leader
  - ![截屏2023-09-27 18.57.13](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-27 18.57.13.png) 

- 分区的好处
  - 存储：便于合理使用存储资源，每个Partition在一个Broker上存储，可以把海量的数据按照分区切割成一块一块数据存储在多台Broker上。合理控制分区的任务,可以实现负载均衡的效果。
  - 计算：提高并行度,生产者可以以分区为单位发送数据;消费者可以以分区为单位进行消费数据。
  - ![截屏2023-09-28 19.08.58](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-28 19.08.58.png) 
  - 粘性：先往一个分区发，集合在一起
  - 分区分配：保存负载均衡 & 可靠
    - ![截屏2023-09-29 11.57.03](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 11.57.03.png)

### 副本

- Kafka 副本作用：提高数据可靠性。
-  Kafka默认副本 1 个,生产环境一般配置为 2 个,保证数据可靠性；太多副本会增加磁盘存储空间,增加网络上数据传输,降低效率。
-  Kafka中副本分为: Leader和Follower. Kafka生产者只会把数据发往Leader, 然后Follower 找Leader进行同步数据。
- Kafka分区中的所有副本统称为 AR （Assigned Repllicas)。AR=ISR+OSR
  - ISR，表示和 Leader 保持同步的 Follower 集合。如果 Follower 长时间未向 Leader 发送 通信请求或同步数据,则该Follower将被踢出ISR。该时间阈值由replica.lag.time.max.ms参数设定,默认30s。 Leader发生故障之后,就会从ISR中选举新的Leader.
  - OSR，表示 Follower 与 Leader 副本同步时，延迟过多的副本。

### 故障处理

- Follower

![截屏2023-09-29 11.17.52](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 11.17.52.png)

- Leader

![截屏2023-09-29 11.51.46](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 11.51.46.png)

### Kafka文件存储

- 存储架构：![截屏2023-09-29 14.41.35](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 14.41.35.png)

- 稀疏索引查找：![image-20230929150147570](/Users/xiangjianhang/Library/Application Support/typora-user-images/image-20230929150147570.png) 

### 文件清理策略

- 清理时间：Kafka 中默认的日志保存时间为 7天，可以通过调整如下参数修改保存时间。
  -  log.retention.hours，最低优先级小时，默认 7 天。
  - log.retention.minutes，分钟。
  - log.retention.ms，最高优先级毫秒。
  - log.retention.check.interval.ms，负责设置检查周期，默认 5 分钟。
- 清理策略
  - delete
    -  log.cleanup.policy = delete 所有数据启用删除策略
    - 基于时间:默认打开。以segment中所有记录中的最大时间戳作为该文件时间戳。
    - 基于大小:默认关闭。超过设置的所有日志总大小,删除最早的segment。
       log.retention.bytes,默认等于-1,表示无穷大。
  - compact
    - compact日志压缩：对于相同key的不同value值，只保留最后一个版本。
       log.cleanup.policy=compact所有数据启用压缩策略
    - 压缩后的offset可能是不连续的，比如上图中没有6，当从这些offset消费消息时，将会拿到比这个offset大的offset对应的消息，实际上会拿到offset为7的消息，并从这个位置开始消费。
    - 这种策略只适合特殊场景,比如消息的key是用户ID, value是用户的资料,通过这种压缩策略,整个消息里就保存了所有用户最新的资料。

### 高效读写数据

1. Kafka 本身是分布式集群，可以采用分区技术，并行度高
2. 读数据采用稀疏索引，可以快速定位要消费的数据
3. 顺序写磁盘
   - Kafka 的 producer 生产数据，要写入到 log 文件中，写的过程是一直追加到文件末端，为顺序写。官网有数据表明，同样的磁盘，顺序写能到 600M/s，而随机写只有 100K/s。这与磁盘的机械机构有关，顺序写之所以快，是因为其省去了大量磁头寻址的时间。
4. 页缓存和零拷贝技术
   - ![截屏2023-09-29 15.17.05](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 15.17.05.png)

## Kafka 消费

### Kafka消费方式

- pull（拉）模式： consumer采用从broker中主动拉取数据。Kafka采用这种方式。
  - pull模式不足之处是，如果Kafka没有数据，消费者可能会陷入循环中，一直返回空数据。
- push（推）模式：Kafka没有采用这种方式，因为由broker决定消息发送速率，很难适应所有消费者的消费速率。

### Kafka消费者总体工作流程

![截屏2023-09-29 15.25.44](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 15.25.44.png)

### 消费者组   

- Consumer Group（CG）：消费者组，由多个consumer组成。形成一个消费者组的条件，是所有消费者的groupid相同。
  - 消费者组内每个消费者负责消费不同分区的数据，一个分区只能由一个组内消费者消费。
  - 消费者组之间互不影响。所有的消费 者都属于某个消费者组，即消费者组是逻辑上的一个订阅者。
  - 如果向消费组中添加更多的消费者，超过主题分区数量，则有一部分消费者就会闲置，不会接收任何消息。
- 消费者组的初始化流程
  - ![截屏2023-09-29 16.30.03](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 16.30.03.png)
  - ![截屏2023-09-29 17.00.56](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 17.00.56.png)
- 代码实现案例：必须指定消费组id 

### 消费offset

-  _consumer_offsets 主题里面采用 key 和 value 的方式存储数据。key 是 group.id+topic+分区号，value 就是当前 offset 的值。每隔一段时间，kafka 内部会对这个 topic 进行compact，也就是每个group.id+topic+分区号就保留最新数据
- ![截屏2023-09-29 21.14.38](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 21.14.38.png)

- 自动提交offset：![截屏2023-09-29 21.39.31](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 21.39.31.png)

- 手动提交offset
  - 虽然自动提交offset十分简单便利,但由于其是基于时间提交的,开发人员难以把握offset提交的时机。因 此Kafka还提供了手动提交offset的API。
  - 手动提交offset的方法有两种：分别是commitSync（同步提交）和commitAsync（异步提交）。两者的相同点是,都会将本次提交的一批数据最高的偏移量提交;不同点是,同步提交阻塞当前线程,一直到提交成功,并且会自动失败重试(由不可控因素导致,也会出现提交失败) ;而异步提交则没有失败重试机制,故有可能提交失败。commitSync（同步提交）：必须等待offset提交完毕，再去消费下一批数据。

- 指定offset消费

- 指定时间消费

  - ```
    // 希望把时间转换为对应的offset
    HashMap<TopicPartition, Long> topicPartitionLongHashMap = new HashMap<>();
    // 封装对应集合
     for (TopicPartition topicPartition : assignment){
    topicPartitionLongHashMap.put(topicPartition,System.currentTimeMillis() - 1 * 24 * 3600 * 1000);
     Map<TopicPartition, OffsetAndTimestamp> topicPartitionoffsetAndTimestampHap = kafkaConsumer.offsetsForTimes(topicPartitionLongHashHap);
     
     // 指定消费的offset
     for (TopicPartition topicPartition : assignment) {
     OffsetAndTimestamp offsetAndTimestamp = topicPartitionoffsetAndTimestampMap.get(topicPartition);
     kafkaConsumer.seek(topicPartition,offsetAndTimestamp.offset());
    }
    ```

- 消费问题：

  - 重复消费：已经消费了数据，但是 offset 没提交。
  - 漏消费：先提交 offset 后消费，有可能会造成数据的漏消费。
  - 解决方法：事务 

### Kraft

- kafka2.8.0 之后可采用
  - 原先Zookeeper 保存元数据
  - 现在保存在controller里面

## 生产经验

### 生产经验：数据有序

- 单分区内，有序
- 多分区：分区与分区间无序，若需要有序需要重排，借助spark或flink

### 生产经验：数据无序

- kafka在1.x版本之前保证数据单分区有序，条件如下： max.in.flight.requests.per.connection=1 （不需要考虑是否开启幂等性）。
- kafka在1.x及以后版本保证数据单分区有序,条件如下:
  - （1）未开启幂等性max.in.flight.requests.per.connection 需要设置为1
  - （2）开启幂等性max.in.flight.requests.per.connection需要设置小于等于5
  - 原因说明:因为在kafka 1.x以后,启用幂等后, kafka服务端会缓存producer发来的最近5个request的元数据,
    故无论如何，都可以保证最近5个request的数据都是有序的。

### 生产经验：节点服役和退役

- 新服役
  - Step1：clone快速，并启动
  - Step2：负载均衡 
    1. 创建要均衡的主题 topics-to-move.json
    2. 生成负载均衡的计划：bin/kafka-reassign-partitions.sh  hadoop102: 9092 bootstrap-server -topics-to-move-json-file  topics-to-move.json --broker-list "0,1,2,3" --qenerate =======执行后显示current /proposed
    3. 创建副本存储计划： vim increase-replication-factor.json包含生成的计划
    4. 执行副本存储计划： bin/kafka-reassign-partitions.sh bootstrap-server -reassignment-json-file  increase-replication-factor.json --executee  hadoop102:9092
    5. 验证副本存储计划： bin/kafka-reassign-partitions.sh hadoop102:9092
        bootstrap-server --reassignment-json-file increase-replication-factor.json --verify

- 退役旧节点
  - Step1：执行负载均衡操作
    1. 创建要均衡的主题 topics-to-move.json
    2. 生成负载均衡的计划：bin/kafka-reassign-partitions.sh  hadoop102: 9092 bootstrap-server -topics-to-move-json-file  topics-to-move.json --broker-list "0,1,2" --qenerate =======执行后显示current /proposed
    3. 创建副本存储计划： vim increase-replication-factor.json包含生成的计划
    4. 执行副本存储计划： bin/kafka-reassign-partitions.sh bootstrap-server -reassignment-json-file  increase-replication-factor.json --executee  hadoop102:9092
    5. 验证副本存储计划： bin/kafka-reassign-partitions.sh hadoop102:9092
        bootstrap-server --reassignment-json-file increase-replication-factor.json --verify
  - Step2：停止退役broker

### 生产经验：手动调整分区副本存储

- 背景：![截屏2023-09-29 11.58.57](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-29 11.58.57.png)

- Steps:

  - Step1：创建新分区

  - Step2：查看分区存储情况

  - Step3：创建副本存储计划

    - ```json
       "version":1,
       "partitions":[
         {"topic":"three","partition":0, "replicas": [0,1]}, 			 {"topic":"three","partition":1,"replicas": [0,1]},	 	 		 
         {"topic":"three","partition":2,"replicas": [1,0]},				 {"topic":"three","partition":3,"replicas": [1,0]}
        ]
      ```

  - Step4：执行副本存储计划
  - Step5：验证

- Leader Partition自动平衡 
  - 正常情况下, Kafka本身会自动把Leader Partition均匀分散在各个机器上,来保证每台机器的读写吞吐量都是均匀的。但是如果某些broker宕机，会导致Leader Partition过于集中在其他少部分几台broker上，这会导致少数几台broker的读写请求压力过高，其他宕机的broker重启之后都是follower partition，读写请求很低，造成集群负载不均衡。
  -  auto.leader.rebalance.enable, 自动Leader Partition 平衡 默认是true。
  -  leader.imbalance.per.broker.percentage,默认是10%。每个broker允许的不平衡的leader的E率。如果每个broker超过了这个值,控制器会触发leader的平衡。
  - leader.imbalance.check.interval.seconds,默认值300秒。检查leader负载是否平衡的间隔时间。

### 生产经验：增加副本因子

- 某个主题的重要性增加，所以需要增加副本数
- 步骤流程
  - Step1：创建主题
  - Step2：手动增加副本存储
  - Step3：执行副本存储计划

### 生产经验：分区的分配和再平衡

- 分区策略 
  - Range：
    -  Range 是对每个 topic 而言的。首先对同一个 topic 里面的分区按照序号进行排序，并对消费者按照字母顺序进行排序。假如现在有 7 个分区，3 个消费者，排序后的分区将会是0,1,2,3,4,5,6；消费者排序完之后将会是CO,C1,C2通过 partitions数/consumer数 来决定每个消费者应该消费几个分区。如果除不尽，那么前面几个消费者将会多消费 1 个分区。
    - 例如，7/3=2 余1,除不尽，那么消费者CO便会多消费 1 个分区。8/3=2余2，除不尽，那么CO和C1分别多
      消费一个。
    - 缺点：容易产生数据倾斜，多个主题都积累多部分数据，总体就会多很多
  -  RoundRobin： 针对集群中所有Topic而言
    - RoundRobin 轮询分区策略，是把所有的 partition 和所有的 consumer 都列出来，然后按照 hashcode 进行排序，最后通过轮询算法来分配partition 给到各个消费者。
  - Sticky
    - 粘性分区定义:可以理解为分配的结果带有“粘性的”。即在执行一次新的分配之前,考虑上一次分配的结果,尽量少的调整分配的变动,可以节省大量的开销。粘性分区是 Kafka 从 0.11.x 版本开始引入这种分配策略，首先会尽量均衡的放置分区到消费者上面,在出现同一消费者组内消费者出现问题的时候,会尽量保持原有分配的分区不变化。

### 生产经验：消费者事务

- ![截屏2023-09-30 13.04.13](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-30 13.04.13.png)

### 生产经验：数据积压（消费者如何提高吞吐量）

- 解决方法：
  - 1）如果是Kafka消费能力不足，则可以考虑增加Topic的分区数，并且同时提升消费组的消费者数量，消费者数 = 分区数。（两者缺一不可）
  - 2）如果是下游的数据处理不及时：提高每批次拉取的数量。批次拉取数据过少(拉取数据/处理时间<生产速度) ,使处理的数据小于生产的数据，也会造成数据积压。

## 框架集成

### 集成Flume

- Flume生产者 

  - 举个例子：![截屏2023-09-30 17.14.27](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-30 17.14.27.png)

  - 关键配置文件：

  - ```
    # 1 组件定义
     al.sources = rl
     al.sinks = k1
     al.channels = c1
     # 2 配置 source
     al.sources.r1.type = TAILDIR
     al.sources.r1.filegroups = f1
     al.sources.r1.filegroups.f1 = /opt/module/applog/app.*
     al.sources.r1.positionFile
     /opt/module/flume/taildir_position.json
     # 3 配置 channel
     al.channels.cl.type = memory
     al.channels.cl.capacity = 1000
     a1.channels.c1.transactionCapacity = 100
     # 4 配置 sink
     al.sinks.k1.type = org.apache.flume.sink.kafka.KafkaSink
     al.sinks.k1.kafka.bootstrap.servers
     hadoop102: 9092, hadoop103: 9092, hadoop104: 9092
     al.sinks.k1.kafka.topic = first
     al.sinks.k1.kafka.flumeBatchSize = 20
     al.sinks.k1.kafka.producer.acks = 1
     al.sinks.k1.kafka.producer.linger.ms = 1
    # 5 拼接组件
     a1.sources.r1.channels = c1
     al.sinks.k1.channel = cl
    
    ```

- Flume消费者

  - 举个例子：![截屏2023-09-30 17.17.53](/Users/xiangjianhang/Downloads/LN/Kafka/截屏2023-09-30 17.17.53.png)

  - 关键配置文件：

    ```
    # 1 组件定义
     al.sources = rl
     al.sinks = k1
     al.channels = c1
     # 2 配置 source
     al.sources.rl.type = org.apache.flume.source.kafka.KafkaSource
     al.sources.r1.batchSize = 50
     al.sources.rl.batchDurationMillis = 200
     al.sources.r1.kafka.bootstrap.servers = hadoop102:9092
     al.sources.r1.kafka.topics = first
     al.sources.r1.kafka.consumer.group.id = custom.g.id
     #3配置channel
     al.channels.c1.type = memory
     al.channels.c1.capacity = 1000
     a1.channels.c1.transactionCapacity = 100
     # 4 配置 sink
     al.sinks.k1.type = logger
     # 5 拼接组件
     al.sources.rl.channels = c1
     al.sinks.k1.channel = c1
    ```



## 集成Flink

- Flink生产者：

  - 代码:

  - ```java
     public static void main(String[] args) throws Exception{
    // 1 获取环境
     StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
     env.setParallelism(3);
    // 2 准备数据源
     ArrayList<String> wordlist = new ArrayList<>();
     wordlist.add("hello");
     wordlist.add("atguigu");
     DataStreamSource<String> stream = env.fromCollection(wordlist);
    // 创建一个kafka 生产者
     Properties properties = new Properties();
    properties.put(ProducerConfig.BO0TSTRAP_SERVERS_CONFIG,"hadoop102:9092, hadoop103:9092");
     FlinkkafkaProducer<String> kafkaProducer = new FlinkkafkaProducer<>( topicld: "first", new SimpleStringSchema(), properties);
    //3 添加数据源 kafka生产者
     stream.addSink(kafkaProducer);
    // 4 执行代码
     env.execute();
     }

- Flink消费者

  - 代码

  - ```java
     public static void main(String[] args) {
    // 1 获取环境
     StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
     env.setParallelism(3);
    // 2 创建一个消费者
     Properties properties = new Properties();
     properties.put(ConsumerConfig.B00TSTRAP_SERVERS_CONFIG,"hadoop102:9092, hadoop103:9092");
     properties.put (ConsumerConfig.GROUP_ID_CONFIG,"test");
     FlinkKafkaConsumer<String> kafkaConsumer = new FlinkKafkaConsumer<>( topic: "first", new SimpleStringSchena(), properties);l
    // 3 关联 消费者 和flink流
     env.addSource (kafkaConsumer).print();
    // 4 执行
     env.execute();
     }
    ```

### 集成springboot