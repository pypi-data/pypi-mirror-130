import time
from pymyorm.connection_pool import ConnectionPool
from config import db
from models.user import User
from threading import Thread


class TaskThread(Thread):

    def run(self):
        from pymyorm.local import local
        from pymyorm.connection_pool import ConnectionPool
        pool = ConnectionPool()
        local.conn = pool.get()
        print(f"thread name={self.name} conn={local.conn}")
        time.sleep(3)
        one = User.find().where(name='ping').one()
        print(one)
        pool.put(local.conn)
        local.conn = None


def main():
    pool = ConnectionPool()
    pool.size(size=10)
    pool.debug(debug=True)
    pool.create(**db)

    stime = time.time()
    thread_list = []
    for _ in range(10):
        thread = TaskThread()
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    etime = time.time()
    print(f"time diff: {etime - stime}")


if __name__ == '__main__':
    main()
