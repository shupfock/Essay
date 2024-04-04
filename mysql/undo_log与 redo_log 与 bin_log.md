#### undo log 基本概念

-   Undo log是一种用于撤销回退的日志, 在数据库事务开始前, mysql 会记录更新前的数据到 undo log 日志文件里面, 当事务回滚时或者数据库崩溃时, 可以利用 undo log 来进行回退
-   undo log 产生和销毁: undo log 在事务开始前产生; 事务在提交时, 并不会立刻删除 undo log, InnoDB 会将该事物对应的 undo log 放入删除列表中, 后面通过后台线程 purge thread 进行回收处理

**注意: undo log 也会产生 redo log, 因为 undo log 也要实现持久性保护**

#### undo log 的作用

1.   **提供回滚操作 [undo log 实现事务的原子性]**

     在数据修改的时候, 不仅记录了 redo log, 还记录了相对应的 undo log, 如果因为某些原因事务执行失败了, 可以借助 undo log 进行回滚

     undo log 和 redo log 记录物理日志不一样, 它是逻辑日志. 可以认为当 delete 一条记录是, undo log 中会记录一条对应的 insert记录, 反之亦然, 当 update 一条记录时, 它记录一条对应相反的 update 记录

2.   **提供多版本并发控制(MVCC) [undo log 实现 MVCC]**

     在 mysql 数据库 InnoDB 存储引擎中, 用 undo log 来实现MVCC, 当读取的某一行被其他事务锁定时, 他可以从 undo log 中分析出该行记录以前的数据版本是怎么样的, 从而让用户能够读取到当前事物操作之前的数据[快照读]



#### redo log 基本概念

-   InnoDB 引擎对数据的更新, 是先将更新记录写入到 redo log 日志, 然后会咋机系统空闲的时候或者是按照设定的更新策略再讲日志中的内容更新到磁盘中. 这就是所谓的预写式技术(Write Ahead logging). 这种技术可以大大减少 IO 操作的频率, 提升数据刷新的效率
-   redo log: 被称作重做日志, 包括2 部分: 一个是内存中的日志缓冲(redo log bugger), 另一个是磁盘上的日志文件(redo log file)

#### redo log 的作用

​	mysql每执行一条 DML 语句, 现将记录写入 redo log buffer. 后续某个时间点再一次将多个操作记录写到 redo log file. 当故障发生致使内存数据丢失后, InnoDB 会在重启时, 经过重放 redo, 将 Page 恢复到崩溃之前的状态, **通过 redo log 可以实现事物的持久性**



#### bin log 基本概念

-   binlog 是一个二进制格式的文件, 用于记录用户对数据库更新的 sql 语句信息, 例如更改数据库表和更改内容的 sql 语句都会记录到 binlog 里, 但是不会记录 select 和 show 这类操作
-   binlog 在 mysql 的 server 层实现(引擎公用)
-   binlog 为逻辑日志, 记录的是一条 sql 语句的原始逻辑
    -   binlog 不限制大小, 追加写入, 不会覆盖以前的日志
    -   默认情况下, binlog 日志是二进制格式的, 不能使用查看文本的工具命令查看, 而使用 mysqlbinlog 解析查看

#### binlog 的作用

-   主从复制: 在主库中开启 binlog 功能, 这样主库就可以把 binlog 传递给从库, 从库拿到 binlog 后实现数据恢复达到主从数据一致性
-   数据恢复: 通过 mysqlbinlog 工具来恢复数据