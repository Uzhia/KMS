# Java连接Neo4j数据库程序

程序的核心文件是src/main/java/demo/App目录下的App.java文件。该文件中有连接Neo4j数据库的代码，其中 ***URI*** 字符串为Neo4j服务器的地址， ***USER*** 字符串为登录Neo4j服务器的用户名， ***PASSWORD*** 为该用户的密码。

运行App.java程序以后会尝试连接上服务器，如果尝试连接服务器一段时间以后失败的话，程序会捕捉报错并将报错的结果输出到运行中，然后结束运行。成功的话则会执行下列代码块：
```
try(Session session = driver.session()) {   
String cql="";  
Result result;
int id = 16 ,limit = 25;  
String node1 = "" , node2 = "test" , relation = "年代", label = "info" ,name="明" ;  
String property = "entity='e114514'";  
RemoveNode(session,label,node2);  
AddNode(session,label,node2);  
CreateRelation(session,node1,node2,relation);  
DeleteRelation(session,node1,node2,relation);  
QueryNode(driver,label,node1, String.valueOf(limit));  
findById(driver,label, String.valueOf(id));  
setNodeProperties(session,label,node2,property);  
CQL(session,cql);  
}
```
其中，
`cql` `id` `limit` `node1` `node2` `relation` `label` `name` `property` `result`
为已经声明的变量 ，
`RemoveNode()` `AddNode()` `CreateRelation()` `DeleteRelation()` `QueryNode()` `findById()` `setNodeProperties()` `CQL()`
为已经编写好的函数，可以直接将变量带入函数中或稍加修改变量再带入运行就能实现基本的增删改查功能。如果这些函数的功能还不够齐全，那么该程序最大的特点在于可以直接将字符串作为CQL语句输入到数据库中执行。因此可以直接在 `cql` 中写CQL语句，然后调用 `CQL()` 函数，或者直接 `session.run(cql)` 也可以直接运行CQL语句，运行返回的结果可以赋值给变量 `result` ，`result.records()` 可以返回一个 `List<Record>` 类型的值，因此可以声明一个 `List<Record> r = result.records()` ，然后用 `for(Record i : r) System.out.println(i.toString());`  将结果输出。