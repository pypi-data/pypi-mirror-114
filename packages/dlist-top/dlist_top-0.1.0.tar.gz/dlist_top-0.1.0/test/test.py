import logging
from dlist_top import Client
from .config import TOKEN

# class Test(Base):
#     a: Unix

# x = Test(a = 1619220922087)
# print(x.a)


logging.basicConfig(level=logging.INFO)

dlist = Client(token=TOKEN)
dlist.connect()

@dlist.on('rate')
def on_rate(data):
    print(data)
    
@dlist.on('vote')
def on_vote(data):
    print(data)