from rsmq import RedisSMQ


class RedisUtils():
    def __init__(self,host):
        self.conn=RedisSMQ(host=host, qname="accounts")

    def redis_enqueue(self,msg):
        self.conn.sendMessage(delay=0).message(msg).execute()

    def redis_dequeue(self):
        return self.conn.popMessage().execute()['message']

    def redis_queue_length(self):
        return self.conn.getQueueAttributes().execute()['msgs']

    def redis_quit(self):
        return self.conn.quit()

    def redis_clear_queue(self):
        self.conn.deleteQueue().exceptions(False).execute()
        self.conn.createQueue(delay=0).vt(20).execute()