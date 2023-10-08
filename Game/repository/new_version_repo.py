import numpy as np


class GameRules:
    def __init__(self, interest_rate=0.3):
        # Для игры, в целом
        self.education = None
        self.inflation = None

        # Для банка

        self.interest_rate = interest_rate

        # Для корпоративной облигации
        self.corp_bond_scalar = None
        self.noise = None

        # Для государственной облигации
        self.gov_bond_scalar = 0.005
        # Для акции Роста
        self.was_more_than_40 = None
        self.voters_ratio = None

        # Для Обычной акции (барсучий случай ориг.)
        self.noise_simple_1 = self.make_random_noise(0.035, 0.0125)
        self.noise_simple_2 = self.make_random_noise(0.015, 0.0125)
        self.simple_add = np.random.choice(a=[self.noise_simple_1, self.noise_simple_2], size=1, p=[1 / 2, 1 / 2])
        # Для недвижимости

        # Для третей акции

        # Для опциона

        # Для фьючерса

    # Получаем новые данные о случайных величинах. Использовать каждый год
    def new_state(self) -> int:
        self.corp_bond_scalar = np.random.choice(a=[0.017, 0, 0.005], p=[1 / 3, 1 / 3, 1 / 3])
        self.noise = self.make_random_noise(0, 0.005)
        return 1

    def make_random_noise(self, expected_value, std):
        '''
        штука для нормального шума с ограничениями
        :param expected_value: матожидание
        :param std: стандартное отклонение
        :return: нормальный шум с заданными параметрами
        '''
        noise = np.random.normal(loc=expected_value, scale=std)
        if abs(noise) > abs(expected_value + 3 * std):
            if noise < 0:
                noise = expected_value - 3 * std
            else:
                noise = expected_value + 3 * std
        return noise

    def calc_bank(self, amount) -> int:  # в банк подается сумма, на выходе получаем (новая сумма, прирост)
        return amount * (1 + self.interest_rate)

    def calc_corp_bond(self, amount, educ_count, is_not_mortgage) -> int:  # мб educ count где-то потом добавлять
        return (1 / 3) * (amount * (1 + self.corp_bond_scalar + self.inflation + self.noise) +
                          amount * self.education * is_not_mortgage * educ_count)

    def calc_gov_bond(self, amount, educ_count, is_not_mortgage) -> int:
        return (1 / 3) * (amount * (1 + self.gov_bond_scalar + self.inflation + self.noise) +
                          amount * self.education * is_not_mortgage * educ_count)

    def calc_education(self,amount, educ_count):
        # TODO придумать, как детектить то, что если если образование, то нужно деньги сохранить
        return educ_count + 1 if educ_count < 8 else 7, amount

    def calc_simple_stock(self, amount, educ_count):
        expected_return = 1 + self.inflation - 0.01
        '''
        ЭТО КАК РАЗ БАРСУЧИЙ СЛУЧАЙ
        нормальное распределение с матожиданием 4 и дисперсией 1. При этом дивы по дефолту 3
        '''
        return (1 / 3) * (amount * (expected_return + self.simple_add) + educ_count * amount * self.education)
    def calc_growth_stock(self, amount, year, educ_count):
        '''
        АКЦИЯ РОСТА
        '''
        market_premium = 0
        if not self.was_more_than_40:
            if year == 7:
                market_premium = self.inflation + 0.035
            elif year == 8:
                market_premium = self.inflation + 0.06
            elif year == 9:
                market_premium = self.inflation + 0.11
            elif year == 10:
                market_premium = self.inflation + 0.15
        else:
            market_premium = self.inflation - 0.01
        if self.voters_ratio > 0.3:
            if self.was_more_than_40:
                market_premium = self.inflation - 0.01
            else:
                market_premium = self.inflation - 0.29
                self.checker = True
        else:
            pass

        return  (1 / 3) * (amount * (1 + market_premium) +  amount * educ_count) #TODO мб не так работает образование

    def calc_mortgage(self, amount):
        return 0

    def calc_third_stock(self, amount):
        return 0

    def calc_futures(self, amount):
        return 0

    def calc_option(self, amount):
        return 0

class Repository(GameRules):
    def __init__(self, interest_rate):
        self.set_of_frozen_players = {}
        super().__init__(interest_rate)

    def get_players(self) -> int:  # Получить список всех игроков
        pass

    def player_step(self) -> int:  # Сохранить ход игрока
        pass

    def gamble(self) -> int:  # Сделать ход для всех игроков, ход которых зависит от хода других
        pass

    def delete_players(self, list_of_players: list) -> int:
        pass


class InvestingOptions:
    '''
    Класс для реализации различных инвестиционных возможностей в игре. Почти все активы строятся одинаковым образом:
    на вход подаются индексы игроков, сумма в предыдущий год по данному активу, колонка для инициализации результата
    инвестирования в инструмент.
    '''

    def __init__(self, df: pd.DataFrame, year: int, educ_dohod: float,
                 inflation_rate: float, number_only: float,
                 number_together: float, was_more_than_40: bool):
        self.data = df  # датафрейм с информацией по текущей игре
        self.choice_1 = "year_" + str(year) + '_1'
        self.choice_2 = "year_" + str(year) + '_2'
        self.choice_3 = "year_" + str(year) + '_3'
        self.future_money_1 = 'asset_' + str(year) + '_1'
        self.future_money_2 = 'asset_' + str(year) + '_2'
        self.future_money_3 = 'asset_' + str(year) + '_3'
        self.educ = educ_dohod
        self.inflat = inflation_rate
        self.stock_only_ratio = number_only  # коэффициент участников для акции с отрицательной бетой
        self.stock_together_ratio = number_together  # коэффициент участников для акции роста
        self.year = year
        self.was_more_than_40 = was_more_than_40
        self.checker = False
        self.first_check_mortgage = True

    def bank(self, indexes,
             mon_fut, flag=0):
        '''
        Реализация инвествыбора "вложение в банк".
        ВАЖНО!!!! ПОСЛЕДУЮЩИЕ ФУНКЦИИ РАБОТАЮТ ПО ТАКОМУ ЖЕ ПРИНЦИПУ
        :param indexes: индексы игроков, которые выбрали банк - np.array
        :param mon_fut: колонка, куда будет начислена сумма по результатам инвестирования - str
        :param mon_prev: колонка, откуда будет взята сумма по результатам прошлых инвестирований - str
        :param flag: по дефолту 0 - для дополнительного дохода от образования необходимо поставить 1
        :return: self
        '''
        self.data.loc[indexes, mon_fut] = (1 / 3) * (self.data.loc[indexes, "TOTAL"] * \
                                                     (1 + self.inflat) + self.data.loc[
                                                         indexes, 'TOTAL'] * self.educ * flag * self.data.loc[
                                                         indexes, 'educ'])
        return self

    '''
    def bank_pm(self, mon_prev: float, player: Player,  flag=0): # TODO implement this funk to preexecute mode
        return mon_prev * (1 + self.inflat - 0.005) + mon_prev * self.educ * flag * player.Education
    def gov_bond_pm(self, mon_prev: float, player: Player, flag = 0):
        scalar_value = np.random.choice(a=[0.035, 0, -0.01], p=[0.25, 0.5, 0.25])
        return mon_prev * (1 + scalar_value + self.inflat) + mon_prev * self.educ * flag * player.Education
    def education_pm(self, mon_prev: float, player: Player, flag=0):
        player.Education += 1
        player.save()
        return mon_prev * ( 1 +player.Education * flag * self.educ )


    def korp_bond(self, indexes,
                  mon_fut, flag=0):
        scalar_value = np.random.choice(a=[0.017, 0, 0.005], p=[1 / 3, 1 / 3, 1 / 3])
        noise = self.make_random_noise(0, 0.005)
        self.data.loc[indexes, mon_fut] = (1 / 3) * (self.data.loc[indexes, "TOTAL"] * ( \
                    1 + scalar_value + self.inflat + noise) + \
                                                     self.data.loc[indexes, "TOTAL"] * self.educ * flag * self.data.loc[
                                                         indexes, 'educ'])
        return self

    def gov_bond(self, indexes, mon_fut, flag=0):
        noise = self.make_random_noise(0, 0.005)
        self.data.loc[indexes, mon_fut] = (1 / 3) * (self.data.loc[indexes, "TOTAL"] * \
                                                     (1 + self.inflat + 0.005 + noise) + \
                                                     flag * self.data.loc[indexes, "TOTAL"] * self.educ * self.data.loc[
                                                         indexes, 'educ'])
        return self
        '''

    def education(self, indexes, mon_fut):
        # поставь ограничение на 8-ой уровень образования
        self.data.loc[indexes, 'educ'] += 1
        # self.data.loc[self.data['educ'] > 1, 'educ'] = 1  # ограничение на образование
        self.data.loc[indexes, mon_fut] = (1 / 3) * self.data.loc[indexes, "TOTAL"]
        return self

    def stock_only(self, indexes, mon_fut, flag=0):
        if 0 < self.stock_together_ratio < 0.1:
            market_premium = self.inflat + 0.03
        elif 0.1 <= self.stock_together_ratio < 0.2:
            market_premium = self.inflat + 0.05
        elif 0.2 <= self.stock_together_ratio < 0.4:
            market_premium = self.inflat + 0.07
        elif 0.4 <= self.stock_together_ratio < 0.6:
            market_premium = self.inflat + 0.09
        else:
            market_premium = self.inflat - 0.03
        self.data.loc[indexes, mon_fut] = 0.33 * (self.data.loc[indexes, "TOTAL"] * (1 + market_premium) + \
                                                  self.data.loc[indexes, 'educ'] * self.educ * flag * self.data.loc[
                                                      indexes, "TOTAL"])
        return self

    def stock_together(self, indexes, mon_fut, flag=0):
        '''
        АКЦИЯ РОСТА
        '''
        if not self.was_more_than_40:
            if self.year == 7:
                market_premium = self.inflat + 0.035
            elif self.year == 8:
                market_premium = self.inflat + 0.06
            elif self.year == 9:
                market_premium = self.inflat + 0.11
            elif self.year == 10:
                market_premium = self.inflat + 0.15
        else:
            market_premium = self.inflat - 0.01
        if self.stock_together_ratio > 0.3:
            if self.was_more_than_40:
                market_premium = self.inflat - 0.01
            else:
                market_premium = self.inflat - 0.29
                self.checker = True
        else:
            pass

        self.data.loc[indexes, mon_fut] = (1 / 3) * \
                                          (self.data.loc[indexes, "TOTAL"] * (1 + market_premium) + \
                                           self.data.loc[indexes, "TOTAL"] * flag * self.educ * self.data.loc[
                                               indexes, 'educ'])
        return self

    def stock_index(self, indexes, mon_fut, flag=0):
        expected_return = 1 + self.inflat - 0.01
        '''
        ЭТО КАК РАЗ БАРСУЧИЙ СЛУЧАЙ
        нормальное распределение с матожиданием 4 и дисперсией 1. При этом дивы по дефолту 3
        '''
        noise_1 = self.make_random_noise(0.035, 0.0125)
        noise_2 = self.make_random_noise(0.015, 0.0125)
        add = np.random.choice(a=[noise_1, noise_2], size=1, p=[1 / 2, 1 / 2])
        self.data.loc[indexes, mon_fut] = (1 / 3) * \
                                          (self.data.loc[indexes, "TOTAL"] * (expected_return + add) + \
                                           self.data.loc[indexes, "TOTAL"] * self.educ * self.data.loc[indexes, 'educ'])
        return self

    def sosed(self, indexes, mon_fut, flag=0):
        outcomes = np.random.choice(a=[0.1, 0.0], size=len(indexes), p=[1 / 2, 1 / 2])
        outcomes += 1
        self.data.loc[indexes, mon_fut] = (1 / 3) * (self.data.loc[indexes, "TOTAL"] * outcomes + \
                                                     self.data.loc[indexes, "TOTAL"] * flag * self.educ * self.data.loc[
                                                         indexes, 'educ'])
        return self

    def mortgage(self, indexes, mon_fut, flag=0):
        """
        Сначала проверяем, что они использовали опцию накопа в недвиге, потом зачисляем тем, у кого уже есть актив
        а потом уже начисляем тем, кто первый раз выбрал
        """
        if self.first_check_mortgage:
            self.checker_for_mortgage(indexes)
            self.first_check_mortgage = False
        return_mortgage = 1.07  # FIX
        return_mortgage_init = 1.03
        return_mortgage += self.make_random_noise(0, 0.01)
        return_mortgage_init += self.make_random_noise(0, 0.01)
        """
        condition_first = self.data['mortgage_count'] != 0
        if self.data[condition_first].shape[0] == 0: #проверка, чтобы не было ошибки в коде - начисляем хоть кому-то
            pass
        else:
            count_this_year = self.data.loc[indexes][self.list_of_choices].isin(['mortgage']).sum(axis=1).values
            #смотрим, сколько "ипотек" было взято игроком конкретно в этот год. Если оно совпадает с текущим количеством
            # мортгейдж каунт, то получается, что он взял еще одну - тогда отправляем на 1.03
            current_values = self.data.loc[indexes, 'mortgage_count'].values
            diff = count_this_year - current_values
            nakop_mortgage = diff[diff == 0]
            indexes_to_nakop = nakop_mortgage
            if indexes_to_nakop:
                accrue__ = (1 / 3) * (
                        self.data.loc[condition_first].loc[indexes_to_nakop, "TOTAL"] * return_mortgage + \
                        self.data.loc[condition_first].loc[indexes_to_nakop, "TOTAL"] * self.educ *
                        self.data.loc[condition_first].loc[indexes_to_nakop, 'educ'])
                self.data.loc[accrue__.index, mon_fut] = accrue__
                vals = self.data.loc[condition_first].loc[accrue__.index, 'mortgage_count']
                vals -= 1
                self.data.loc[vals.index, 'mortgage_count'] = vals.values
                return self
        """
        """
        #condition_second = self.data['mortgage_count'] == 0
        #print(self.data.loc[condition_second].loc[indexes])
        to_accrue = (1 / 3) * (
                self.data.loc[indexes, 'TOTAL'] * return_mortgage_init + \
                self.data.loc[indexes, 'TOTAL'] * self.educ *
                self.data.loc[indexes, 'educ']
        ) #было loc[condition_second]
        self.data.loc[to_accrue.index, mon_fut] = to_accrue
        vals_2 = self.data.loc[to_accrue.index]['mortgage_count'] #loc[condition_second]
        vals_2 += 1
        self.data.loc[vals_2.index, 'mortgage_count'] = vals_2.values
        """
        self.data.loc[indexes, 'further_mortgage'] += 1
        sub_info = self.data.loc[indexes, 'now_mortgage'] - self.data.loc[indexes, 'further_mortgage']
        indexes_to_nakop = sub_info[sub_info >= 0].index
        indexes_to_start = sub_info[sub_info < 0].index
        if len(indexes_to_start) > 0:
            self.accrue_mortgage(indexes_to_start, mon_fut, return_mortgage_init, flag='start', flag_ed=flag)
        if len(indexes_to_nakop) > 0:
            self.accrue_mortgage(indexes_to_nakop, mon_fut, return_mortgage, flag='nakop', flag_ed=flag)
        return self

    def accrue_mortgage(self, indexes, mon_fut, return_rate, flag, flag_ed=0):
        to_accrue = (1 / 3) * \
                    (self.data.loc[indexes, 'TOTAL'] * return_rate + \
                     self.data.loc[indexes, 'TOTAL'] * self.educ * flag_ed * \
                     self.data.loc[indexes, 'educ'])  # было loc[condition_second]
        self.data.loc[to_accrue.index, mon_fut] = to_accrue
        vals_2 = self.data.loc[to_accrue.index]['mortgage_count']
        if flag == 'start':
            vals_2 += 1
        elif flag == 'nakop':
            vals_2 -= 1
            self.data.loc[to_accrue.index, 'further_mortgage'] -= 1
            self.data.loc[to_accrue.index, 'now_mortgage'] -= 1
        self.data.loc[vals_2.index, 'mortgage_count'] = vals_2.values
        return self

    def checker_for_mortgage(self, indexes):
        """
        фукнция нужна для того, чтобы проверить, что игрок
        исполнил второй раз опцию недвижимости. В случае если нет - убрать его накопленный доход
        """
        mask = self.data['mortgage_count'] != 0
        count_second_choice = self.data[mask]
        if count_second_choice.shape[0] == 0:
            return self
        else:
            count_second_choice = count_second_choice.loc[indexes][[self.choice_1, self.choice_2, self.choice_3]]
            count_second_choice = count_second_choice.isin(['mortgage']).sum(axis=1)
            difference = count_second_choice - self.data.loc[indexes, 'mortgage_count']
            '''
            мы будем понижать только тем, у кого разница отрицательная. Это значит, что они не использовали свою возможность
            второй раз вложиться в недвигу, и тогда мы убираем у них первоначальное вложения из накопа, чтобы потом,
            когда они позже в игре решат вложится в недвигу, не был начислен сверхдоход
            у тех, у кого разница положительная, ничего не трогаем, потому что они могли, например, в год t-1 выбрать
            1 недвигу, а в год t - две. 
            '''
            to_sum = difference[difference < 0]
            self.data.loc[to_sum.index, "mortgage_count"] += to_sum
            return self  # NEEDS DEBUGGING!!!

    """
    def _return_bool_flag(self):
        '''
        Изначально функция была написана для того, чтобы флаг не менялся в зависимости от порядка
        вложения в актив (например, если education был выбран в качестве первого актива, то повторный вызов
        accrue привел бы к увеличению доходности
        :return: булевское значение для того, чтобы можно было начислять допдоход по образованию
        '''
        if self.year == 1:
            return 0
        return 1
    """

    def _accrue_money_(self, year_column, fut_money):
        '''
        Проход по всем функциям и начисление.
        !!!!!!!!!ПОКА НЕЯСНО КАК СРАВНИВАТЬ NaN - у меня пандас отказывается сравнивать np.nan, полученный
        на вход в датафрейм с nan
        !!!!!!!
        :param year_column: колонка, где находятся выборы участников в этот год - str
        :param fut_money: колонка, куда будет начислена сумма по результатам инвестирования - str
        :return: self
        '''
        opportunities = self.data[year_column].unique()
        option_dict = {'bank': self.bank,
                       'sosed': self.sosed,
                       'korp_bond': self.korp_bond,
                       'gov_bond': self.gov_bond,
                       'stock_together': self.stock_together,
                       'stock_only': self.stock_only,
                       'stock_index': self.stock_index,
                       'mortgage': self.mortgage}
        # bool_flag = self._return_bool_flag()
        for option in opportunities:
            if option == 'education':
                pass
            else:
                players_ = self.data[(self.data[year_column] == option)].index
                '''
                if option == 'education':
                    ind_for_ed = self.data[self.data[year_column] == 'education'].index
                    self.education(ind_for_ed, fut_money)
                    continue
                '''
                try:
                    option_dict[option](players_, fut_money, flag=1)
                except Exception as e:
                    # print(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)
                    self.bank(players_, fut_money, flag=1)
        return self

    def make_random_noise(self, expected_value, std):
        '''
        штука для нормального шума с ограничениями
        :param expected_value: матожидание
        :param std: стандартное отклонение
        :return: нормальный шум с заданными параметрами
        '''
        noise = np.random.normal(loc=expected_value, scale=std)
        if abs(noise) > abs(expected_value + 3 * std):
            if noise < 0:
                noise = expected_value - 3 * std
            else:
                noise = expected_value + 3 * std
        return noise

    def last_education(self):
        list_of_choice = [(self.choice_1, self.future_money_1),
                          (self.choice_2, self.future_money_2),
                          (self.choice_3, self.future_money_3)]
        for tup in list_of_choice:
            who_chose_ed = self.data[tup[0]].isin(['education'])
            indexes = who_chose_ed[who_chose_ed != 0].index
            self.education(indexes, tup[1])
        return self

    def accrue(self):
        '''
        Проход по инвестиционным опциям и начисление доходности для всех игроков
        :return: pd.DataFrame - итоговый датафрейм после 1 года игры.
        '''
        # self.list_of_choices = [self.choice_1, self.choice_2, self.choice_3]
        self._accrue_money_(self.choice_1, self.future_money_1)
        # self.list_of_choices = self.list_of_choices[1:]
        self._accrue_money_(self.choice_2, self.future_money_2)
        # self.list_of_choices = self.list_of_choices[1:]
        self._accrue_money_(self.choice_3, self.future_money_3)
        self.last_education()
        total_ = self.data[[self.future_money_1, self.future_money_2, self.future_money_3]].sum(axis=1)
        self.data[f'TOTAL_year_{self.year}_for_dohod'] = self.data['TOTAL']
        self.data[f"asset_{self.year}_1_for_dohod"] = self.data[self.future_money_1]
        self.data[f"asset_{self.year}_2_for_dohod"] = self.data[self.future_money_2]
        self.data[f"asset_{self.year}_3_for_dohod"] = self.data[self.future_money_3]
        self.data["TOTAL"] = total_
        if self.checker:
            self.was_more_than_40 = True
        return self.data


class Repository:

    def __init__(self, id_, more_than_40=None, year=None, inflation_rate=0.04, educ_dohod=0.0033):
        '''
        Базовое правило в названии колонок: сначала ГОД, потом номер актива
        :param id_: айдишники игроков
        :param inflation_rate: базовая цифра, от которой отталкиваются дальнейшие проценты - уровень инфляции
        '''
        a = Player.objects.all() or [Player(Name='TestUser')]
        # a = Factory.get_notreal_players() # TODO тут
        self.id_ = [i.ID for i in a]
        aa = Admin.objects.all()
        if len(aa) == 0:
            year = 0
            Admin(Day=2).save()
        else:
            year = list(Admin.objects.all())[-1:][0].Day - 2
        data = pd.DataFrame({"id": self.id_})  # инициализация id
        data["TOTAL"] = [i.sum_active() for i in a]
        data[f"asset_{year}_1"] = [i.Active_a for i in a]  # инициализация актива 1
        data[f"asset_{year}_2"] = [i.Active_b for i in a]  # инициализация актива 2
        data[f"asset_{year}_3"] = [i.Active_c for i in a]
        data['mortgage_count'] = [i.Mortgage_count for i in a]
        data['further_mortgage'] = [i.Further_mortgage for i in a]
        data['now_mortgage'] = [i.Now_mortgage for i in a]
        data['educ'] = [i.Education for i in a]
        data = data.set_index("id")  # смена индекса на id
        self.data = data
        self.inflation = inflation_rate
        self.educ_dohod = educ_dohod
        if more_than_40 is None:
            self.more_than_40 = False
        else:
            self.more_than_40 = more_than_40

    def Choice(self,
               year,  # номер года
               asset_1_choice,  # список из выборов игроков касательно инвестиций актива 1
               asset_2_choice,  # список из выборов игроков касательно инвестиций актива 2
               asset_3_choice  # актив 3
               ):
        year_1 = "year_" + str(year) + '_1'  # название колонки с выборами касательно актива 1
        year_2 = "year_" + str(year) + '_2'  # название колонки с выборами касательно актива 2
        year_3 = "year_" + str(year) + '_3'  # SAME but active 3

        self.data[year_1] = asset_1_choice
        self.data[year_2] = asset_2_choice
        self.data[year_3] = asset_3_choice

        '''ЭТУ ФУНКЦИЮ МОЖНО БУДЕТ ИЗМЕНЯТЬ В ЗАВИСИМОСТИ ОТ ХАРАКТЕРА ПРИНИМАЕМЫХ ДАННЫХ ПО ВЫБОРУ АКТИВА'''
        ''' я не понял зачем нам тут это, но ладно, оставлю (комментарий от меня)'''
        return self.data

    def Gamble(self, year):  # номер года

        asset_1_is = "asset_" + str(year) + '_1'  # получаем тикер актива 1, который подается на выход
        asset_2_is = "asset_" + str(year) + '_2'  # получаем тикер актива 2, который подается на выход
        asset_3_is = 'asset_' + str(year) + '_3'

        choice_1 = "year_" + str(year) + '_1'  # получаем тикер выбора инвестиции актива 1
        choice_2 = "year_" + str(year) + '_2'  # получаем тикер выбора инвестиции актива 2
        choice_3 = 'year_' + str(year) + '_3'

        self.data[asset_1_is] = 0  # иницциализация нового значения актива 1 нулем
        self.data[asset_2_is] = 0  # иницциализация нового значения актива 2 нулем
        self.data[asset_3_is] = 0

        asset_1_was = "asset_" + str(year - 1) + '_1'
        asset_2_was = "asset_" + str(year - 1) + '_2'
        asset_3_was = 'asset_' + str(year - 1) + '_3'

        N_together = self.data[self.data[choice_1] == "stock_together"][asset_1_was].sum()  # исправить на 1 строку
        N_together += self.data[self.data[choice_2] == "stock_together"][asset_2_was].sum()
        N_together += self.data[self.data[choice_3] == "stock_together"][asset_3_was].sum()
        N_together = N_together / self.data["TOTAL"].sum()

        N_only = self.data[self.data[choice_1] == "stock_only"][choice_1].count()  # исправить на 1 строку
        N_only += self.data[self.data[choice_2] == "stock_only"][choice_2].count()
        N_only += self.data[self.data[choice_3] == "stock_only"][choice_3].count()

        gambling = InvestingOptions(self.data, year, educ_dohod=self.educ_dohod,
                                    inflation_rate=self.inflation,
                                    number_only=N_only / len(self.data),  # корректировка
                                    number_together=N_together,
                                    was_more_than_40=self.more_than_40)
        new_data = gambling.accrue()
        new_data['now_mortgage'] = new_data['further_mortgage']
        new_data['further_mortgage'] = 0
        self.data = new_data
        # print(new_data[['mortgage_count', 'further_mortgage', 'now_mortgage']])
        self.more_than_40 = gambling.was_more_than_40
        return self.data, self.more_than_40

# a = Factory()
# Player(Name='Vasya3').save()
# Player(Name='Vasya2').save()
# game_1 = a.get_repository(np.arange(1, 4, 1))
# print(game_1.data)
# for i in range(1, 7):
#     if i == 1:
#         game_1.Choice(i,
#                  ["mortgage", "stock_index", 'mortgage', 'education', 'sosed', 'korp_bond', 'gov_bond', 'mortgage'],
#                  ["bank", "mortgage", "stock_index",'education', 'sosed', 'korp_bond', 'gov_bond', 'mortgage'],
#                  ["bank", "stock_index", 'mortgage','education', 'sosed', 'korp_bond', 'gov_bond', 'mortgage'],
#                  )
#         game_1.Gamble(i)
#     else:
#         game_1.Choice(i,
#                       ["mortgage", "stock_index", 'mortgage', 'education', 'sosed', 'korp_bond', 'gov_bond',
#                        'mortgage'],
#                       ["mortgage", "mortgage", "stock_index", 'education', 'sosed', 'korp_bond', 'gov_bond',
#                        'mortgage'],
#                       ["mortgage", "stock_index", 'mortgage', 'education', 'sosed', 'korp_bond', 'gov_bond',
#                        'mortgage'],
#                       )
#         game_1.Gamble(i)
