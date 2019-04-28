import redis

pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.set("name","liaochao")
print(r.get("name"))
#批量插入
r.mset(name1="test1",name2="test2")
print (r.mget("name1","name2"))
r.append("name3","test3")
print (r.get("name3"))