Mysql 的设计者将一个 B+Tree 的节点大小设置为等于一个页(这样做的目的是每个节点只需要一次 IO 就可以完成全载入), InnoDB 的一个页大小为 16KB, 锁一个每个节点的大小也是 16KB, 并且 B+Tree 的根节点是保存在内存中的, 子节点才存储在磁盘上



假设一个 B+Tree 高为 2 , 即存在一个根节点和若干个叶子节点, 那么这颗 B+Tree 的存放总记录为: **根节点指针数 \* 单个叶子节点记录行数**

-    **计算根节点指针数**: 假设表的主键为 INT 类型, 占用 4 字节(或 BIGINT 类型 8 字节), 指针大小为 6 个字节, 那么一个页(也就是 B+Tree 中的一个节点), 大概可以存储: 16384B / (4 + 6B) = 1638,  一个节点最多可以存储 1638 个索引指针
-   **计算每个叶子节点的记录数**: 假设一行记录的数据大小为 1K, 那么一页就可以存储 16 行数据, 16KB / 1KB = 16
-   **一颗高度为 2 的 B+Tree 可以存放的记录数为**: 1638 * 16 = 26208 条数据记录, 同样的原理可以推算出一个高度为 3 的 B+Tree 可以存放: 1638 * 1638 * 16 = 42928704 条这样的记录

**所以 InnoDB 的 B+Tree 高度一般为 1-3 层, 就可以满足千万级别的数据存储**, 在查找数据时一次页的查找代表一次 IO, 所以通过主键索引查询通常只需要 1-3 次 IO 操作即可查找到数据

