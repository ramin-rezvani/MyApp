import sys
import os

sys.path.insert(0, '/home/rezvaniramin/MyApp')
os.environ['VIRTUAL_ENV'] = '/home/rezvaniramin/.virtualenvs/newenv'

from app import app as application