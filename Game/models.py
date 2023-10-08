from django.db import models
# import csv, sys, os
# import django
import json


class Player(models.Model):
    ID = models.AutoField(auto_created=True, primary_key=True, unique=True)
    Name = models.CharField('name', max_length=200, unique=True, null=False)
    Active_a = models.FloatField('active_a', default=100, null=False)
    Active_a_pred = models.FloatField('active_a', default=100, null=False)
    Active_b = models.FloatField('active_b', default=100, null=False)
    Active_b_pred = models.FloatField('active_b', default=100, null=False)
    Active_c = models.FloatField('active_c', default=100, null=False)
    Active_c_pred = models.FloatField('active_c', default=100, null=False)
    Education = models.IntegerField('education', default=0)
    Day = models.IntegerField('day', default=1, null=False)
    History = models.CharField('history', max_length=400, null=False, default='[300]')
    Mortgage_count = models.IntegerField('mortgage_count', default=0)
    Further_mortgage = models.IntegerField('further_mortgage', default=0)
    Now_mortgage = models.IntegerField('now_mortgage', default=0)
    Active_a_historical = models.FloatField('active_a_historical', default=100, null=False)
    Active_b_historical = models.FloatField('active_b_historical', default=100, null=False)
    Active_c_historical = models.FloatField('active_c_historical', default=100, null=False)
    CurrentGameID = models.IntegerField('game_id', null=False, default=0)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return self.Name

    def get_history(self):
        return self.History

    def append_to_history(self, x):
        self.History = self.History[:-1] + ',' + str(x) + self.History[-1]
        return 1

    def current(self, day):
        return day == self.Day  # текущий день. Возможно, можно поставить и день - 1

    def sum_active(self):
        return round(self.Active_a + self.Active_b + self.Active_c, 2)

    def actives_pred(self):
        return round((self.Active_c_pred + self.Active_a_pred + self.Active_b_pred) / 3, 4)

    def next_year(self, a, b, c, e, f, g, d, day):  # aa, bb, cc после a, b, c
        if day > self.Day:
            self.Day += 1
        self.Mortgage_count = e
        self.Further_mortgage = f
        self.Now_mortgage = g
        self.Active_a_pred = (self.Active_a + self.Active_b + self.Active_c) / 3
        self.Active_b_pred = (self.Active_a + self.Active_b + self.Active_c) / 3
        self.Active_c_pred = (self.Active_a + self.Active_b + self.Active_c) / 3
        self.Active_a = a
        self.Active_b = b
        self.Active_c = c
        self.Education = d
        self.append_to_history(self.sum_active())
        self.Active_a_historical = a  # aa
        self.Active_b_historical = b  # bb
        self.Active_c_historical = c  # cc

    def percentage_increase_active_a(self):
        res = (-self.actives_pred() + self.Active_a_historical) / self.Active_a_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def percentage_increase_active_b(self):
        res = (-self.actives_pred() + self.Active_b_historical) / self.Active_b_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def percentage_increase_active_c(self):
        res = (-self.actives_pred() + self.Active_c_historical) / self.Active_c_pred
        if res >= 0:
            output = f"+{round(100 * res, 2)}%"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def education(self):
        return f'{round(self.Education/3, 2)}'

    def sum_active_percentage_increase(self):
        res = (self.Active_a + self.Active_b - self.Active_a_pred - self.Active_b_pred + self.Active_c
               - self.Active_c_pred) / (
                    self.Active_a_pred + self.Active_b_pred + self.Active_c_pred)
        if res >= 0:
            output = f"+{round(100 * res, 2)} %"
        else:
            output = f"{round(100 * res, 2)}%"
        return output

    def obnulit(self):
        self.Day = 1
        self.Active_a_pred = 100
        self.Active_a = 100
        self.Active_b = 100
        self.Active_c = 100
        self.Active_b_pred = 100
        self.Active_c_pred = 100
        self.Education = 0
        self.History = '[200]'
        return 1

    def one_year_back(self):
        self.Day -= 1
        new = json.loads(self.History)
        self.Active_a = self.Active_a_pred
        self.Active_b = self.Active_b_pred
        self.Active_c = self.Active_c_pred
        if len(new) < 3:
            i = 0
        else:
            i = -3
        self.Active_a_pred = new[i] // 3
        self.Active_b_pred = new[i] // 3
        self.Active_c_pred = new[i] // 3
        self.History = json.dumps(new[:-1])


class Active(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField('name', max_length=200, null=False, unique=True)
    Name_eng = models.CharField('name_eng', max_length=200)

    def get_name(self):
        return self.Name

    def __str__(self):
        return self.Name


class Factor(models.Model):
    Name1 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_a')
    Name2 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_b')
    Name3 = models.ForeignKey(Active, on_delete=models.CASCADE, null=True, related_name='active_c')
    Day = models.IntegerField('day', null=False)
    UserID = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    ActA_increase = models.CharField('actAinc', max_length=10, null=True, default="обработка")
    ActB_increase = models.CharField('actBinc', max_length=10, null=True, default="обработка")
    ActC_increase = models.CharField('actCinc', max_length=10, null=True, default="обработка")
    Money_in = models.FloatField('money_in', null=True)
    Money_out = models.FloatField('money_in', null=True)
    Not_chosen_number = models.IntegerField('not_chosen_number', default=0, null=False)

    def __str__(self):
        return str(self.Day) + ' ' + str(self.UserID) + ' ' + str(self.Name1) + ' ' + str(self.Name2) \
               + ' ' + str(self.Name3)


class Admin(models.Model):
    Game_id = models.BigAutoField(primary_key=True)
    Day = models.IntegerField('Day', null=False)
    Was_more_fourty = models.BooleanField('Was_more_fourty', null=False, default=False)

    def __str__(self):
        return "Наступил день {0} в игре номер {1}".format(self.Day, self.Game_id)