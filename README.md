一、storm的安装与使用  

1、安装  
步骤1、安装java环境  
sudo apt-get install default-jre  
步骤2、Linux环境下载storm(版本0.9.2)  
wget http://mirror.bit.edu.cn/apache/storm/apache-storm-0.9.2-incubating/apache-storm-0.9.2-incubating.tar.gz  
步骤3、解压  
tar zxvf apache-storm-0.9.2-incubating.tar.gz  
mv  apache-storm-0.9.2-incubating /data/storm  
步骤4、配置环境变量  
vi /etc/profile  
export STORM_HOME=/data/storm  
export PATH=$PATH:$STORM_HOME/bin  
source /etc/profile  
步骤5、编辑配置文件  
cd /data/storm  
vi conf/storm.yaml  
storm.zookeeper.servers:  
     - "192.168.199.208"    ##zookeeper地址  
nimbus.host: "192.168.199.208"  ##跑nimbus进程地址  
storm.zookeeper.port: 32181 ##zookeeper端口  
storm.local.dir: "/data/storm"  
supervisor.slots.ports:  ##开启的worker进程  
     - 6700  
     - 6701  
     - 6702  
     - 6703  
步骤6、启动服务  
nohup  /data/storm/bin/storm nimbus >/dev/null 2>&1 &   
nohup  /data/storm/bin/storm supervisor >/dev/null 2>&1 &   
nohup  /data/storm/bin/storm ui >/dev/null 2>&1 &  

2、部署storm项目  
步骤1、安装pyleus  
pip install pyleus  
步骤2、把storm项目copy到目标机器上  
log_bolt.tar.gz  
步骤3、创建项目需要的数据库、数据表结构  
CREATE DATABASE `logserver` /*!40100 DEFAULT CHARACTER SET utf8  
create table behavior(  
       ...   id INT NOT NULL AUTO_INCREMENT,  
       ...   uuid VARCHAR(100) NOT NULL,  
       ...   type VARCHAR(100) NOT NULL,  
       ...   strjson VARCHAR(100) NOT NULL,  
       ...   date VARCHAR(100) NOT NULL,  
       ...   primary key(id));  
步骤4、提交项目到storm  
tar zxvf log_bolt.tar.gz  
cd log_bolt/  
pyleus  --verbose submit -n 192.168.199.208 log_bolt.jar  
说明(pylues操作)  
pyleus  --verbose submit -n 192.168.199.208 log_bolt.jar  ##提交项目到storm  
pyleus  kill -n 192.168.199.208 log_bolt  ##杀掉log_bolt项目  
pyleus  build pyleus_topology.yaml  ##生成log_bolt项目  


二、逻辑说明： 

数据类型             注释           field                         value
PAYACCOUNT   付费账号     Channel:UUID       单UUID单渠道单位时间内的付费次数
利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key下的Channel:UUID自增

PAYCOUNT        付费次数      Channel              单渠道单位时间付费次数
利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key下的Channel自增

PAYNUM            付费人数      Channel               单渠道单位时间付费人数
额外添加5个key（项目名:数据类型:游戏 ID:时间:channel）数据类型为集合，每获得一条数据把uuid放到额外添加5个key中（该key为对用户进行去重）。计算额外添加的5个key集合的长度，把值放到对应的5个key和field下

PAYSUM             付费总额      channel              单渠道单位时间付费总额
利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key下的value加上对应的amount值

LOGINACCOUN T 登录账号    channel:uuid         单UUID单渠道单位时间内的登录次数 
利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key下的Channel:UUID自增

LOGINCOUNT      登录次数     channel                单渠道登录次数总数
利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key下的Channel自增

LOGINNUM          登录人数      channel              单渠道登录人数(登录次数去重)
额外添加5个key（项目名:数据类型:游戏 ID:时间:channel）数据类型为集合，每获得一条数据把uuid放到额外添加5个key中（该key为对用户进行去重）。计算额外添加的5个key集合的长度，把值放到对应的5个key和field下

FIRSTLOGIN        首登人数      channel             首次登录(注册)人数
判断LOGINACCOUN ALL值是否存在，如果不存在利用redis hash自增属性（hincrby）每获得一条数据让对应的5个key和field下的value自增。并且新增key（项目名:数据类型:游戏 ID:20170715:channel）类型为集合用于留存处理，如果判断LOGINACCOUN ALL值不存在，把uuid放入额外添加key中（该key为统计每天首登用户有哪些）

RETAINED            留存数据      channel:day      留存人数，day为2，3，7，15，30 代表次留 ，三留，7留，15留，30   
每获得一条数据，根据当前数据日期计算出2，3，7，15，30留对应的日期。根据2，3..留对应的日期可以找到对应的首登key（FIRSTLOGIN 中创建的），判断用户在哪天的首登key中，记录到对应的 channel:day中 

