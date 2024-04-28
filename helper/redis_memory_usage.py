import redis
import backend.queryengine as queryengine


def print_redis_memory_usage():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    info = redis_client.info()
    memory_usage = info["used_memory"]
    print(f"Redis memory usage: {memory_usage / (1024 * 1024):.2f} MB")

    keys = redis_client.keys("*")

    for key in keys:
        value = redis_client.get(key)
        print(f"{key}: {value}")


if __name__ == '__main__':
    print_redis_memory_usage()