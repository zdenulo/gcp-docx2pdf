import os

port = os.environ.get('PORT', 8080)

bind = "0.0.0.0:{}".format(port)
workers = 2

