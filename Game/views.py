import json
import time
import numpy as np
import faker
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
from itertools import chain

# from .static.hard.banking import Repository
# Create your views here.

from django.shortcuts import render
from .models import Player, Active, Factor, Admin
from Game.repository.repository import Repository, Factory


# это функции просто для перехода между страницами


# переход на страничку с авторизацией
def index(request):
    try:
        pass
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/authorization.html")


# страничка с pandas репозиторием
def panda(request):
    try:
        factory = Factory()
        players = Factory.get_players(game_id=1) # TODO переделать, game_id назначать по-другому
        id_players_sorted = sorted([i.ID for i in list(players)])
        # TODO ВОТ ТУТ НАДО ДОСТАТЬ ПЕРЕМЕННУЮ ИЗ БД И ОТПРАВИТЬ ЕЕ В ФУНКЦИЮ get_repository (аргумент flag_40, линия 33 в repository.py)
        repo = factory.get_repository(id_=id_players_sorted)
        context = {'table_html': repo.data.to_html()}
    except:
        raise Http404('Что-то пошло не так')
    return render(request, 'player/panda.html', context )


# переход на страничку для инвестирования
def to_MainWindow(request, player):
    try:
        player = Player.objects.get(Name=player)
        players = Factory.get_players()
        rating = list(players).index(player) + 1
        day = Factory.get_day()  # TODO поменять на день пользоватлея
        len_rating = len(players)
        id_actives = Factory.get_ids(day)
        actives = Active.objects.filter(Id__in=id_actives)

    except:
        raise Http404('Что-то пошло не так в to Main menue!')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day': day})


# переход на страницу с графиком
def to_top_players(request, player_nam):
    try:
        player = Player.objects.get(Name=player_nam)
        day = Factory.get_day()
        players = Factory.get_players(game_id=player.CurrentGameID)
        rating = list(players).index(player) + 1
        user_choices = Factor.objects.filter(UserID=player, UserID__CurrentGameID=player.CurrentGameID).order_by('-Day')
        years = json.dumps(list(range(1, day + 1)))
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/statistica.html", {'years': years, 'player': player, 'user_choices': user_choices,
                                                      'players': players, 'rating': rating})


# страница регистрации пользователя :переход на страницу с рейтингом/админку
def to_personal_page(request):
    try:
        game_id = Factory.get_game_id()
        if request.POST['user'] == 'adminPage':
            try:
                day = Factory.get_day(game_id=game_id)
                user_factors = Factor.objects.filter(Day=day, UserID__CurrentGameID=game_id)
                actives = Active.objects.all()
                players = Factory.get_players()
            except:
                raise Http404('Что-то пошло не так в to_admin_page')
            return render(request, "player/AdminPage.html",
                          {'counter': len(user_factors), 'q': len(players), 'actives': actives,
                           'players': players, 'day': day, 'game_id': game_id})

        a = Player.objects.filter(Name=request.POST['user'])
        if len(a) == 0:
            new_player = request.POST['user'].strip()  # проверка на то, что имя нормальное
            game_id = Factory.get_game_id()
            player = Player(Name=new_player, CurrentGameID=game_id)
            player.save()
        else:
            player = a[0]
            game_id = player.CurrentGameID
        players = Factory.get_players(game_id)
        rating = list(players).index(player) + 1  # TODO : действительно ли нужен такой рейтинг?
    except:
        raise Http404('Что-то пошло не так')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})


# переход на страницу с рейтингом не со стр регистрации, а с другого любого места
def to_top(request, player):
    try:
        a = Player.objects.filter(Name=player)
        player = a[0]
        players = Factory.get_players(game_id=player.CurrentGameID)
        rating = list(players).index(player) + 1
    except:
        raise Http404('Либо не нашел пользователя, либо других пользователей, либо рейтинг неправильный')
    return render(request, "player/Personal Page.html", {'player': player, 'players': players, 'rating': rating})


# перезагрузка страницы с инвестированием не знаю, почему - разобраться
def next_step(request, play):
    try:
        st_only = False  # TODO почему-то дублирует функицю to_MainWindow
        player = Player.objects.get(Name=play)
        players = Factory.get_players(game_id=player.CurrentGameID)
        rating = list(players).index(player) + 1
        flag = Admin.objects.order_by('-Day')[0].Day
        day = Factory.get_day(game_id=player.CurrentGameID)

        if player.Day == flag:
            pass
        len_rating = len(players)
        id_actives = Factory.get_ids(day)
        actives = Active.objects.filter(
            Id__in=id_actives)  # TODO можно сделать так, чтобы в разных играх было доступно разное количество активов
    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day': day})


# Кнопка, отвечающая за смену имени в админке И за простую загрузку админки с URL
def to_admin_page(request):
    try:
        game_id = Factory.get_game_id()
        day = Factory.get_day(game_id=game_id)
        try:
            a = Player.objects.filter(Name=request.POST['user'])[0]
            Factory.get_fake_name()
            a.Name = next(Factory.get_fake_name()) + str(np.random.randint(2, 20) ** 2 % 79)
            a.save()
        except:
            pass

        user_factors = Factor.objects.filter(Day=day, UserID__CurrentGameID=game_id)
        players = Factory.get_players()
        actives = Active.objects.all()  # todo допилить админскую страничку
        counter = len(user_factors)
        q = len(players)
    except:
        raise Http404('Что-то пошло не так в to_admin_page')
    return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                     'players': players, 'day': day, 'game_id': game_id})


# Теперь пошли функции с логикой

# Логика инвестирования со стороны игрока - Игроком нажата клавиша (подтвердить выбор)
def make_choice(request, player_name):
    try:
        st_only = False
        player = Player.objects.get(Name=player_name)

        # player.Day = player.Day + 1 #TODO Позже перестать использовать день как флаг что игрок сделал ход
        # player.save() # не учел где мы используем день, как флаг
        day = Factory.get_day(game_id=player.CurrentGameID)
        # player.save()
        players = Factory.get_players(game_id=player.CurrentGameID)
        rating = list(players).index(player) + 1
        ##
        len_rating = len(players)
        id_actives = Factory.get_ids(day)
        actives = Active.objects.filter(Id__in=id_actives)
        ##
        a = request.POST.get('activeA')
        b = request.POST.get('activeB')
        c = request.POST.get('activeС')
        number_of_not_chosen_options = 0
        if not a:
            a = 'Банк'
            number_of_not_chosen_options += 1
        if not b:
            b = 'Банк'
            number_of_not_chosen_options += 1
        if not c:
            c = 'Банк'
            number_of_not_chosen_options += 1
        act_a = Active.objects.get(Name__startswith=a)
        act_b = Active.objects.get(Name__startswith=b)
        act_c = Active.objects.get(Name__startswith=c)
        user_factors = Factor(Name1=act_a, Name2=act_b, Name3=act_c, Day=day,
                              UserID=player, Money_in=player.sum_active(),
                              Not_chosen_number=number_of_not_chosen_options)
        factor = Factor.objects.filter(Day=day, UserID=player, UserID__CurrentGameID=player.CurrentGameID)
        if len(factor) != 0:
            factor.delete()
        user_factors.save()
        factor = Factor.objects.filter(Day=day, UserID__CurrentGameID=player.CurrentGameID)
        if player.Day <= day and len(factor) < len(players) > 1:
            player.Day = player.Day + 1
            player.save()
        if len(players) > 1000000:
            factory = Factory()
            empty_choice = 'bank'
            flag = True
            day1 = day
            was_more_than_40 = Factory.get_day(game_id=player.CurrentGameID,
                                               was_more_fourty=True)  # !!!! Проверить, как работает
            Admin.objects.filter(Game_id=player.CurrentGameID).delete()
            user_factors = Factor.objects.filter(Day=day,
                                                 UserID__CurrentGameID=player.CurrentGameID)  # достаем все выборы за этот день
            # TODO проверить, как долго работает запрос вверху
            players = Factory.get_players(game_id=player.CurrentGameID)
            new_day = Admin(Day=day + 1, Was_more_fourty=was_more_than_40, Game_id=player.CurrentGameID)
            new_day.save()  # просто меняем день на новый
            day = new_day.Day
            k = sorted(user_factors, key=lambda x: x.UserID.ID)  # отсортируем выборы юзеров по ид (отметим, что
            # выбрали только тех юзеров, которые сделали выбор в данном году)
            idshniki = [i.UserID.ID for i in k]  # чтобы был всегда один и тот же порядок
            id_players_sorted = sorted([i.ID for i in list(players)])
            # TODO ВОТ ТУТ НАДО ДОСТАТЬ ПЕРЕМЕННУЮ ИЗ БД И ОТПРАВИТЬ ЕЕ В ФУНКЦИЮ get_repository (аргумент flag_40, линия 33 в repository.py)
            game1 = factory.get_repository(id_players_sorted,
                                           # TODO непонятно, как будут инициализироваться эти репозитории при двух играх одновременно
                                           flag_40=was_more_than_40)  # нициализируем репозиторий только по тем юзерам, которые сделали
            # первый ход. Те, кто не сделали первых ход в дальнейшем будут игнорироваться. - Это можно пофиксить через
            # репозиторий. Если это не первый год, то вызывается уже существующий репозиторий
            if len(idshniki) < len(game1.id_):
                flag = False  # если тех, кто сделал выбор в текущем году меньше, чем тех, кто сделал выбор в первом году
                list_of_actives_a = []
                list_of_actives_b = []
                list_of_actives_c = []
                dict_k = {el.UserID.ID: el for el in k}
                k = []
                default_act = Active.objects.get(Name_eng=empty_choice)
                for i in game1.id_:
                    player_ = Player.objects.get(ID__exact=i)
                    k.append(player_)
                    if i in dict_k:
                        elem = dict_k[i]
                        list_of_actives_a.append(elem.Name1.Name_eng)
                        list_of_actives_b.append(elem.Name2.Name_eng)
                        list_of_actives_c.append(elem.Name3.Name_eng)
                    else:
                        list_of_actives_a.append(empty_choice)
                        list_of_actives_b.append(empty_choice)
                        list_of_actives_c.append(empty_choice)
                        Factor(Day=day1, UserID=player_, Name1=default_act, Name2=default_act,
                               Name3=default_act, Money_in=player.sum_active(),
                               Not_chosen_number=3).save()  # ту логику лучше убрать в репозиторий
                    #  до этого все строчки про то, как преобразовать в нужный вид полученные данные + для тех, кто не
                    # сделал выбор - деньги по-умолчанию в банке
                game1.Choice(day1,
                             list_of_actives_a,
                             list_of_actives_b,
                             list_of_actives_c

                             )  # делаем выбор
            else:
                a = [i.Name1.Name_eng for i in k]
                b = [i.Name2.Name_eng for i in k]
                c = [i.Name3.Name_eng for i in k]
                game1.Choice(day1,
                             [i.Name1.Name_eng for i in k],
                             [i.Name2.Name_eng for i in k],
                             [i.Name3.Name_eng for i in k]
                             )
            dataframe, was_more_than_40 = game1.Gamble(day1)  # проводим расчёты
            # TODO ВОТ ТУТ Я ДОСТАЛ ЭТУ ПЕРЕМЕННУЮ И ЕЕ ТЕПЕРЬ НАДО КАК-ТО СОХРАНИТЬ В БД - ОНА ОДНА НА ВСЕХ
            i = 0
            act_a = 'asset_' + str(day1) + '_1'
            act_b = 'asset_' + str(day1) + '_2'
            act_c = 'asset_' + str(day1) + '_3'
            # act_a_historical = 'asset_' + str(day1) + '_1_' + 'for_dohod'
            # act_b_historical = 'asset_' + str(day1) + '_2_' + 'for_dohod'
            # act_c_historical = 'asset_' + str(day1) + '_3_' + 'for_dohod'

            for a, b, c, d, e, f, g in game1.data[[act_a, act_b, act_c,  # a, b, c, aa, bb, cc, d, e, f, g
                                                   # act_a_historical,act_b_historical, act_c_historical,
                                                   'educ', 'mortgage_count', 'further_mortgage',
                                                   'now_mortgage']].to_numpy():
                user = k[i]
                if flag:
                    user = user.UserID  # тут просто был  просчет с юзером и идшником
                user.next_year(np.round(a, 4), np.round(b, 4), np.round(c, 4), e, f, g, d, day)  # aa,bb,cc
                user.Education = d
                user.save()
                f = user.factor_set.filter(Day=day1)[0]
                f.ActA_increase = user.percentage_increase_active_a()
                f.ActB_increase = user.percentage_increase_active_b()
                f.ActC_increase = user.percentage_increase_active_c()
                f.Money_out = user.sum_active()
                f.save()
                i += 1
            Admin.objects.filter(Game_id=player.CurrentGameID).delete()
            new_day = Admin(Day=day, Was_more_fourty=was_more_than_40, Game_id=player.CurrentGameID)
            new_day.save()  # просто меняем день на новый
            day = new_day.Day
            players = Factory.get_players(game_id=player.CurrentGameID)


    except:
        raise Http404('Что-то пошло не так в make_chio')
    return render(request, "player/mainWindow.html", {'player': player, 'len_rating': len_rating,
                                                      'players': players,
                                                      'actives': actives, 'rating': rating, 'day': day})


# factory = Factory()


def next_day_admin(request, year):  # функционал всей админики - когда админ что-то нажал
    try:
        game_id = Factory.get_game_id()
        start_time = time.time()
        factory = Factory()
        day = Factory.get_day(game_id=game_id)  # Получаем текущий день от админа
        day1 = day
        id_actives = factory.get_ids(day)
        actives_names = Active.objects.filter(Id__in=id_actives).values_list('Name_eng', flat=True)
        flag = True
        was_more_than_40 = Factory.get_day(game_id=game_id, was_more_fourty=True)
        Admin.objects.filter(Game_id=game_id).delete()  # удаляем этот день из базы
        user_factors = Factor.objects.filter(Day=day, UserID__CurrentGameID=game_id)  # достаем все выборы за этот день
        players = Factory.get_players(game_id=game_id)
        actives = Active.objects.all()
        print("--- %s seconds ---, время на подгрузку объектов" % (time.time() - start_time))
        if int(year) == 400:  # если нажата кнопка превести всех пользователей в состояние по-умлочанию
            newday = Admin(Day=1, Was_more_fourty=was_more_than_40, Game_id=game_id)  # сохраняем день на 1
            newday.save()
            Factor.objects.filter(UserID__CurrentGameID=game_id).delete()
            for i in players:
                i.obnulit()  # у всех игроков тоже обнуляем день и активы по умолчанию
                i.save()

            day = 1  # загружаем 1й день
            print("--- %s seconds ---время на работу всей программы на обнуление года" % (time.time() - start_time))
            return render(request, "player/AdminPage.html",
                          {'counter': len(user_factors), 'q': len(players), 'actives': actives,
                           'players': players, 'day': day, 'game_id': game_id})
        if int(year) == 500:  # если нажата кнопка удалить всех пользователей
            players.delete()  # удаляем пользователей
            Admin(Day=day1, Game_id=game_id).save()  # день сохраняем текущий
            counter = len(user_factors)
            q = len(players)
            print("--- %s seconds ---время на работу всей программы на удаление всех пользователей" % (
                        time.time() - start_time))
            return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                             'players': players, 'day': day, 'game_id': game_id})

        if int(year) == 600:  # если нажата кнопка - загрузить тестовый массив юзеров - можно убрать в репозиторий
            fake_names = Factory.get_fake_name(num_of_names=30,
                                               add_custom_names=True)  # TODO придумать, где хранить ноличество фейковых игроков (это должн быть где-то захоркодено в .env)
            created = Factory.create_bots(fake_names, game_id=game_id)
            d = Admin(Day=day, Game_id=game_id)  # сохраняем текущий день и показываем всех пользователей
            d.save()
            players = Factory.get_players(game_id=game_id)
            counter = len(user_factors)
            q = len(players)
            print("--- %s seconds ---время на работу всей программы на загрузку тестовых юзеров" % (
                        time.time() - start_time))
            return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                             'players': players, 'day': day, 'game_id': game_id})
        if int(year) == 1000 or int(year) == 0:  # если нажата кнопка - предыдущий год. тогда
            if day == 0:  # нельзя уходить в отрицуательные значения - мб добавить что
                day += 1
            new_day = Admin(Day=day - 1, Game_id=game_id)
            for player in players:
                player.one_year_back()
                player.save()
            fact_del = Factor.objects.filter(Day__gte=day, UserID__CurrentGameID=game_id)
            fact_del.delete()
        else:
            new_day = Admin(Day=day + 1, Was_more_fourty=was_more_than_40, Game_id=game_id)
        new_day.save()  # просто меняем день на новый
        day = new_day.Day

        # now make calculations:
        if int(year) != 1000 and int(year) != 0:  # если нажата кнопка следующий год
            time_next_y = time.time()
            k = sorted(user_factors, key=lambda x: x.UserID.ID)  # отсортируем выборы юзеров по ид (отметим, что
            # выбрали только тех юзеров, которые сделали выбор в данном году)
            idshniki = [i.UserID.ID for i in k]  # чтобы был всегда один и тот же порядок
            id_players_sorted = sorted([i.ID for i in list(players)])
            # TODO ВОТ ТУТ НАДО ДОСТАТЬ ПЕРЕМЕННУЮ ИЗ БД И ОТПРАВИТЬ ЕЕ В ФУНКЦИЮ get_repository (аргумент flag_40, линия 33 в repository.py)
            game1 = factory.get_repository(id_players_sorted,
                                           flag_40=was_more_than_40)  # нициализируем репозиторий только по тем юзерам, которые сделали
            # первый ход. Те, кто не сделали первых ход в дальнейшем будут игнорироваться. - Это можно пофиксить через
            # репозиторий. Если это не первый год, то вызывается уже существующий репозиторий
            if len(idshniki) < len(game1.id_):
                flag = False  # если тех, кто сделал выбор в текущем году меньше, чем тех, кто сделал выбор в первом году
                list_of_actives_a = []
                list_of_actives_b = []
                list_of_actives_c = []
                dict_k = {el.UserID.ID: el for el in k}
                k = []
                for i in game1.id_:
                    player_ = Player.objects.get(ID__exact=i)
                    k.append(player_)
                    if i in dict_k:
                        elem = dict_k[i]
                        list_of_actives_a.append(elem.Name1.Name_eng)
                        list_of_actives_b.append(elem.Name2.Name_eng)
                        list_of_actives_c.append(elem.Name3.Name_eng)
                    else:
                        # default_act1 = Active.objects.get(Name_eng=actives_names[np.random.choice(len(actives_names))])
                        # default_act2 = Active.objects.get(Name_eng=actives_names[np.random.choice(len(actives_names))])
                        # default_act3 = Active.objects.get(Name_eng=actives_names[np.random.choice(len(actives_names))])
                        default_act1 = Active.objects.get(Name_eng='bank')
                        default_act2 = Active.objects.get(Name_eng='bank')
                        default_act3 = Active.objects.get(Name_eng='bank')
                        list_of_actives_a.append(default_act1.Name_eng)
                        list_of_actives_b.append(default_act2.Name_eng)
                        list_of_actives_c.append(default_act3.Name_eng)

                        a = Factor(Day=day1, UserID=player_, Name1=default_act1, Name2=default_act2,
                                   Name3=default_act3, Money_in=player_.sum_active(),
                                   Not_chosen_number=3).save()  # ту логику лучше убрать в репозиторий
                    #  до этого все строчки про то, как преобразовать в нужный вид полученные данные + для тех, кто не
                    # сделал выбор - деньги по-умолчанию в банке      
                print("--- %s seconds --- время до чойса в next_year" % (time.time() - time_next_y))
                game1.Choice(day1,
                             list_of_actives_a,
                             list_of_actives_b,
                             list_of_actives_c

                             )  # делаем выбор
            else:
                a = [i.Name1.Name_eng for i in k]
                b = [i.Name2.Name_eng for i in k]
                c = [i.Name3.Name_eng for i in k]
                game1.Choice(day1,
                             [i.Name1.Name_eng for i in k],
                             [i.Name2.Name_eng for i in k],
                             [i.Name3.Name_eng for i in k]
                             )
            time_gambl = time.time()
            dataframe, was_more_than_40 = game1.Gamble(day1)  # проводим расчёты
            print("--- %s seconds -- время гэмблинга-" % (time.time() - time_gambl))
            time_aft_gambl = time.time()
            # TODO ВОТ ТУТ Я ДОСТАЛ ЭТУ ПЕРЕМЕННУЮ И ЕЕ ТЕПЕРЬ НАДО КАК-ТО СОХРАНИТЬ В БД - ОНА ОДНА НА ВСЕХ
            i = 0
            act_a = 'asset_' + str(day1) + '_1'
            act_b = 'asset_' + str(day1) + '_2'
            act_c = 'asset_' + str(day1) + '_3'
            # act_a_historical = 'asset_' + str(day1) + '_1_' + 'for_dohod'
            # act_b_historical = 'asset_' + str(day1) + '_2_' + 'for_dohod'
            # act_c_historical = 'asset_' + str(day1) + '_3_' + 'for_dohod'

            for a, b, c, d, e, f, g in game1.data[[act_a, act_b, act_c,  # a, b, c, aa, bb, cc, d, e, f, g
                                                   # act_a_historical,act_b_historical, act_c_historical,
                                                   'educ', 'mortgage_count', 'further_mortgage',
                                                   'now_mortgage']].to_numpy():
                user = k[i]
                if flag:
                    user = user.UserID  # тут просто был  просчет с юзером и идшником
                user.next_year(np.round(a, 4), np.round(b, 4), np.round(c, 4), e, f, g, d, day)  # aa,bb,cc
                user.Education = d
                user.save()
                f = user.factor_set.filter(Day=day1)[0]
                f.ActA_increase = user.percentage_increase_active_a()
                f.ActB_increase = user.percentage_increase_active_b()
                f.ActC_increase = user.percentage_increase_active_c()
                f.Money_out = user.sum_active()
                f.save()
                i += 1
        Admin.objects.filter(Game_id=game_id).delete()
        new_day = Admin(Day=day, Was_more_fourty=was_more_than_40, Game_id=game_id)
        new_day.save()  # просто меняем день на новый
        day = new_day.Day
        players = Factory.get_players(game_id=game_id)
        counter = len(Factor.objects.filter(Day=day, UserID__CurrentGameID=game_id))
        q = len(players)
        print("--- %s seconds вроемя на работу после гэмблинга" % (time.time() - time_aft_gambl))
        print("--- %s seconds ---время на работу всей программы" % (time.time() - start_time))
    except:
        raise Http404('Что-то пошло не так в to_admin_page')

    return render(request, "player/AdminPage.html", {'counter': counter, 'q': q, 'actives': actives,
                                                     'players': players, 'day': day, 'game_id': game_id})
