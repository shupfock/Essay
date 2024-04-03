### InnoDB 的行锁是怎么实现的

**InnoDB 行锁是通过对索引数据页上的记录加锁实现的**, 主要实现算法有 3 种: Record Lock,  Gap Lock 和 Next-key Lock

-   Record Lock锁: 锁定单个行记录的锁(记录锁, RC, RR 隔离级别支持)
-   Gap Lock 锁: 间隙锁, 锁定索引记录间隙, 确保索引记录的间隙不变. (范围锁, RR 隔离级别支持)
-   Next-key Lock 锁: 记录锁和间隙锁的组合, 同时锁住数据, 并且锁住数据前后范围( 记录锁+范围锁, RR 隔离级别支持)

>   注意: InnoDB 这种行锁实现意味着: 只有通过索引条件检索数据, InnoDB 才使用行级锁, 否则, InnoDB 将使用表锁

**在 RR 隔离级别下, InnoDB 对于记录加锁行为都是先采用 Next-key Lock, 但是当 SQL 操作含有唯一索引时, InnoDB 会对 Next-key Lock 进行优化, 降级为 Record Lock, 仅锁住索引本身而非范围**

各种操作加锁的特点:

1.   select ... form 语句: InnoDB 引擎采用 MVCC 机制实现非阻塞读, 所以对于普通的 select 语句, InnoDB 不加锁
2.   select ... form lock in share mode 语句: 追加了共享锁, InnoDB 会使用 Next-key Lock 锁进行行处理, 如果扫描发现唯一索引, 可以降级为 RecordLock 锁
3.   select ... from for update 语句: 追加了排他锁, InnoDB 会使用 Next-key Lock 锁进行处理, 如果扫描发现唯一索引, 可以降级为 RecordLock 锁
4.   update ... where / delete ... from 语句: InnoDB 会使用 Next-key Lock 锁进行处理, 如果扫描发现唯一索引, 可以降级为 RecordLock 锁
5.   insert 语句: InnoDB 会在将要插入的那一行设置一个排他的 RecordLock 锁