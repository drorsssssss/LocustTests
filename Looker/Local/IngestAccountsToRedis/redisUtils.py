from LocustUtils.redis_utils import RedisUtils

def ingestAccountsToRedis():
    accounts_data_path='/redis/accounts.csv'
    host='localhost'
    redis_conn = RedisUtils(host)

    #clear queue before enqueing
    redis_conn.redis_clear_queue()

    with open(accounts_data_path,"r") as file:
        for line in file:
            redis_conn.redis_enqueue(line.strip())

    print(f"Number of added entries to queue: {redis_conn.redis_queue_length()}")

ingestAccountsToRedis()




