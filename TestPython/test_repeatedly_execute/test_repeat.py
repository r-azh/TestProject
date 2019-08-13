__author__ = 'R.Azh'


import time
starttime=time.time()
while True:
  print("tick tak: time is ", time.time())
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))