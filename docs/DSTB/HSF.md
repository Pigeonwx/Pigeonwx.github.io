# 产品概述

HSF（High-speed Service Framework，高速服务框架）是一款在阿里巴巴内部广泛使用的分布式 RPC 服务框架。HSF 作为阿里巴巴的基础中间件，能够联通不同的业务系统，解耦系统间的实现依赖。该框架统一了分布式应用层面的服务发布和调用方式，从而帮助用户便捷地开发和使用分布式应用与公共功能模块。同时，HSF 还屏蔽了诸如远程通讯、序列化实现、性能损耗、同步/异步调用方式实现等分布式领域中的复杂技术细节。

## 架构

作为一个纯客户端架构的 RPC 框架，HSF 本身没有服务端集群。所有 HSF 服务调用均是服务消费方（Consumer）与服务提供方（Provider）点对点进行的。为了实现整套分布式服务体系，HSF 还需要依赖一些外部系统来提供额外的功能。

![hsf_architecture_优化](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/DSTB/HSF/hsf_architecture_优化.png)

### 地址注册中心

地址注册中心用于服务发现功能。没有注册中心的话，HSF 只能完成简单的点对点调用。注册中心的存在使得服务提供端可以将自己的服务信息发布出去，服务消费端也可以从中获取需要调用的服务的机器信息。在阿里巴巴内部，地址注册中心是由 ConfigServer 承担的。

### 持久化配置中心

持久化配置中心用于存储 HSF 服务的治理规则。HSF 客户端在启动时会从配置中心订阅各种服务治理规则（如路由规则、归组规则、权重规则等），并根据这些规则对调用过程进行干预。在阿里巴巴内部，持久化配置中心的角色是由 Diamond 承担的。

### 元数据存储中心

元数据包含了 HSF 服务对应的方法列表和参数结构等信息。虽然元数据不会对 HSF 的调用过程产生直接影响，但为提高运维便捷性，HSF 客户端在启动时会将元数据上报到元数据存储中心，供运维使用。在阿里巴巴内部，元数据存储中心由 Redis 承担。

### HSF 控制台

[HSF 控制台](https://hsf.alibaba-inc.com/hsfops/v2)提供了一系列服务运维功能，包括服务查询、服务治理规则管理、服务测试、服务 Mock 及单机运维等，旨在提高 HSF 服务的研发效率和运维便捷性。

- 服务查询：提供多种维度的服务查询功能，展示服务的实时状态。
- 服务治理：提供管理路由规则、归组规则、同机房规则、权重规则等多种服务治理规则，帮助用户完成服务集群的管理与流量划分。
- 服务测试：提供快速测试和调用服务的能力，通过页面输入参数即可完成一次 HSF 服务调用，提高研发效率。
- 服务 Mock：提供 HSF 服务的 Mock 能力，无需关注服务端是否存在，只需在 HSFOPS 上配置好 Mock 规则，即可通过 hsf-mock 插件获取配置的 Mock 数据，无需修改代码。

## 应用场景

HSF 适用于希望进行服务化改造的应用，将单个巨型应用拆分成多个职责分明的基础服务应用，并将其提供给更多上层应用使用。如果你的应用希望实现这一目标，HSF 将会是最佳选择。

# 基于 API 方式部署 HSF 服务

## 快速入门

本文将向初次使用 HSF 的用户介绍如何快速的发布一个服务，以及如何通过远程调用消费这个服务。全文共包含以下内容：

1. 运行环境
2. 服务的定义与实现
3. 发布 HSF 服务
4. 消费 HSF 服务

## 1. 运行环境

- JDK >= 8
- Maven >= 3

## 2. 添加 Maven 依赖

HSF 最新版本请在 [artlab](https://artlab.alibaba-inc.com/GAResult?GroupId=com.taobao.hsf&Artifact=hsf-all) 中查看。

```xml
<dependency>
    <groupId>com.taobao.hsf</groupId>
    <artifactId>hsf-all</artifactId>
    <version>3.1.20</version>
</dependency>
```



## 3. 服务的定义与实现

**“服务” 始于接口的定义，首先需要根据业务逻辑定义好服务接口。**

在日常开发中，一般会将服务的接口定义在一个工程中，它会被打成一个 jar 包，发布到 maven 仓库中。服务端实现 jar 包中的接口，通过 HSF 发布对应的服务；而消费端通过依赖这个 jar 包，透过 HSF 远程调用消费到服务端的接口实现。

> 本文中的代码工程范例，可以在 [hsf-guide](http://gitlab.alibaba-inc.com/middleware-container/hsf-guide/tree/develop) 中获取。

### 3.1 定义服务接口

本文目的在于快速的展示 HSF 的使用方法，因此仅定义一个非常简单的 `HelloWorldService` 用于演示，并将它放在 `hsf-guide-api` 这个工程中。

```java
public interface HelloWorldService {

    /**
     * 根据参数中指定的名字，生成问候语
     *
     * @param name 被问候的姓名
     * @return 问候语
     */
    String sayHi(String name);
}
```



### 3.2 编写服务实现

在完成服务接口的定义后，服务提供方需根据业务逻辑实现接口。添加服务 `HelloWorldService` 的实现类 `HelloWorldServiceImpl` 。

```java
public class HelloWorldServiceImpl implements HelloWorldService {

    @Override
    public String sayHi(String name) {
        if (name == null || name.length() == 0) {
            return null;
        }
        return "Hi, " + name + "! Welcome to the HSF world.";
    }
}
```



在范例中，`HelloWorldService` 的业务逻辑很简单：若 name 不为空，则使用 name 生成问候语并返回；否则，返回 `null`。

至此，服务提供方实现代码编写完成。

## 4. 发布 HSF 服务

根据服务接口定义 `HelloWorldService` 完成本地服务 `HelloWorldServiceImpl` 的实现后，只需要将这个服务通过 HSF 发布出去，就可以让其他 HSF 客户端通过远程调用消费到当前机器的服务了。

在 main 函数中通过装配 `HSFApiProviderBean` 将发布服务 `HelloWorldService` ：

```java
HSFApiProviderBean hsfApiProviderBean = new HSFApiProviderBean();

// [设置] 发布服务的接口
hsfApiProviderBean.setServiceInterface("com.alibaba.middleware.hsf.guide.api.service.HelloWorldService");
// [设置] 服务的实现对象，target 为 HelloWorldServiceImpl 的实例
hsfApiProviderBean.setTarget(target);
// [设置] 服务的版本
hsfApiProviderBean.setServiceVersion("1.0.0");
// [设置] 服务的组别
hsfApiProviderBean.setServiceGroup("HSF");
// [设置] 服务的响应时间
hsfApiProviderBean.setClientTimeout(5000);
// [设置] 服务传输业务对象时的序列化类型
hsfApiProviderBean.setPreferSerializeType("hessian2");

// [发布] HSF服务
hsfApiProviderBean.init();
```



以上配置中，`serviceInterface`, `version`, `serviceGroup` 三者构成了 HSF 中最为关键概念：

- **服务名：** 即 `serviceInterface`:`version`
- **组别：** 即 `serviceGroup`

**服务名和组别唯一决定了服务的发布、订阅关系。**

> 除了 API 的方式外，HSF 还支持 SpringBoot 注解方式配置、发布服务，具体请参考 [用户指南 - 发布服务](https://mw.alibaba-inc.com/hsf/quick-start/qs-api) 这一小节。

启动 main 函数后，可在 [日常 HSFOPS 控制台](https://hsf.alibaba.net/hsfops/v2/service/query?dataId=com.alibaba.hsf.demo.DemoService*) 查询到发布的服务和机器。

![image.png](https://mw.alibaba-inc.com/assets/images/img-6a6c785fbb8d391495d89a33c3d117ca.png)

## 4. 消费 HSF 服务

现在，服务接口定义的 jar 包已经 deploy 到 maven 仓库，HSF 服务也已经发布成功了，接下来服务的客户端只需要依赖接口定义，并引入 HSF 就可以消费远程的 `HelloWorldService` 服务了。

### 4.1 添加服务接口依赖

创建 `hsf-guide-client` 工程，作为客户端消费服务的工程。

客户端在消费服务前，首先需要向服务提供方咨询服务接口定义 jar 包的 maven 坐标，在本文中，即 `hsf-guide-api` 的坐标：

```xml
<dependency>
    <groupId>com.alibaba.middleware</groupId>
    <artifactId>hsf-guide-api</artifactId>
    <version>1.0.0-SNAPSHOT</version>
</dependency>
```



### 4.3 配置并消费 HSF 服务

在 main 函数中通过装配 `HSFApiConsumerBean` 订阅服务 `HelloWorldService`，并在初始化完成后，像调用本地代码一样，通过代理调用远程的 HSF 服务：

```java
HSFApiConsumerBean hsfApiConsumerBean = new HSFApiConsumerBean();

// [设置] 订阅服务的接口
hsfApiConsumerBean.setInterfaceName("com.alibaba.middleware.hsf.guide.api.service.HelloWorldService");
// [设置] 服务的版本
hsfApiConsumerBean.setVersion("1.0.0");
// [设置] 服务的组别
hsfApiConsumerBean.setGroup("HSF");

// [订阅] HSF 服务，同步等待地址推送，默认 false (异步)，同步默认超时时间 3000 毫秒
hsfApiConsumerBean.init(true);

// [代理] 获取 HSF 代理
HelloWorldService helloWorldService = (HelloWorldService) hsfApiConsumerBean.getObject();

// [调用] 像调用本地接口一样，发起 HSF 调用
String hi = helloWorldService.sayHi("BingYuan");
System.out.println(hi);
```



> 除了 API 的方式外，HSF 还支持 SpringBoot 注解方式配置、消费服务，具体请参考 [用户指南 - 编写调用端](https://mw.alibaba-inc.com/hsf/quick-start/qs-api) 这一小节。

`HSFApiConsumerBean` 构建完成后，HSF 就会根据代码中设置的服务名（interfaceName: version）和组别（group）订阅服务的地址，并在发起调用时，随机选取其中的一个服务提供方执行远程调用。

在服务提供方启动的状态下，运行上述代码，将会输出：

```jsx
Hi,BingYuan ! Welcome to the HSF world.
```



至此，`HelloWorldService` 这个服务的发布与消费过程，就全部完成了。

## 5. 总结

本文以 `HelloWorldService` 服务为例，介绍了如何定义、编写、发布、消费 HSF 服务的完整过程，所有源码都可以在 [hsf-guide](http://gitlab.alibaba-inc.com/middleware-container/hsf-guide/tree/develop) 工程中下载。

# 基于 SpringBoot 部署 HSF 服务

本文介绍如何在不接入 Pandora 的情况下使用 SpringBoot 部署 HSF 服务。

推荐优先参考 [基于 PandoraBoot 部署 HSF 服务](https://mw.alibaba-inc.com/hsf/quick-start/qs-pandora)，接入 Pandora 部署 HSF 服务。

## 1. 添加 Maven 依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>jcl-over-slf4j</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-test</artifactId>
        <scope>test</scope>
    </dependency>

    <!-- hsf -->
    <dependency>
        <groupId>com.taobao.hsf</groupId>
        <artifactId>hsf-all</artifactId>
        <version>3.1.20</version>
    </dependency>
</dependencies>
```



## 2. 代码实现

### 2.1 SpringBoot 启动类

```java
package com.taobao.hsf;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {"com.taobao.hsf"})
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```



### 2.2 服务接口与实现

```java
package com.taobao.hsf.api;

public interface HelloWorldService {

    String sayHi(String name);
}
```



直接在服务实现类上添加 `@HSFProvider` 注解，指定服务接口、版本号和分组，即可发布服务。不指定 BeanName 的情况下，HSFProviderBean 在 Spring 中默认的 BeanName 为 HSFProvider-helloWorldServiceImpl。

```java
package com.taobao.hsf.api;

import com.taobao.hsf.app.spring.util.annotation.HSFProvider;

@HSFProvider(serviceInterface = HelloWorldService.class, serviceVersion = "1.0.0", serviceGroup = "HSF")
public class HelloWorldServiceImpl implements HelloWorldService{

    @Override
    public String sayHi(String name) {
        if (name == null || name.length() == 0) {
            return null;
        }
        return "Hi, " + name + "! Welcome to the HSF world.";
    }
}
```



SpringBoot 应用要直接使用 `com.taobao.hsf.app.spring.util.annotation.HSFProvider` 注解需要配置 HSF 的 BeanFactoryPostProcessor

```java
package com.taobao.hsf.config;

import com.taobao.hsf.app.spring.util.consumer.HSFConsumerSpringPostProcessor;
import com.taobao.hsf.app.spring.util.provider.HSFProviderSpringPostProcessor;
import org.springframework.beans.factory.config.BeanFactoryPostProcessor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HSFConfig {

    @Bean
    public BeanFactoryPostProcessor hsfProviderBeanFactoryPostProcessor() {
        return new HSFProviderSpringPostProcessor();
    }

    @Bean
    public BeanFactoryPostProcessor hsfConsumerBeanFactoryPostProcessor() {
        return new HSFConsumerSpringPostProcessor();
    }
}
```



### 2.3 消费端代码

通常一个 HSF Consumer 需要在多个地方使用，但并不需要在每次使用的地方都用 @HSFConsumer 来标记。

只需要写一个统一个 Config 类来注册到 Spring 容器，然后在其它需要使用的地方，直接@Autowired 注入即可。

HSFConsumerBean 在 Spring 中默认的 BeanName 为 HSFConsumer-helloWorldService，为了便于注入，这里指定 BeanName 为 helloWorldService。

```java
package com.taobao.hsf.consumer;

import com.taobao.hsf.api.HelloWorldService;
import com.taobao.hsf.app.spring.util.annotation.HSFConsumer;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HSFConsumerConfig {

    @HSFConsumer(consumerBeanName = "helloWorldService", serviceVersion = "1.0.0", serviceGroup = "HSF")
    private HelloWorldService helloWorldService;
}
```



## 3. 发起调用

本地启动 Demo 成功后，可以在 [HSFops 控制台](https://hsf.alibaba.net/hsfops/v2/service/query) 日常环境中查询到服务，可以通过控制台服务测试功能对服务进行调用。

本文通过本地 Spring 单测的形式来执行一次调用。

```java
import com.taobao.hsf.Application;
import com.taobao.hsf.api.HelloWorldService;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(classes = { Application.class })
public class HsfTest {

    @Autowired
    private HelloWorldService helloWorldService;

    @Test
    public void testInvoke() {
        TestCase.assertEquals("Hi, pandora boot! Welcome to the HSF world.", helloWorldService.sayHi("pandora boot"));
    }

}
```



## 4. 示例目录结构

```shell
.
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── taobao
    │   │           └── hsf
    │   │               ├── Application.java
    │   │               ├── api
    │   │               │   ├── HelloWorldService.java
    │   │               │   └── HelloWorldServiceImpl.java
    │   │               ├── config
    │   │               │   └── HSFConfig.java
    │   │               └── consumer
    │   │                   └── HSFConsumerConfig.java
    │   └── resources
    └── test
        └── java
            └── HsfTest.java
```



在实际项目中，消费方需要通过二方包的形式引入服务提供方的服务接口，以便在消费方中调用服务。