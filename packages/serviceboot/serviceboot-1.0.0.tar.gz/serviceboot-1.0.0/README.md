# ServiceBoot —— CUBE-Net微服务引擎

ServiceBoot是基于Tornado开发的开源微服务引擎，用于将普通Python程序封装成为可提供高并发HTTP API访问的云原生微服务，是构成和开发[CUBE-Net微服务框架](https://gitee.com/cubenet/cubenet)的核心组件。

ServiceBoot实现了对高并发HTTP API调用的函数化和异步化封装。开发者直接以普通Python函数的形式来编程API接口，不需要特意设计和指定每个API对应的URL端口，也不需要掌握和使用Python和Tornado中晦涩难懂的异步编程原理和语法，即可达到高效并发处理的性能和效果，从而大大降低微服务应用的学习门槛和开发难度，提高云原生应用的开发效率和运行性能。

ServiceBoot目前可提供的API接口类型和功能如下：

- RESTful API（面向JSON数据格式）。
- 二进制数据API。
- 文件上传API。
- 可视化Web页面访问API。
- Special API。
- WebSocket实时通信API。
- HTTP API网关功能支持。

## 依赖包地址 

- https://pypi.org/project/serviceboot

## 依赖包引用

    pip install serviceboot -i https://pypi.tuna.tsinghua.edu.cn/simple

## CUBE-Net微服务框架

CUBE-Net微服务框架是基于ServiceBoot开发的一套云原生微服务框架。参见：

- https://gitee.com/cubenet/cubenet
