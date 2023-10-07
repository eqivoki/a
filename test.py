import csv, sys, os
import os
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = dir_path + '/finalGame'
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django

django.setup()
from Game.models import Player
a = Player.objects.all()
print(a)
# class Host:
#     def __init__(self):
#         pass
#     #
#
# wget https://raw.githubusercontent.com/gaoxx643/MovieLens-1M-Dataset/master/movies.dat
# wget https://raw.githubusercontent.com/gaoxx643/MovieLens-1M-Dataset/master/users.dat
# wwget https://raw.githubusercontent.com/gaoxx643/MovieLens-1M-Dataset/master/ratings.dat
# class Player:
#     def __init__(self, name):
#         self.name = name
#         self.active_a = 100
#         self.active_b = 100
#
#     def Name(self):
#         print(f'my name is {self.name}')
#         return 0
#     def __abs__(self):
#         return 'player'
#
#
# p = Player('Vanya')
# p.Name()
# a = [p, p]
# print(a)

print()
