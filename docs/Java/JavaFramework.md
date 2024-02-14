# Java Framework

[TOC]

## Mybatis

### 简介

- MyBATIS是一种data mapper，处于类和数据表之间的中间层；把SQL语句的参数（parameter）和返回结果（result）映射至类
- 更好地分离数据库和对象模型的设计，这样就相对减少了两者间的耦合
- 半自动化框架的ORM，需要开发人员掌握SQL语句的编写。不同的数据库要重新修改SQL，因此MyBatis的数据库移植性不好

### 整体架构

![image-20231011234231758](/Users/xiangjianhang/Downloads/LN/JavaFramework/image-20231011234231758.png)

### MyBatis vs Hibernate

- Hibernate 优势
  - DAO 层开发比较简单
  - 对对象的维护和缓存较
  - 数据库移植性好（MyBatis在不同的数据库需要写不同 SQL）
  - 有更好的二级缓存机制，可以使用第三方缓存
- Mybatis优势
  - 可以进行更为细致的 SQL 优化，可以减少查询字段
  - MyBatis 容易掌握，而 Hibernate 门槛较高

### 代码示例

> 核心jar包
>
> ```java
>                                           
> mybatis-3.2.2.jar 核心jar 
> mysql-connector-java-5.1.10-bin.jar 数据库访问 
> asm-3.3.1.jar 增强类 
> cglib-2.2.2.jar 动态代理 
> commons-logging-1.1.1.jar 通用日志 
> javassist-3.17.1-GA.jar java助手 
> log4j-1.2.17.jar 日志 
> slf4j-api-1.7.5.jar 日志 
> slf4j-log4j12-1.7.5.jar 日志
> ```

- 数据库表：Person

  ```sql
  CREATE TABLE PERSON( 
  	PER_ID INT NOT NULL, 
  	PER_FIRST_NAME VARCHAR (40) NOT NULL, 
  	PER_LAST_NAME VARCHAR (40) NOT NULL, 
  	PER_BIRTH_DATE DATETIME , 
  	PER_WEIGHT_KG FLOAT NOT NULL, 
  	PER_HEIGHT_M FLOAT NOT NULL, 
  	PRIMARY KEY (PER_ID) 
  ) 
  
  ```

- Java Bean：Person类

  ```java
                                         /*Person.java */
  package examples.domain; 
  public class Person { 
  	private int id; 
  	private String firstName;   private String lastName; 
  	private Date birthDate; 
  	private double weightInKilograms; 
  	private double heightInMeters; 
  	public int getId () { 
  		return id; 
  	} 
  	public void setId (int id) { 
  		this.id = id; 
  	} 
  	…
  } 
  
  ```

- 映射文件：Person.xml 

  ```xml
                                       Person.xml 
  <?xml version="1.0" encoding="UTF-8" ?>
  <!DOCTYPE mapper
  PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd"> 
  <mapper namespace="cn.mybatis.mapper.Person"> 
        <select id="getPerson" resultType="examples.domain.Person"> 
  	SELECT PER_ID as id, 
  	PER_FIRST_NAME as firstName, 
  	PER_LAST_NAME as lastName, 
  	PER_BIRTH_DATE as birthDate, 
  	PER_WEIGHT_KG as weightInKilograms, 
  	PER_HEIGHT_M as heightInMeters 
  	FROM PERSON 
  	WHERE PER_ID = #{value} 
       </select> 
  </mapper> 
  
  ```

- 配置文件：SqlMapConfig.xml 配置文件也可以是.properties 

  ```xml
                                     SqlMapConfig.xml 
  <environments default="development">
          <environment id="development">
            <transactionManager type="JDBC" > 
            <dataSource type="UNPOOLED"> 
  	<property name="JDBC.Driver" value="com.mysql.jdbc.Driver"/> 
  	<property name="JDBC.ConnectionURL"
                                     value="jdbc:mysql://localhost:3306/mybatisdb"/> 
  	<property name="JDBC.Username" value="root"/> 
  	<property name="JDBC.Password" value=""/> 
           </dataSource> 
  </environment> </environments> 
  <mappers>
  <mappers>
  <mapper resource="cn/mybatis/mapper/Person.xml" />
  <!-- 批量加载mapper
        指定包名，mybatis自动扫描包下边所有mapper接口进行加载
        需将类名和mapper.xml映射文件名称保持一致，且在同一目录中-->
  <package name="cn.mybatis.mapper"/> 
  </mappers>
  
  </configuration> 
  
  
  
  可配置一些额外的属性，大致如下：
  <settings 
  	cacheModelsEnabled ="true"  <!--是否启用缓存机制-- >   
     	lazyLoadingEnabled="true"  <!-- 是否启用延迟加载机制 -->   
    	 enhancementEnabled="true"  <!-- 是否启用字节码增强机制 -->   
    	 errorTracingEnabled="true"  <!-- 是否启用错误处理机制 -->   
     	 maxRequests="32"  <!-- 同时执行SQL语句的最大线程数 -->   
    	 maxSessions="10"  <!-- 最大Session数 -->   
     	 maxTransactions="5"  <!-- 最大并发事务数 -->   
     	useStatementNamespaces="true"/>  <!-- 是否启用名称空间 --> 
  /> 
  
  ```

- 测试代码：MyBatisTest

  ```java
  public static void main(String[] args) {
          try {
              InputStream config = Resources
                      .getResourceAsStream("SqlMapconfig.xml");
              SqlSessionFactory ssf = new SqlSessionFactoryBuilder().build(config);
              SqlSession ss = ssf.openSession();
  // 操作CRUD，第一个参数：指定statement，规则：命名空间+“.”+statementId 
  // 第二个参数：指定传入sql的参数：这里是用户id 
              Person p = ss.selectOne(
                      "com.mybatis.mapper.Person.getPerson", 1);
              System.out.println(mu);
              ss.close();
          } catch (IOException e) {e.printStackTrace();}
      }
  }
  
  ```

- 接口映射器更方便

  ```java
  import examples.domain.Person
  
  public interface PersonDao { 
        public Person getPerson(Integer id); 
        ……
  }
  
  
  
  public static void main(String[] args) {
          try {
              InputStream config = Resources
                      .getResourceAsStream("SqlMapconfig.xml");
              SqlSessionFactory ssf = new SqlSessionFactoryBuilder().build(config);
              SqlSession ss = ssf.openSession();
              PersonDao personDao = ss.getMapper(PersonDao.class);
              Person p = personDao.getPerson(1);
              System.out.println(mu);
              ss.close();
          } catch (IOException e) {e.printStackTrace();}
      }
  }
  
  ```

- CRUD:通常可以进行select\insert\delete\update\statement 

- ```xml
                                       Person.xml 
        
  <mapper namespace="Person"> 
        <select id="getPerson" resultType="examples.domain.Person"> 
  	SELECT PER_ID as id, 
  	PER_FIRST_NAME as firstName, 
  	PER_LAST_NAME as lastName, 
  	PER_BIRTH_DATE as birthDate, 
  	PER_WEIGHT_KG as weightInKilograms, 
  	PER_HEIGHT_M as heightInMeters 
  	FROM PERSON 
  	WHERE PER_ID = #{value} 
       </select> 
  </mapper> 
  
  
                                               Person.xml 
   
  <mapper namespace="Person"> 
        <insert id="insertPerson" parameterType="examples.domain.Person"
             useGeneratedKeys="true" keyProperty="id"> <!--主键自动递增-->
  	INSERT INTO 
  	PERSON (PER_ID, PER_FIRST_NAME, PER_LAST_NAME, 
  	PER_BIRTH_DATE, PER_WEIGHT_KG, PER_HEIGHT_M) 
  	VALUES (#{id}, #{firstName}, #{lastName}, 
  		#{birthDate}, #{weightInKilograms}, #{heightInMeters}) 
       </insert > 
  </mapper> 
  
  
                                               Person.xml 
   
  <mapper namespace="Person"> 
        <update id="updatePerson" parameterType="examples.domain.Person"> 
  	UPDATE PERSON 
  	SET PER_FIRST_NAME = #{firstName}, 
  	PER_LAST_NAME = #{lastName}, 
  	PER_BIRTH_DATE = #{birthDate}, 
  	PER_WEIGHT_KG = #{weightInKilograms}, 
  	PER_HEIGHT_M = #{heightInMeters} 
  	WHERE PER_ID = #{id} 
       </update> 
  </mapper> 
  
  
                                          Person.xml 
   
  <mapper namespace="Person"> 
        <delete id="deletePerson" parameterType="examples.domain.Person"> 
  	DELETE PERSON 
  	WHERE PER_ID = #{id} 
        </delete> 
  </mapper> 
  
  <mapper namespace="Product"> 
        <statement id=”insertTestProduct” > 
              insert into PRODUCT (PRD_ID, PRD_DESCRIPTION) 
                         values (1, “Shih Tzu”) 
        </statement>
  </mapper> 
  
  ```

- 联合查询

  ```xml
  <resultMap id=”get-product-result” class=”com.ibatis.example.Product”> 
  <result property=”id” column=”PRD_ID”/> 
  <result property=”description” column=”PRD_DESCRIPTION”/> 
  <result property=”category.id” column=”CAT_ID” /> 
  <result property=”category.description” column=”CAT_DESCRIPTION” /> 
  </resultMap> 
  <statement id=”getProduct” parameterType=”int” 
                                         resultMap=”get-product-result”> 
          select * 
          from PRODUCT, CATEGORY 
          where PRD_CAT_ID=CAT_ID 
          and PRD_ID = #{value} 
  </statement> 
  
  
  <resultMap id="resultUserArticleList" type="Article">
          <id property="id" column="aid" />
          <result property="title" column="title" />
          <result property="content" column="content" />
          <association property="user" javaType="User">
              <id property="id" column="id" />
              <result property="userName" column="userName" />
              <result property="userAddress" column="userAddress" />       </association>        
      </resultMap>
  < select id="getUserArticles" parameterType="int" resultMap="resultUserArticleList">
       select user.id,user.userName,user.userAddress,article.id aid,article.title,article.content from user,article
                where user.id=article.userid and user.id=#{id}   </select>
  
  ```

## Spring

### spring容器的生命周期 

Spring容器的生命周期是指整个Spring应用程序上下文的生命周期。Spring容器的生命周期包括以下主要阶段：

- **实例化（Instantiation）**：在启动应用程序时，Spring容器会实例化并初始化容器，加载配置文件，创建BeanFactory等。
- **配置（Configuration）**：容器配置阶段，从XML文件、Java配置类或其他配置源中读取Bean定义。
- **初始化（Initialization）**：容器初始化阶段，初始化Bean实例并进行依赖注入。
- **运行（Runtime）**：在容器初始化后，应用程序可以从容器中检索和使用Bean。
- **销毁（Destruction）**：应用程序关闭时，Spring容器会销毁所有Bean，释放资源，执行销毁回调方法。

### springbean的生命周期

**Spring Bean的生命周期**： Spring Bean的生命周期是指单个Bean实例的生命周期，它是Spring容器生命周期的一部分。Bean的生命周期包括以下主要阶段：

- **实例化（Instantiation）**：在容器初始化时，Bean的实例被创建，这通常包括调用构造函数。
- **属性注入（Property Injection）**：容器为Bean注入属性值，如依赖项、配置属性等。
- **自定义初始化方法（Custom Initialization Method）**：如果Bean定义了初始化方法，容器会在属性注入后调用它。
- **Bean可用（Bean Usable）**：Bean实例已被完全初始化，可以在应用程序中使用。
- **自定义销毁方法（Custom Destruction Method）**：如果Bean定义了销毁方法，容器在Bean销毁之前会调用它。
- **销毁（Destruction）**：容器销毁Bean实例，释放资源。

在Bean的生命周期中，你可以使用Spring提供的初始化方法和销毁方法，或者使用注解（如`@PostConstruct`和`@PreDestroy`）来自定义Bean的初始化和销毁过程。这允许你在Bean的生命周期各个阶段执行自定义逻辑。

### 设计模式

#### IOC

IOC（Inversion of Control）是一种设计思想，而不是一个特定的设计模式。它代表了一种控制反转的概念，也叫做依赖注入（Dependency Injection），它将应用程序的控制权从应用程序代码中反转到容器或框架中，实现了松耦合的设计。

虽然IOC本身不是一个特定的设计模式，但它通常与其他设计模式一起使用，以实现更好的代码组织和可维护性。以下是与IOC相关的一些设计模式：

1. **工厂模式**：工厂模式是IOC的一种具体实现方式。在工厂模式中，应用程序不直接实例化对象，而是通过工厂类创建和返回对象。这降低了直接对象创建的控制权，实现了IOC。

2. **依赖注入**：依赖注入是IOC的具体应用，它允许将依赖关系（如其他对象或数值）注入到对象中，而不是在对象内部硬编码依赖。这提高了代码的可测试性和可维护性。

3. **单例模式**：单例模式是一种常见的与IOC结合使用的设计模式。在IOC容器中，单例模式确保某些类的唯一实例被管理和共享。

4. **观察者模式**：观察者模式也与IOC关联紧密，它用于实现发布-订阅模型，其中观察者对象订阅主题对象的事件。IOC容器通常使用观察者模式来通知Bean状态的变化。

总之，虽然IOC本身不是一个设计模式，但它影响了应用程序的设计和架构，使得应用程序更加灵活、可扩展和易于维护。在实际应用中，IOC通常与其他设计模式结合使用，以实现更好的软件工程实践。

#### AOP

AOP（面向切面编程）通常体现了以下设计模式：

1. **装饰器模式（Decorator Pattern）**：AOP可以被视为一种装饰器模式的扩展，其中切面（Aspect）类可以被动态织入到现有对象的方法中，以增加功能。这与装饰器模式类似，但装饰器模式通常用于对象级别的功能增强，而AOP更广泛地用于跨多个对象和方法的功能增强。

2. **策略模式（Strategy Pattern）**：AOP中的切面类本质上是一种策略模式的实现。它定义了在方法执行的不同点上执行的操作，这些操作可以视为策略，而具体方法的调用则是上下文，根据不同的切面策略执行不同的操作。

3. **观察者模式（Observer Pattern）**：AOP中的切面类可以被视为观察者，它们观察方法的执行，并在方法的不同点上触发相应的操作。这是一种观察者模式的变种，用于实现横切关注点的解耦。

总之，AOP在许多方面体现了装饰器、策略和观察者等设计模式的特征，以实现横切关注点的模块化和可维护性。这种模式的主要目标是将与核心业务逻辑无关的横切关注点（如日志、事务管理、安全性）从核心业务逻辑中分离出来，从而提高代码的可读性和可维护性。

### 事务实现

Spring框架实现事务的方式主要包括编程式事务管理和声明式事务管理。Spring事务管理建立在底层的事务抽象之上，它支持多种不同的事务管理器和事务传播行为，以满足不同应用场景的需求。

1. **编程式事务管理**：编程式事务管理是通过编写代码显式地管理事务的提交和回滚。Spring提供了`PlatformTransactionManager`接口作为事务管理器的抽象。开发人员可以使用这些事务管理器（如`DataSourceTransactionManager`、`HibernateTransactionManager`等）编写代码以开启、提交和回滚事务。

   示例代码（基于编程式事务管理的Spring事务管理方式）：

   ```java
   TransactionDefinition def = new DefaultTransactionDefinition();
   TransactionStatus status = transactionManager.getTransaction(def);

   try {
       // 执行业务逻辑
       // ...
       transactionManager.commit(status);
   } catch (Exception e) {
       transactionManager.rollback(status);
   }
   ```

2. **声明式事务管理**：声明式事务管理是通过在配置中声明事务的属性来管理事务。Spring提供了`@Transactional`注解，可以应用到方法或类上，以指示哪些方法需要进行事务管理。Spring AOP会自动处理事务的开启、提交和回滚。

   示例代码（基于声明式事务管理的Spring事务管理方式）：

   ```java
   @Service
   public class MyService {
       @Autowired
       private MyRepository repository;
   
       @Transactional
       public void performBusinessOperation() {
           // 执行业务逻辑
           // ...
       }
   }
   ```

Spring框架提供了不同的事务管理器（如JDBC、Hibernate、JPA、JTA等）来适应不同的数据访问技术。开发人员可以根据应用的需要选择合适的事务管理器。

Spring的事务管理还支持不同的事务传播行为，如REQUIRED、REQUIRES_NEW、NESTED等，以定义方法之间的事务关系。这些特性使得Spring事务管理非常强大和灵活，适用于各种不同的应用场景。