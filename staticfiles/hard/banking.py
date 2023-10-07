class Active():
    def __init__(self, name, name_eng):
        self.name_rus = name
        self.name_eng = name_eng




class Repository():
    def __init__(self):
        k = ['Банк', 'Стартап Соседа', 'Образование', 'Гособлигации'
                                    , 'Корпоративыне облигации']
        z = ['bank', 'startap', 'obrasovanie', 'gosobligatszii', 'korporativnye']
        self.list_actives_choice = []
    def __str__(self):
        return 'название актива'

    def get_list_actives_choice(self, year):
        return self.list_actives_choice[:year + 2]
    def get_list_actives_choice_eng(self, year):
        return self.list_actives_choice_eng[:year + 2]


repo = Repository()
print(repo.get_list_actives_choice(1))