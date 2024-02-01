# SpringBoot

>  笔记: https://www.yuque.com/leifengyang/springboot3
>  代码: https://gitee.com/leifengyang/spring-boot-3

## SpringBoot3核心特性

### 1. 快速入门

### 1.1 SpringBoot是什么

SpringBoot 帮我们简单、快速地创建一个独立的、生产级别的 Spring 应用大多数 SpringBoot 应用只需要编写少量配置即可快速整合 Spring 平台以及第三方技术

特性：

- 快速创建独立 Spring 应用
  - SSM：导包、写配置、启动运行
- 直接嵌入Tomcat, Jetty or Undertow (无需部署 war 包) 【Servlet容器】
  -  linux java tomcat mysql: war 放到 tomcat 的webapps下
  -   jar: java环境; java -jar
- 重点：提供可选的starter，简化应用整合
  - 场景启动器（starter）：web、json、邮件、oss（对象存储）、异步、定时任务、缓存…..
  - 以前：导包一堆，控制好版本。
  - 现在：为每一种场景准备了一个依赖： web-starter, mybatis-starter
  - 无代码生成、无xml
- 总结：简化开发，简化配置，简化整合，简化部署，简化监控，简化运维。

##  SpringBoot3场景实战

###  Docker快速入门

###  NoSOL
接口文档
远程调用
消息服务
Web安全
可观测性
 AOT

## 响应式编程全套

 Reactor核心
 Spring-WebFlux(响应式Web)

 Spring Data R2DBC（响应式数据库）
Spring Data Reactive Redis（响应式NoSQL） 

Spring Security Reactive（响应式安全）