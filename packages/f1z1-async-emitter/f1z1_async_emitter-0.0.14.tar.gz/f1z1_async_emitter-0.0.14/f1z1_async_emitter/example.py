# @Time     : 2021/7/23
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
# from datetime import datetime
#
# from f1z1_common import UnitOfTime
# from async_emitter.f1z1_async_emitter import (
#     CounterWorkerBuilder,
#     TimeoutWorkerBuilder,
#     WorkerGroupFactory,
#     WorkerMasterFactory,
#     Speed,
#     run,
#     CounterWorkerDecorate
# )
#
#
# # @CounterWorkerDecorate(count=10, speed=1000, speed_unit=UnitOfTime.MILLISECOND)
# async def request(resp: str, speed: Speed):
#     print("send request...")
#     await speed
#     print(f"response, {resp}")
#     return resp
#
#
# def worker(resp: str, speed: Speed):
#     builder = TimeoutWorkerBuilder(
#         request,
#         args=(resp, speed)
#     )
#     builder \
#         .set_timeout(10000, UnitOfTime.MILLISECOND) \
#         .set_speed(500, UnitOfTime.MILLISECOND)
#     return builder.build()
#
#
# def group(speed: Speed):
#     g = WorkerGroupFactory.create(
#         100,
#         100,
#         UnitOfTime.MILLISECOND
#     )
#     g.stuff([worker(f"resp_{index}", speed) for index in range(5)])
#     print(g)
#     return g
#
#
# # async def run():
# #     return await worker().start()
#
# def current(unit: int):
#     return datetime.now().timestamp() * abs(unit)
#
#
# def main():
#     speed = Speed(2000, UnitOfTime.MILLISECOND)
#     # # res = run(worker("angel", speed))
#     master = WorkerMasterFactory.create(3)
#     master.add(group(speed))
#     master.add(group(speed))
#     print(f"master {master}")
#     res = master.start()
#     # res = run(request("angel", speed))
#     for index, item in enumerate(res):
#         print(f"{index}: {item}")
#
#
# if __name__ == '__main__':
#     main()
