

# 一次完整的HTTP请求过程



DNS解析  ->  网络连接  ->  发起HTTP请求  ->  服务端响应  ->  页面渲染



### DNS解析

> [**域名系统**](https://zh.wikipedia.org/wiki/域名系统)（英语：**D**omain **N**ame **S**ystem，缩写：**DNS**）是互联网的一项服务。它作为将域名和IP地址相互映射的一个分布式数据库，能够使人更方便地访问互联网。DNS使用TCP和UDP端口。当前，对于每一级域名长度的限制是63个字符，域名总长度则不能超过253个字符

![](.assets/%E5%9F%9F%E5%90%8D%E7%BB%93%E6%9E%84%E8%A7%A3%E6%9E%90.png)

<center>域名结构解析图</center>

1. 浏览器DNS缓存 
   - chrome查看浏览器DNS缓存：`chrome://net-internals/#dns`
2. 系统DNS缓存
   - win查看DNS缓存： `ipconfig /displaydns` 
   - win清除DNS缓存：`ipconfig /flushdns` 
3. host文件
   - win: `C:\Windows\System32\drivers\etc\hosts` 
   - linux: `/etc/hosts` 
4. DNS服务器
   - DNS查询有2种方式：**递归**和**迭代**，DNS客户端设置使用的DNS服务器一般都是递归服务器，它负责全权处理客户端的DNS查询请求，直到返回最终结果。而DNS服务器之间一般采用迭代查询方式。
   - 以查询 www.wenjuan.com 为例：
     - 客户端发送查询报文"query www.wenjuan.com"至DNS服务器，DNS服务器首先检查自身缓存，如果存在记录则直接返回结果。
     - 如果记录老化或不存在，则：
       1. DNS服务器向根域名服务器发送查询报文"query www.wenjuan.com"，根域名服务器返回顶级域 .com 的顶级域名服务器地址。
       2. DNS服务器向 .com 域的顶级域名服务器发送查询报文"query www.wenjuan.com"，得到二级域 .wenjuan.com 的权威域名服务器地址。
       3. DNS服务器向 .wenjuan.com 域的权威域名服务器发送查询报文"query www.wenjuan.com"，得到主机 www 的A记录，存入自身缓存并返回给客户端。

小思考：DNS解析的过程使用的是TCP还是UDP协议，DNS劫持的原理是什么？

------

### 网络连接

<img src=".assets/%E6%8B%93%E6%89%91%E5%9B%BE.png" style="zoom:50%;" />

<center>网络拓扑图</center>

- ARP

> [**地址解析协议**](https://zh.wikipedia.org/zh-cn/地址解析协议)（英语：Address Resolution Protocol，缩写：ARP）是一个通过解析网络层地址来找寻数据链路层地址的网络传输协议，它在IPv4中极其重要。ARP最初在1982年的RFC 826（征求意见稿）中提出并纳入互联网标准STD 37。

- MAC地址

  > [**MAC地址**](https://zh.wikipedia.org/wiki/MAC%E5%9C%B0%E5%9D%80)（**英语：Media Access Control Address）**，直译为**媒体存取控制地址**，也称为**局域网地址**（LAN Address），**以太网地址**（Ethernet Address）或**物理地址**（Physical Address），它是一个用来确认网络设备位置的地址。在OSI模型中，第三层网络层负责IP地址，第二层数据链接层则负责MAC地址。MAC地址用于在网络中唯一标示一个网卡，一台设备若有一或多个网卡，则每个网卡都需要并会有一个唯一的MAC地址。

- IP地址

  > [**IP地址**](https://zh.wikipedia.org/wiki/IP%E5%9C%B0%E5%9D%80)（英语：IP Address，全称Internet Protocol Address），又译为**网际协议地址**、**互联网协议地址**。是网际协议中用于标识**发送**或**接收数据报**的设备的一串数字

以主机A（192.168.38.10）向主机B（192.168.38.11）发送数据为例。

1. 当发送数据时，主机A会在自己的ARP缓存表中寻找是否有目标IP地址。如果找到就知道目标MAC地址为（00-BB-00-62-C2-02），直接把目标MAC地址写入帧里面发送就可。
2. 如果在ARP缓存表中没有找到相对应的IP地址，主机A就会在网络上发送一个广播（ARP request），目标MAC地址是“FF.FF.FF.FF.FF.FF”，这表示向同一网段内的所有主机发出这样的询问：“192.168.38.11的MAC地址是什么？”
3. 网络上其他主机并不响应ARP询问，只有主机B接收到这个帧时，才向主机A做出这样的回应（ARP response）：“192.168.38.11的MAC地址是00-BB-00-62-C2-02”，此回应以单播方式进行。这样，主机A就知道主机B的MAC地址，它就可以向主机B发送信息。同时它还更新自己的ARP高速缓存（ARP cache），下次再向主机B发送信息时，直接从ARP缓存表里查找就可。

小思考： 为什么有了MAC地址还需要IP？ 

- TCP

  > [**传输控制协议**](https://zh.wikipedia.org/wiki/传输控制协议)（英语：**T**ransmission **C**ontrol **P**rotocol，缩写：**TCP**）是一种面向连接的、可靠的、基于字节流的传输层通信协议，由IETF的RFC 793定义。在简化的计算机网络[OSI模型](https://zh.wikipedia.org/wiki/OSI模型)中，它完成第四层传输层所指定的功能。[用户数据报协议](https://zh.wikipedia.org/wiki/用户数据报协议)（UDP）是同一层内另一个重要的传输协议

  TCP三次握手与四次挥手

  <img src=".assets/%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B.png" style="zoom:50%;" />

  <center>三次握手</center>

<img src=".assets/%E5%9B%9B%E6%AC%A1%E6%8C%A5%E6%89%8B.png" style="zoom:50%;" />

<center>四次挥手</center>

小思考：TCP粘包是什么，如何解决

------

### 发起HTTP请求

- HTTP

  > [**超文本传输协议**](https://zh.wikipedia.org/wiki/%E8%B6%85%E6%96%87%E6%9C%AC%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE)（英语：**H**yper**T**ext **T**ransfer **P**rotocol，缩写：**HTTP**）是一种用于分布式、协作式和超媒体信息系统的应用层协议

  - HTTP请求

    http请求由请求行，消息报头，请求正文三部分构成

    ![](./%E4%B8%80%E6%AC%A1%E5%AE%8C%E6%95%B4%E7%9A%84HTTP%E8%AF%B7%E6%B1%82%E8%BF%87%E7%A8%8B.assets/HTTP%E8%AF%B7%E6%B1%82.png)

    <center>http请求内容</center>

  - 请求方法

    - GET(常用)：向指定的资源发出“显示”请求。使用GET方法应该只用在读取资料，而不应当被用于产生“副作用”的操作中
    - HEAD：与GET方法一样，都是向服务器发出指定资源的请求。只不过服务器将不传回资源的本文部分
    - POST(常用)：向指定资源提交数据，请求服务器进行处理（例如提交表单或者上传文件）。数据被包含在请求本文中。这个请求可能会创建新的资源或修    改现有资源，或二者皆有。每次提交，表单的数据被浏览器用编码到HTTP请求的body里。浏览器发出的POST请求的body主要有两种格式，一种是application/x-www-form-urlencoded用来传输简单的数据，大概就是"key1=value1&key2=value2"这样的格式。另外一种是传文件，会采用multipart/form-data格式。采用后者是因为application/x-www-form-urlencoded的编码方式对于文件这种二进制的数据非常低效
    - PUT：向指定资源位置上传其最新内容
    - DELETE：请求服务器删除Request-URI所标识的资源
    - TRACE：回显服务器收到的请求，主要用于测试或诊断
    - OPTIONS：这个方法可使服务器传回该资源所支持的所有HTTP请求方法
    - CONNECT：HTTP/1.1协议中预留给能够将连接改为隧道方式的代理服务器。通常用于SSL加密服务器的链接（经由非加密的HTTP代理服务器）

  - HTTP响应

    HTTP响应由状态行，消息报头，响应正文构成

    <img src=".assets/HTTP%E5%93%8D%E5%BA%94.png" style="zoom:35%;" />

    <center>http返回内容</center>

  - 常用状态码

    - 200：请求成功

    - 301：重定向，永久移动

    - 302：重定向，临时移动

    - 400：客户端语法错误

    - 401：请求要求用户身份认证

    - 403：服务器理解请求客户端的请求，但是拒绝执行

    - 404：服务器无法根据客户端的请求找到资源

    - 405：客户端请求中的方法被禁止

    - 422：服务器理解请求实体的内容类型，并且请求实体的语法是正确的，但是服务器无法处理包含的指令

    - 500：服务端错误的响应，意味着服务器遇到意外的情况并阻止请求

    - 502：网关或代理服务器从上游服务器中接收到的响应是无效的

    - 503：服务器尚未处于可以接受请求的状态

    - 504：网关或代理服务器无法在规定的时间内获得想要的响应

      ![](.assets/%E7%8A%B6%E6%80%81%E7%A0%81%E6%80%BB%E7%BB%93.png)

      <center>错误码总结</center>

  - HTTPS

    HTTPS = HTTP + SSL/TLS

    HTTPS的信任基于预先安装在操作系统中的证书颁发机构（CA）。因此，与一个网站之间的HTTPS连线仅在这些情况下可被信任：

    - 浏览器正确地实现了HTTPS且操作系统中安装了正确且受信任的证书颁发机构；
    - 证书颁发机构仅信任合法的网站；
    - 被访问的网站提供了一个有效的证书，也就是说它是一个由操作系统信任的证书颁发机构签发的（大部分浏览器会对无效的证书发出警告）；
    - 该证书正确地验证了被访问的网站（例如，访问`https://example.com`时收到了签发给`example.com`而不是其它域名的证书）；
    - 此协议的加密层（SSL/TLS）能够有效地提供认证和高强度的加密。

- 反向代理

  > [**反向代理**](https://zh.wikipedia.org/wiki/%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86)（**Reverse proxy**）在电脑网络]中是代理服务器的一种。服务器根据客户端的请求，从其关系的一组或多组后端服务器（如Web服务器）上获取资源，然后再将这些资源返回给客户端，客户端只会得知反向代理的IP地址，而不知道在代理服务器后面的服务器集群的存在

  ![](.assets/%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86.png)

  <center>反向代理</center>

  反向代理的主要作用为：

  - 对客户端隐藏服务器（集群）的IP地址
  - 安全：作为应用层防火墙为网站提供对基于Web的攻击行为（例如DoS/DDoS）的防护，更容易排查恶意软件等
  - 为后端服务器（集群）统一提供加密和SSL加速（如SSL终端代理）
  - 负载均衡，若服务器集群中有负荷较高者，反向代理通过URL重写，根据连线请求从负荷较低者获取与所需相同的资源或备援
  - 对于静态内容及短时间内有大量访问请求的动态内容提供缓存服务
  - 对一些内容进行压缩，以节约带宽或为网络带宽不佳的网络提供服务
  - 减速上传
  - 为在私有网络下（如局域网）的服务器集群提供NAT穿透及外网发布服务
  - 提供HTTP访问认证
  - 突破互联网封锁

- 负载均衡

  > **负载平衡**（英语：load balancing）是一种电子计算机技术，用来在多个计算机（计算机集群）、网络连接、CPU、磁盘驱动器或其他资源中分配负载，以达到优化资源使用、最大化吞吐率、最小化响应时间、同时避免过载的目的。 使用带有负载平衡的多个服务器组件，取代单一的组件，可以通过冗余提高可靠性。负载平衡服务通常是由专用软件和硬件来完成。 主要作用是将大量作业合理地分摊到多个操作单元上进行执行，用于解决互联网架构中的高并发和高可用的问题

  Nginx负载均衡策略

  - 轮询：轮询是upstream的默认分配方式，即每个请求按照时间顺序轮流分配到不同的后端服务器，如果某个后端服务器down掉后，能自动剔除

    ```nginx
    upstream backend {
        server 192.168.0.1:8080;
        server 192.168.0.2:8080;
    }
    ```

  - 加权轮询：轮询的加强版，即可以指定轮询比率，weight和访问几率成正比，主要应用于后端服务器异质的场景下

    ```nginx
    upstream backend {
        server 192.168.0.1:8080 weight=1;
        server 192.168.0.2:8080 weight=2;
    }
    ```

  - ip_hash：每个请求按照访问ip（即Nginx的前置服务器或者客户端IP）的hash结果分配，这样每个访客会固定访问一个后端服务器，可以解决session一致问题

    ```nginx
    upstream backend {
        ip_hash;
        server 192.168.0.1:8080;
        server 192.168.0.2:8080;
    }
    ```

  - fair：公平地按照后端服务器的响应时间（rt）来分配请求，响应时间短即rt小的后端服务器优先分配请求

    ```nginx
    upstream backend {
        server 192.168.0.1:8080;
        server 192.168.0.2:8080;
        fair;
    }
    ```

  - url_hash： 与ip_hash类似，但是按照访问url的hash结果来分配请求，使得每个url定向到同一个后端服务器，主要应用于后端服务器为缓存时的场景下

    ```nginx
    upstream backend {
        server 192.168.0.1:8080;
        server 192.168.0.2:8080;
        hash $request_uri;
        hash_method crc32;
    }
    ```

小思考： HTTP必须使用TCP协议么？ 

拓展阅读：https://www.zhihu.com/question/302412059/answer/533223530

------

### 服务器响应HTTP请求

<img src=".assets/Django%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.png" style="zoom:70%;" />

<center>Django生命周期</center>

- 路由

  简单来说，路由就是URL到函数的映射

- 中间件

  ```python 
  def add_middlewares(app: App) -> App:
      app.add_middleware(SignatureHandleMiddleware)
      app.add_middleware(ExceptionHandleMiddleware)
      app.add_middleware(
          CORSMiddleware,
          allow_origins="*",
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
      logger.info("app middleware added")
      return app
  
  
  class ExceptionHandleMiddleware(BaseHTTPMiddleware):
      def __init__(self, app):
          super().__init__(app)
  
      async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
          try:
              response = await call_next(request)
          except ValidationError as e:
              logger.error(e)
              return make_param_invalid_response()
          except (APIException, ApplicationException) as e:
              logger.error(e)
              return make_api_exception_response(e)
          except HTTPException as e:
              logger.error(e)
              return make_internal_error_response()
          return response
  ```

  简单来说，中间件是一种可以接入request和response对象的函数。所谓中间，源于中间件函数位于request和response生命周期的中间，中间件可以直接接入request和response两个对象和将控制权限传递给下一个中间件。

  它具有如下特性：

  - 可执行任意代码
  - 对request和response对象做修改
  - 可随时结束request-response生命周期
  - 在request-response生命周期的stack中调用next中间件

- 缓存

  **商业世界里，现金为王；架构世界里，缓存为王**

  我们常说的缓存，根据资源存放位置、具体用途和运行机制不同，一般可以分为：

  - 数据库缓存

  - 服务器缓存

  - 客户端缓存

    ![](.assets/%E7%BC%93%E5%AD%98%E5%88%86%E7%B1%BB.png)

    <center>不同的缓存类型</center>

  web缓存的优缺点

  优点：

  - 减少网络延迟，提升用户体验
  - 减少数据传输，节省网络带宽和流量
  - 减轻服务器压力
  - 提升系统性能

  缺点：

  - 额外的硬件支出
  - 高并发下缓存失效
  - 缓存造成的数据同步问题

- 数据库

  > [**数据库**](https://zh.wikipedia.org/zh-cn/%E6%95%B0%E6%8D%AE%E5%BA%93)，简而言之可视为电子化的文件柜——存储电子文件的处所，用户可以对文件中的资料执行新增、截取、更新、删除等操作

  - 索引是什么

    数据库索引好比是一本书前面的目录，能加快数据库的查询速度。索引是对数据库表中一个或多个列（例如，User 表的 '姓名' 列）的值进行排序的结构。如果想按特定用户的姓名来查找他或她，则与在表中搜索所有的行相比，索引有助于更快地获取信息

  - 索引的优点：

    - 大大加快数据的检索速度;

    - 创建唯一性索引，保证数据库表中每一行数据的唯一性;

    - 加速表和表之间的连接;

    - 在使用分组和排序子句进行数据检索时，可以显著减少查询中分组和排序的时间。

  - 索引的缺点：

    - 索引需要占用数据表以外的物理存储空间

    - 创建索引和维护索引要花费一定的时间
    - 当对表进行更新操作时，索引需要被重建，这样降低了数据的维护速度

  - 索引的类型：

    - 哈希表

      <img src=".assets/%E5%93%88%E5%B8%8C%E8%A1%A8.png" style="zoom:80%;" />

    - 有序数组

      <img src=".assets/%E6%9C%89%E5%BA%8F%E6%95%B0%E7%BB%84.png" style="zoom:80%;" />

    - 搜索树

      <img src=".assets/%E6%90%9C%E7%B4%A2%E6%A0%91.png" style="zoom:80%;" />

小思考：缓存一致性怎么处理比较好？

------

### 浏览器解析响应，进行页面渲染

- 几种常见的前端后合作模式

  - 前后端不分离，后端返回HTML

  - 前后端分离，后端返回json数据

  - 前后端分离，前端进行服务端渲染，前端返回HTML

- CDN

  > [**內容分发网络**](https://zh.wikipedia.org/wiki/%E5%85%A7%E5%AE%B9%E5%82%B3%E9%81%9E%E7%B6%B2%E8%B7%AF)（英语：**C**ontent **D**elivery **N**etwork或**C**ontent **D**istribution **N**etwork，缩写：**CDN**）是指一种透过互联网互相连接的电脑网络系统，利用最靠近每位用户的服务器，更快、更可靠地将音乐、图片、视频、应用程序及其他文件发送给用户，来提供高性能、可扩展性及低成本的网络内容传递给用户