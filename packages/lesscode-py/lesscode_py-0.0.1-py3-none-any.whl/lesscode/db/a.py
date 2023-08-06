

import asyncio

# hosts = [{'host': '120.92.33.79', 'port': 9210}]
hosts = ['zhengyang:158022@120.92.33.79:9210']

# hosts = [[{'host': '120.92.33.79', 'port': 9210}]]


# async def print_info():
#     event_loop = asyncio.get_event_loop()
#     # async with AsyncElasticsearch(hosts=hosts,port=9210) as client:
#     async with AsyncElasticsearch(hosts=hosts) as pool:
#         print(await pool.info())
#     # client = Elasticsearch(
#     #     hosts=hosts, loop=event_loop, timeout=3600)
#     body = {
#         "query": {
#             "bool": {
#                 "must": [
#                     {"terms": {
#                         "basic.currency": [
#                             "人民币"
#                         ]
#                     }}
#                 ]
#             }
#         }
#     }
#
#     # records =pool.search(index="core.company", body=body)
#     # print(records)
#     # assert isinstance(client.transport.connection_pool,
#
#
# # asyncio.run(print_info())
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(print_info())
# # loop.close()
#
#
# # GET core.company/_search
# es = AsyncElasticsearch(hosts=hosts)
# async def main():
#     resp = await es.search(
#         index="core.company",
#         body={
#             "query": {
#                 "bool": {
#                     "must": [
#                         {"terms": {
#                             "basic.currency": [
#                                 "人民币"
#                             ]
#                         }}
#                     ]
#                 }
#             }
#         },
#         size=20,
#     )
#     print(resp)

# asyncio.run(main())
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())