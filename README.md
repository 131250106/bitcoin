# bitcoin

## 系统架构图
![image](https://github.com/131250106/bitcoin/blob/master/img/design.png)

## 系统模块设计图
![image](https://github.com/131250106/bitcoin/blob/master/img/module.png)

## 创世节点启动流程图
![image](https://github.com/131250106/bitcoin/blob/master/img/initialnode.png)

## 其它节点启动时序图
![image](https://github.com/131250106/bitcoin/blob/master/img/time.png)

## POW共识算法设计与实现
1. 所有节点启动完毕后，新开一个线程，执行挖矿逻辑
2. 某个节点一旦挖到某个block后，从transaction池中拉取TX，验证并放入新的block中
3. 该节点将new block 广播出去后，继续挖下一个区块
4. 某一节点一旦收到某个new block，立即发送一个信号量，停止当前挖矿行为
5. 验证该收到的new block

	5.1 如果验证通过，则将该new block添加到自己的链上

	5.2 验证不通过：

		5.2.1 从自己的routing table中的所有邻居节点拉取区块链

		5.2.2 逐个与自身区块链进行对比

			5.2.2.1 若区块链比自己的长，则用该区块链覆盖掉自己的链

			5.2.2.2 若区块链与自己的一样长，寻找fork分支点，进行fork操作

6. 继续挖下一个区块

### pow算法实现验证 —— 模拟双花操作：
某一节点将某笔钱分别不同人人发两次，经过实验模拟，发现同一时刻，只有一个交易会被确认，双花发生概率为0.
PS: 另一笔交易会在将来某个时候该节点中钱包的余额大于交易额时，被其他人或自己所确认，最终花费出去，钱包余额再次减少。

## 不同算力攻击成功概率（这里模拟双花攻击）
1. 攻击节点一旦挖到新的区块时，除了从transaction池中拉取TX外，立即新建一个TX，花费自己所有的钱，给-1号地址（模拟取现过程），并创建两个new block，
block1 包含该TX，block2不包含这个TX
2. 攻击节点给正常节点发送block1，给攻击节点发送block2
3. 正常节点收到该block时，会校验block1的合法性，发现正常，确认该TX，此时取现过程被确认，攻击者取到第一笔现金
4. 攻击节点收到该block时，会校验block2的合法性，正常，接收该block

	5.1 若攻击节点再次挖到新的区块，除了从transaction池中拉取TX外，立即新建一个TX，再次花费自己所有的钱，给-1号地址（模拟取现过程），重复1步骤

		5.1.1 攻击节点收到块，验证，不冲突，加入区块链

		5.1.2 正常节点收到块，验证，冲突，拉取其它节点的区块链，若链比自己长，则覆盖（最终上次的取现交易被覆盖掉，成功双花）

	5.2 若正常节点再次挖到新的区块，则进行正常逻辑，区块链正常运行

6. 一段时间后，观察攻击节点给-1号地址的TX的所有金额，即全部取现金额，若金额大于本身比特币金额，则表示攻击成功。
7. 记录不同算力下攻击成功概率

### 理论上分析：
攻击成功的概率 = 系统算力占比

### 模拟实验结果：
| 攻击者算力占比 | 20% | 40% | 60% | 80% |
|----------------|-----|-----|-----|-----|
| 攻击成功概率   |  2/38   |  7/48   |  9/35   |  22/65   |

注：A/B A表示攻击者提现次数，B表示挖矿的总轮数


## 不同带宽下分叉概率
| 带宽(MB)/延迟(ms) | 1000MB/0ms | 100MB/1ms | 10MB/0ms | 10MB/100ms | 10MB/1000ms | 1MB/1000ms |
|----------------|-----|-----|-----|-----|-----|-----|
| 分叉概率   |  0/(20*5)   |   0/(20*5)   |   0/(20*5)   |   0/(20*5)   |  0/(20*5)    |  0/(20*5)    |

## BGP劫持 or eclipse攻击
### BGP劫持步骤
1. 攻击者发动BGP劫持，将网络分割为**两部分**（先前2个网络正常连同并挖矿），一个大网络、一个小网络。用mininet可以限制2个网络之间的延迟，延迟设为无穷大则视为ping不同，即2个网络发生分割。
2. 在小网络中，攻击者发布交易卖出自己全部的加密货币，并兑换为法币。页面展示为攻击者生成transaction，钱包余额转移到某个特殊地址（例如“1”）。
3. 经过小网络的“全网确认”生成新block，这笔交易生效，攻击者获得等值的法币，攻击者节点钱包余额为0。
4. 攻击者释放BGP劫持，大网络与小网络互通，小网络上的一切交易被大网络否定（大网络区块链长于小网络），攻击者的加密货币全部回归到账户，而交易得来的法币，依然还在攻击者手中，完成获利。即攻击者节点区块链被大网络覆盖，钱包余额恢复至小网络区块链分叉前状态。

### Eclipse攻击步骤
eclipse攻击针对具有公共IP的受害者，其详细步骤如下：
1. 攻击者通过控制多个傀儡节点，向受害节点发起大量持续性TCP传入连接，将傀儡节点的IP地址填充到受害节点的tried表中。
2. 在建立TCP传入连接的基础上，傀儡节点向受害节点发送ADDR消息，该消息包含了大量不属于区块链网络的“垃圾”IP地址。然而，受害节点默认将此类还未成功建立连接的地址存储在其new表中。攻击者就是利用此特性来达到覆盖受害节点的new表地址的目的。其中，“垃圾”地址是未分配的或保留以供将来使用的地址。
3. 攻击持续到受害者节点重新启动，并从其永久存储的tried表和new表中选择新的传出连接。受害者很大概率地将建立的所有8个传出连接与攻击者地址相连 (所有的8个地址均来自tried表,因为受害者无法连接到new表中的“垃圾”地址）。
4. 攻击者不断用其攻击地址与受害者相连，从而最终占据受害者剩下的117个传入连接。（总之就是修改了某个节点所有的路由表，使其只能连接到攻击者节点，之后就为所欲为）
5. 对受害者节点发动多重支付攻击和自私挖矿攻击等。
6. 具体的双花攻击包括0确认双花攻击，攻击者向受害节点发送包含某个转账交易a的transaction并且在攻击者网络中不需确认（攻击者从而收到转账并提现）；同时攻击者向其余正常节点发送不包含转账交易a的transaction，经过正常矿工的挖矿形成链B，在链B的历史中，攻击者并没有收到交易a的记录。
7. N-确认双花攻击，受害者网络存在矿工，受害节点需要看到区块链N-1块中存在已确认的交易才发货，攻击者向受害节点发送包含某个转账交易a的transaction并且在攻击者网络中得到确认（挖矿算力由受害者贡献），形成链A；同时攻击者从外部得到正常的链B，只要向受害者发送更长的链B（其中不存在转账交易a的transaction），链A就会被链B覆盖，链A上的交易随之逆转。


## POS共识算法设计与实现
PoS(Proof of stake)直观来看就是拥有更多财产的节点，有更大的概率获得记账权，然后获得奖励。具体模拟的过程如下：

1. 每个节点根据当前钱包中的比特币数量num从[0,num]随机生成一个值，代表其权益大小，并且向所有节点广播。
2. 当所有节点都收到来自其他节点的权益广播后，将记账权赋予当前具有最大权益值的节点。
3. 具有记账权的节点将该节点上的交易验证后打包进区块，计算hash之后广播该区块。
4. 其余节点收到广播的区块，经过验证后将其加到区块链的尾部，完成区块链的增长。

## PBFT共识算法设计与实现
发起节点i,创建block，调用1号节点，pre-prepare（self.id, block）

1号节点发送广播（除发起节点i外），调用其它结点的prepare方法

所有节点的prepare方法里广播调用其它结点的prepare方法，计数自己被调用次数，若结果大于一半的N，则广播调用commit方法

commit方法里计数被调了多少次，若大于一半的N，则记录这个block, 同时调用交易节点的reply方法

交易结点的reply方法里计数，若大于一半的N，记录这个block,钱包扣钱， 调用大家的计数清零函数

===============================================================================
### 原PBFT共识算法
1. 请求阶段：客户端向主节点发送请求。
2. 预准备阶段：主节点分配一个序列号n给收到的请求，然后向所有备份节点广播预准备消息，预准备消息的格式为`<<PRE-PREPARE,v,n,d>,m>`，这里v是视图编号，m是客户端发送的请求消息，d是请求消息m的摘要。
3. 准备阶段：备份节点i接受了预准备消息`<<PRE-PREPARE,v,n,d>,m>`，则进入准备阶段。在准备阶段的同时，该节点向所有副本节点发送准备消息<PREPARE,v,n,d,i>，并且将预准备消息和准备消息写入自己的消息日志。
4. 确认阶段：副本节点收到2f个从不同副本节点发来一致的预准备消息，一共2f+1个一致的预准备消息确认了消息的正确性，然后按照序号n依次执行请求。

算法流程如图所示：
![PBFT](https://pic1.zhimg.com/v2-9d674fd22e1c2fd84068dff4a1ae2a54_r.jpg)

参考链接：https://zhuanlan.zhihu.com/p/34346665
