package demo;

import java.util.Map;
import java.util.List;

import org.neo4j.driver.*;
import org.neo4j.driver.Record;


public class App {
    //直接执行CQL语句，并返回执行结果
    static Result CQL(Session session,String cql){
        return session.run(cql);
    }
    //根据label和name查询节点，返回id
    static void QueryNode(Driver driver,String label,String name,String limit){
        String cql = "MATCH (n:" + label + " {name: $name}) RETURN id(n) LIMIT "+limit;
        Map<String, Object> map = Map.of("name",name);
        var result = driver.executableQuery(cql).withParameters(map).execute();
        List<Record> r = result.records();
        for(Record i : r){
            System.out.println(i.toString());
        }
    }
    //根据id查找节点，返回name
    static void findById(Driver driver,String label,String id){
        String cql = "MATCH (n:" + label + ") WHERE id(n)="+ id +" RETURN n.name";
        var result = driver.executableQuery(cql).execute();
        List<Record> r = result.records();
        for(Record i : r){
            System.out.println(i.toString());
        }
    }
    //根据label查询节点，返回name和id
    static void QueryNode(Driver driver,String label,String limit){
        String cql = "MATCH (n:" + label + ") RETURN n.name,id(n) LIMIT "+limit;
        var result = driver.executableQuery(cql).execute();
        List<Record> r = result.records();
        for(Record i : r){
            System.out.println(i.toString());
        }
    }
    //增加节点
    static Result AddNode(Session session, String label, String name){
        String cql = "CREATE (a:"+label+" {name: \"" + name + "\"}) RETURN a";
        return session.run(cql);
    }
    //删除节点
    static void RemoveNode(Session session,String label,String name){
        String cql = "MATCH (a:"+label+" {name: \""+ name +"\"}) DETACH DELETE a";
        session.run(cql);
    }
    //增加节点间关系
    static Result CreateRelation(Session session, String a, String b, String relation){
        String cql = "MATCH (a:info {name: \""+ a +"\"}),(b:info {name: \""+ b +"\"}) CREATE (a)-[r:`"+ relation +"`]->(b)";
        return session.run(cql);
    }
    //删除节点间关系
    static void DeleteRelation(Session session,String a,String b, String relation){
        String cql = "MATCH (a:info {name: \""+ a +"\"})-[r:`"+ relation +"`]-(b:info {name: \""+ b +"\"}) DELETE r";
        session.run(cql);
    }
    //设置节点属性
    static Result setNodeProperties(Session session, String label, String name, String property){
        String cql = "MATCH (a:"+label+" {name: \"" + name + "\"}) SET a." + property;
        return session.run(cql);
    }
    private static final String URI = "bolt://localhost:7687";
    private static final String USER = "neo4j";
    private static final String PASSWORD = "12345678";
    public static void main(String... args) {
        try (var driver = GraphDatabase.driver(URI, AuthTokens.basic(USER, PASSWORD))) {
            try(Session session = driver.session()) {
//                System.out.println("成功连接上Neo4j服务器!");
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
                result = CQL(session,cql);
            } catch (Exception e) {
                System.out.println(e.getMessage());
                System.exit(1);
            }
        }
    }
}
