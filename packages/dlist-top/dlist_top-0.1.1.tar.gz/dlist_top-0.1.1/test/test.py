import logging
from dlist_top import Client
from dlist_top.types import VoteData, RateData, Entity
from .config import TOKEN

# class Test(Base):
#     a: Unix

# x = Test(a = 1619220922087)
# print(x.a)


logging.basicConfig(level=logging.INFO)

dlist = Client(token=TOKEN)
dlist.connect()

@dlist.on('ready')
def on_ready(entity: Entity):
    print(entity)

@dlist.on('rate')
def on_rate(data: RateData):
    print(data)
    
@dlist.on('vote')
def on_vote(data: VoteData):
    print(data)