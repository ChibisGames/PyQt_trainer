import sys, os, sqlite3
from random import randint, sample
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QAction, QLabel


class DataTaker:
    def __init__(self):
        self.con = sqlite3.connect("data/registr.db")
        self.cur = self.con.cursor()

    def save_login(self, login):
        self.login = login

    def open_stats(self):
        self.stat_71 = self.cur.execute("""SELECT n71 FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.stat_72 = self.cur.execute("""SELECT n72 FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.stat_7v = self.cur.execute("""SELECT n7v FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.stat_8a = self.cur.execute("""SELECT n8a FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]

        self.try_71 = self.cur.execute("""SELECT trys71 FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.try_72 = self.cur.execute("""SELECT trys72 FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.try_7v = self.cur.execute("""SELECT trys7v FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]
        self.try_8a = self.cur.execute("""SELECT trys8a FROM Users 
        WHERE UserLogin = """ + "'" + self.login + "'").fetchall()[0][0]

    def save(self):
        self.cur.execute("""UPDATE Users SET n71 = '""" + str(self.stat_71) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET trys71 = '""" + str(self.try_71) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET n72 = '""" + str(self.stat_72) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET trys72 = '""" + str(self.try_72) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET n7v = '""" + str(self.stat_7v) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET trys7v = '""" + str(self.try_7v) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET n8a = '""" + str(self.stat_8a) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.cur.execute("""UPDATE Users SET trys8a = '""" + str(self.try_8a) + """' 
        WHERE UserLogin = '""" + self.login + "'")
        self.con.commit()


class EnterWindow(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        uic.loadUi('data/enter.ui', self)
        self.btn_singin.clicked.connect(self.sing_in)
        self.btn_singup.clicked.connect(self.sing_up)
        self.anonim.clicked.connect(self.f_anonim)

    def sing_in(self):

        self.widget_window = Action(typ='in')
        self.widget_window.show()
        self.close()

    def sing_up(self):
        self.widget_window = Action(typ='up')
        self.widget_window.show()
        self.close()

    def f_anonim(self):
        dbtaker.save_login('Anonymous')
        self.widget_window = Choice()
        self.widget_window.show()
        self.close()


class Action(QWidget):
    def __init__(self, typ='', *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        uic.loadUi('data/action.ui', self)
        self.typ = typ
        if typ == 'in':
            self.info_label.setText('Вход')
            self.actoin_btn.setText('Вход')
            self.setWindowTitle('Вход')
        if typ == 'up':
            self.info_label.setText('Регистрация')
            self.actoin_btn.setText('Регистрация')
            self.setWindowTitle('Регистрация')
        self.actoin_btn.clicked.connect(self.check_log_pass)

    def check_log_pass(self):
        def check_login(logins):
            def probel_login(log):
                if ' ' in log:
                    return False
                return True
            if probel_login(logins):
                return True
            return False

        def passworld_check(passworld):
            def pas_len(password):
                if len(password) > 8:
                    return True
                return False

            def probel_password(password):
                if ' ' in password:
                    return False
                return True

            def low_and_up(password: str):
                lower, upper = False, False
                for i in password:
                    if lower and upper:
                        return True
                    if i.islower():
                        lower = True
                    if i.isupper():
                        upper = True
                return False

            def dig(password: str):
                for i in '1234567890':
                    if i in password:
                        return True

            def combat(password: str):
                s = password.lower()
                for i in range(2, len(combat_s) + 1):
                    if combat_s[i - 2:i + 1] in s:
                        return False
                return True

            combat_s = 'qwertyuiop!asdfghjkl!zxcvbnm!йцукенгшщзхъ!фывапролджэё!ячсмитьбю'
            p = passworld
            if pas_len(p) and low_and_up(p) and dig(p) and combat(p) and probel_password(p):
                return True
            return False

        log_input = str(self.line_log.text())
        pas_input = str(self.line_pas.text())

        # Проходит вход
        if self.typ == 'in':
            try:
                con = sqlite3.connect("data/registr.db")
                cur = con.cursor()
                log_in_data = cur.execute("""SELECT UserLogin FROM Users 
                WHERE UserLogin = '""" + log_input + "'").fetchall()
                pas_in_data = cur.execute("""SELECT Password FROM Users
                WHERE UserLogin = '""" + log_input + "'").fetchall()
                con.close()
                if str(log_in_data[0][0]) == log_input and pas_input == str(pas_in_data[0][0]):
                    # Открытие строки статистики
                    dbtaker.save_login(log_input)
                    dbtaker.open_stats()
                    self.action_battoun()
                else:
                    self.result_lab.setText('Неверный логин или пароль.')
            except Exception:
                self.result_lab.setText('Неверный логин или пароль.')
        # Проходит регистрация
        if self.typ == 'up':
            try:
                con = sqlite3.connect("data/registr.db")
                cur = con.cursor()
                log_in_data = cur.execute("""SELECT UserLogin FROM Users 
                WHERE UserLogin = '""" + log_input + "'").fetchall()
                try:
                    if  log_in_data[0][0] == log_input:
                        self.result_lab.setText('Такой логин уже существует или пароль не соответствует требованиям.')
                except IndexError:
                    if passworld_check(pas_input) and check_login(log_input):
                        cur.execute("""INSERT INTO Users(UserLogin, Password) 
                        VALUES('""" + log_input + "', '" + pas_input + "')")
                        con.commit()
                        con.close()
                        dbtaker.save_login(log_input)
                        dbtaker.open_stats()
                        self.action_battoun()
                    else:
                        self.result_lab.setText('Такой логин уже существует или пароль не соответствует требованиям.')
            except Exception:
                con.close()
                self.result_lab.setText('Неверный логин или пароль.')


    def action_battoun(self):
        self.widget_window = Choice()
        self.widget_window.show()
        self.close()


class Choice(QMainWindow): # Создаём окно с выбором заданий
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        uic.loadUi('data/choice.ui', self)
        self.num_8a.clicked.connect(self.number_8a)
        self.num_7_1.clicked.connect(self.number_7_1)
        self.num_7_2.clicked.connect(self.number_7_2)
        self.num_7v.clicked.connect(self.number_7v)
        self.reload_stats.clicked.connect(self.stat_reload)
        self.la_login_2.setText(dbtaker.login)
        if dbtaker.login != 'Anonymous': # сделать обновление страницы
            self.ltry71.setText(str(dbtaker.try_71))
            self.ltry72.setText(str(dbtaker.try_72))
            self.ltry7v.setText(str(dbtaker.try_7v))
            self.ltry8a.setText(str(dbtaker.try_8a))
            if dbtaker.try_71 == 0:
                self.lmb71.setText('0.0')
            else:
                self.lmb71.setText(str(round(dbtaker.stat_71 / dbtaker.try_71, 3)))
            if dbtaker.try_72 == 0:
                self.lmb72.setText('0.0')
            else:
                self.lmb72.setText(str(round(dbtaker.stat_72 / dbtaker.try_72, 3)))
            if dbtaker.try_7v == 0:
                self.lmb7v.setText('0.0')
            else:
                self.lmb7v.setText(str(round(dbtaker.stat_7v / dbtaker.try_7v, 3)))
            if dbtaker.try_8a == 0:
                self.lmb8a.setText('0.0')
            else:
                self.lmb8a.setText(str(round(dbtaker.stat_8a / dbtaker.try_8a, 3)))
        else:
            self.lmb71.setText('-')
            self.lmb72.setText('-')
            self.lmb7v.setText('-')
            self.lmb8a.setText('-')
            self.ltry71.setText('-')
            self.ltry72.setText('-')
            self.ltry7v.setText('-')
            self.ltry8a.setText('-')

    def number_8a(self):
        self.widget_window = QNum8a()
        self.widget_window.show()

    def number_7_1(self):
        self.widget_window = QNum71()
        self.widget_window.show()

    def number_7_2(self):
        self.widget_window = QNum72()
        self.widget_window.show()

    def number_7v(self):
        self.widget_window = QNum7v()
        self.widget_window.show()

    def stat_reload(self):
        if dbtaker.login != 'Anonymous': # сделать обновление страницы
            self.ltry71.setText(str(dbtaker.try_71))
            self.ltry72.setText(str(dbtaker.try_72))
            self.ltry7v.setText(str(dbtaker.try_7v))
            self.ltry8a.setText(str(dbtaker.try_8a))
            if dbtaker.try_71 == 0:
                self.lmb71.setText('0.0')
            else:
                self.lmb71.setText(str(round(dbtaker.stat_71 / dbtaker.try_71, 3)))
            if dbtaker.try_72 == 0:
                self.lmb72.setText('0.0')
            else:
                self.lmb72.setText(str(round(dbtaker.stat_72 / dbtaker.try_72, 3)))
            if dbtaker.try_7v == 0:
                self.lmb7v.setText('0.0')
            else:
                self.lmb7v.setText(str(round(dbtaker.stat_7v / dbtaker.try_7v, 3)))
            if dbtaker.try_8a == 0:
                self.lmb8a.setText('0.0')
            else:
                self.lmb8a.setText(str(round(dbtaker.stat_8a / dbtaker.try_8a, 3)))
        else:
            self.lmb71.setText('-')
            self.lmb72.setText('-')
            self.lmb8a.setText('-')
            self.ltry71.setText('-')
            self.ltry72.setText('-')
            self.ltry8a.setText('-')


class PatternNumWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        super().__init__()
        uic.loadUi('data/pattern_num.ui', self)
        self.correct_ans_counter = 0
        self.true = False
        self.check_answer.clicked.connect(self.checking_answer)


    def checking_answer(self):
        if self.lineed.text() == self.answer1:
            self.corr_notcorr.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed.setEnabled(False)
        if self.lineed_2.text() == self.answer2:
            self.corr_notcorr_2.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_2.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_2.setEnabled(False)
        if self.lineed_3.text() == self.answer3:
            self.corr_notcorr_3.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_3.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_3.setEnabled(False)
        if self.lineed_4.text() == self.answer4:
            self.corr_notcorr_4.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_4.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_4.setEnabled(False)
        if self.lineed_5.text() == self.answer5:
            self.corr_notcorr_5.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_5.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_5.setEnabled(False)
        if self.lineed_6.text() == self.answer6:
            self.corr_notcorr_6.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_6.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_6.setEnabled(False)
        if self.lineed_7.text() == self.answer7:
            self.corr_notcorr_7.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_7.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_7.setEnabled(False)
        if self.lineed_8.text() == self.answer8:
            self.corr_notcorr_8.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_8.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_8.setEnabled(False)
        if self.lineed_9.text() == self.answer9:
            self.corr_notcorr_9.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_9.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_9.setEnabled(False)
        if self.lineed_10.text() == self.answer10:
            self.corr_notcorr_10.setStyleSheet("background-color:rgb(50, 200, 50)")
            self.correct_ans_counter += 1
        else:
            self.corr_notcorr_10.setStyleSheet("background-color:rgb(200, 50, 50)")
        self.lineed_10.setEnabled(False)
        if not self.true:
            self.true = True
            if dbtaker.login != 'Anonymous':
                if self.__class__.__name__ == 'QNum71':
                    dbtaker.stat_71 += self.correct_ans_counter
                    dbtaker.try_71 += 1
                    dbtaker.save()

                elif self.__class__.__name__ == 'QNum72':
                    dbtaker.stat_72 += self.correct_ans_counter
                    dbtaker.try_72 += 1
                    dbtaker.save()

                elif self.__class__.__name__ == 'QNum7v':
                    dbtaker.stat_7v += self.correct_ans_counter
                    dbtaker.try_7v += 1
                    dbtaker.save()

                elif self.__class__.__name__ == 'QNum8a':
                    dbtaker.stat_8a += self.correct_ans_counter
                    dbtaker.try_8a += 1
                    dbtaker.save()


class QNum71(PatternNumWidget): # Создаём окно задания 7-1
    def __init__(self):
        def sortic(end, first_end, second_end, third_end, four_end):
            if end in [0, 1]:
                return str(first_end)
            elif end in [2, 3]:
                return str(second_end)
            elif end == 4:
                return str(third_end)
            return str(four_end)

        super().__init__()
        # Само задание
        self.setWindowTitle('7-1 - Кодирование изображений')
        for num_step in range(10):
            rand_end = randint(0, 5)  # Определяем суть задания
            size_x = 2 ** randint(5, 10)
            size_y = 2 ** randint(5, 10)
            bite_for_pixel = randint(2, 10)
            weight_img = size_x * size_y * bite_for_pixel / 1024 / 8
            weight_img = int(weight_img) if int(weight_img) - weight_img == 0 else weight_img
            N_lots_colour = 2 ** bite_for_pixel
            if rand_end in [0, 1]:
                str_7_1 = f'Рисунок размером {size_x} на {size_y} пикселей занимает в памяти {weight_img} Кбайт\n' \
                          f'(без учёта сжатия). Найдите максимально возможное количество цветов в палитре изображения.'
            elif rand_end in [2, 3]:
                str_7_1 = f'Какой минимальный объём памяти (в Кбайт) нужно зарезервировать, ' \
                          f'чтобы можно было сохранить любое растровое изображение размером {size_x} на {size_y} ' \
                          f'пикселов при условии, что в изображении могут использоваться {N_lots_colour} различных ' \
                          f'цветов? В ответе запишите только целое число, единицу измерения писать не нужно. ' \
                          f'Если число дробное - запишите ответ через точку.'
            elif rand_end == 4:
                bite_for_pixel_2 = randint(1, bite_for_pixel - 1)
                N_lots_colour_2 = 2 ** bite_for_pixel_2
                weight_img_2 = size_x * size_y * bite_for_pixel_2 / 1024 / 8
                dis_weight = weight_img - weight_img_2
                dis_weight = int(dis_weight) if int(dis_weight) - dis_weight == 0 else dis_weight
                str_7_1 = f'После преобразования растрового {N_lots_colour}-цветного графического файла в ' \
                          f'формат: {N_lots_colour_2} цвета, его размер уменьшился на {dis_weight} Кбайт. ' \
                          f'Каков был размер исходного файла в Кбайтах?'
            else:
                bite_for_pixel_2 = randint(1, bite_for_pixel - 1)
                N_lots_colour_2 = 2 ** bite_for_pixel_2
                weight_img_2 = size_x * size_y * bite_for_pixel_2 / 1024 / 8
                dis_weight = weight_img / weight_img_2
                dis_weight = int(dis_weight) if int(dis_weight) - dis_weight == 0 else round(dis_weight, 2)
                str_7_1 = f'После преобразования растрового графического файла его объем уменьшился ' \
                          f'в {dis_weight} раза. Сколько цветов было в палитре первоначально, если после ' \
                          f'преобразования было получено растровое изображение того' \
                          f' же разрешения в {N_lots_colour_2}-цветной палитре?'
            if num_step == 0:
                self.lab.setText(str_7_1)
                self.answer1 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 1:
                self.lab_2.setText(str_7_1)
                self.answer2 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 2:
                self.lab_3.setText(str_7_1)
                self.answer3 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 3:
                self.lab_4.setText(str_7_1)
                self.answer4 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 4:
                self.lab_5.setText(str_7_1)
                self.answer5 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 5:
                self.lab_6.setText(str_7_1)
                self.answer6 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 6:
                self.lab_7.setText(str_7_1)
                self.answer7 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 7:
                self.lab_8.setText(str_7_1)
                self.answer8 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 8:
                self.lab_9.setText(str_7_1)
                self.answer9 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)
            elif num_step == 9:
                self.lab_10.setText(str_7_1)
                self.answer10 = sortic(rand_end, N_lots_colour, weight_img, weight_img, N_lots_colour)


class QNum72(PatternNumWidget): # Создаём окно задания 7-2
    def __init__(self):
        def sortic(end, first_end, second_end):
            if end == 0:
                return str(first_end)
            return str(second_end)

        super().__init__()
        # Само задание
        self.setWindowTitle('7-2 - Кодирование звука')
        for num_step in range(10):
            rand_end = randint(0, 1)
            list_ul = ['', '']
            discret = randint(2, 4) / randint(1, 2) # дискретизация
            discret = int(discret) if int(discret) - discret == 0 else discret
            permiss =  randint(2, 4) / randint(1, 2) # разрешение
            permiss = int(permiss) if int(permiss) - permiss == 0 else permiss
            rand_ul = randint(0, 1)
            cannal = randint(2, 5)
            time_b = randint(5, 80)
            volume = cannal * time_b
            if rand_ul == 0:
                list_ul[1] = 'выше'
                list_ul[0] = 'меньше'
                factor = permiss / discret
                while (volume * factor) % 1 != 0:
                    time_b += 1
                    volume = cannal * time_b
            else:
                list_ul[0] = 'выше'
                list_ul[1] = 'меньше'
                factor = discret / permiss
                while (volume * factor) % 1 != 0:
                    time_b += 1
                    volume = cannal * time_b
            time_a = int(factor * volume)
            str_7_2 = ''
            if rand_end == 0:
                str_7_2 = f'Музыкальный фрагмент был оцифрован и записан в виде файла без использования сжатия ' \
                          f'данных. Получившийся файл был передан в город А по каналу связи за {time_a} секунд.' \
                          f' Затем тот же музыкальный фрагмент был оцифрован повторно с разрешением в {permiss} ' \
                          f'раза {list_ul[0]} и частотой дискретизации в {discret} раза {list_ul[1]}, чем в ' \
                          f'первый раз. Сжатие данных не производилось. Полученный файл был передан в город Б; ' \
                          f'пропускная способность канала связи с городом Б в {cannal} раза выше, ' \
                          f'чем канала связи с городом А. Сколько секунд длилась передача файла в город Б? ' \
                          f'В ответе запишите только целое число, без единицы измерения.'
            elif rand_end == 1:
                str_7_2 = f'Музыкальный фрагмент был оцифрован и записан в виде файла без использования сжатия ' \
                          f'данных. Получившийся файл был передан в город А по каналу связи за {time_a} секунд. ' \
                          f'Затем тот же музыкальный фрагмент был оцифрован повторно с разрешением в {permiss} раз' \
                          f' {list_ul[0]} и частотой дискретизации в {discret} раз {list_ul[1]}, чем в первый ' \
                          f'раз. Сжатие данных не производилось. Полученный файл был передан в город Б за {time_b} ' \
                          f'секунд. Во сколько раз скорость пропускная способность канала связи с городом Б ' \
                          f'выше, чем канала связи с городом А? В ответе запишите только целое число.'
            if num_step == 0:
                self.lab.setText(str_7_2)
                self.answer1 = sortic(rand_end, time_b, cannal)
            elif num_step == 1:
                self.lab_2.setText(str_7_2)
                self.answer2 = sortic(rand_end, time_b, cannal)
            elif num_step == 2:
                self.lab_3.setText(str_7_2)
                self.answer3 = sortic(rand_end, time_b, cannal)
            elif num_step == 3:
                self.lab_4.setText(str_7_2)
                self.answer4 = sortic(rand_end, time_b, cannal)
            elif num_step == 4:
                self.lab_5.setText(str_7_2)
                self.answer5 = sortic(rand_end, time_b, cannal)
            elif num_step == 5:
                self.lab_6.setText(str_7_2)
                self.answer6 = sortic(rand_end, time_b, cannal)
            elif num_step == 6:
                self.lab_7.setText(str_7_2)
                self.answer7 = sortic(rand_end, time_b, cannal)
            elif num_step == 7:
                self.lab_8.setText(str_7_2)
                self.answer8 = sortic(rand_end, time_b, cannal)
            elif num_step == 8:
                self.lab_9.setText(str_7_2)
                self.answer9 = sortic(rand_end, time_b, cannal)
            elif num_step == 9:
                self.lab_10.setText(str_7_2)
                self.answer10 = sortic(rand_end, time_b, cannal)


class QNum7v(PatternNumWidget): # Создаём окно задания 7-1
    def __init__(self):
        super().__init__()
        # Само задание
        self.setWindowTitle('7v - Скорость передачи данных')
        for num_step in range(10):
            size = randint(5, 100)
            speed_log = randint(20, 22)
            arch = randint(2, 16) * 5
            time_arch = randint(10, 22)
            time_rearch = randint(1, 3)
            str_7v = f'Документ объёмом {size} Мбайт можно передать с одного компьютера на другой двумя способами:\n'\
            f'А) сжать архиватором, передать архив по каналу связи, распаковать;\n'\
            f'Б) передать по каналу связи без использования архиватора.\n'\
            f'Какой способ быстрее и насколько, если\n'\
            f'- средняя скорость передачи данных по каналу связи составляет 2^{speed_log} бит в секунду,\n'\
            f'- объём сжатого архиватором документа равен {arch}% от исходного,\n'\
            f'- время, требуемое на сжатие документа, - {time_arch} секунд, на распаковку - {time_rearch} секунды? \n'\
            f'В ответе напишите букву А, если способ А быстрее, или Б, если быстрее способ Б.'\
            f'Сразу после буквы напишите на сколько ЦЕЛЫХ секунд один способ быстрее другого. '\
            f'(Если способы равны в ответ напишите: А0)'\
            '  '
            ans_arch = (size * arch / 100 * 2 ** 23) / 2 ** speed_log + time_arch + time_rearch
            ans_not_arch = size * 2 ** 23 / 2 ** speed_log
            if ans_arch > ans_not_arch:
                answer = int(ans_arch - ans_not_arch)
                answer = 'Б' + str(answer)
            elif ans_arch == ans_not_arch:
                answer = 'А0'
            else:
                answer = int(ans_not_arch - ans_arch)
                answer = 'А' + str(answer)
            if num_step == 0:
                self.lab.setText(str_7v)
                self.answer1 = answer
            elif num_step == 1:
                self.lab_2.setText(str_7v)
                self.answer2 = answer
            elif num_step == 2:
                self.lab_3.setText(str_7v)
                self.answer3 = answer
            elif num_step == 3:
                self.lab_4.setText(str_7v)
                self.answer4 = answer
            elif num_step == 4:
                self.lab_5.setText(str_7v)
                self.answer5 = answer
            elif num_step == 5:
                self.lab_6.setText(str_7v)
                self.answer6 = answer
            elif num_step == 6:
                self.lab_7.setText(str_7v)
                self.answer7 = answer
            elif num_step == 7:
                self.lab_8.setText(str_7v)
                self.answer8 = answer
            elif num_step == 8:
                self.lab_9.setText(str_7v)
                self.answer9 = answer
            elif num_step == 9:
                self.lab_10.setText(str_7v)
                self.answer10 = answer


class QNum8a(PatternNumWidget): # Создаём окно задания 8а
    def __init__(self):
        # Функции-помошники
        def sortic(end, first_end, second_end, third_end):
            if end == 0:
                return first_end
            elif end == 1:
                return str(second_end)
            return str(third_end)

        def gen_answer_for_8a_third_end(count_sim, count_word, answer_num):
            counter = 0
            if count_word == 4:
                for s1 in sim:
                    for s2 in sim:
                        for s3 in sim:
                            for s4 in sim:
                                counter += 1
                                if s1 == answer_num:
                                    return counter
            else:
                for s1 in sim:
                    for s2 in sim:
                        for s3 in sim:
                            for s4 in sim:
                                for s5 in sim:
                                    counter += 1
                                    if s1 == answer_num:
                                        return counter

        def gen_answer_for_8a_first_end(count_sim, count_word, answer_num):
            counter = 0
            if count_word == 4:
                for s1 in sim:
                    for s2 in sim:
                        for s3 in sim:
                            for s4 in sim:
                                counter += 1
                                if counter == answer_num:
                                    return (s1 + s2 + s3 + s4)
            else:
                for s1 in sim:
                    for s2 in sim:
                        for s3 in sim:
                            for s4 in sim:
                                for s5 in sim:
                                    counter += 1
                                    if counter == answer_num:
                                        return (s1 + s2 + s3 + s4 +  s5)

        super().__init__()
        # Само задание
        self.setWindowTitle('8-a - Слова в алфавитном порядке')
        for num_step in range(10):
            rand_word = randint(4, 5)
            rand_sim = randint(3, 4)
            rand_end = randint(0, 2) # Определяем суть задания
            limit = rand_sim ** rand_word
            sim = sample(list_8a_sim, k=rand_sim)
            str_8a = f'Все {rand_word}-буквенные слова, составленные из букв {", ".join(sim)}, ' \
                     f'записаны в алфавитном порядке. Вот начало списка:\n'
            if rand_word == 4:
                for i in range(rand_sim):
                    str_sim = ''
                    str_sim += sim[0] + sim[0] + sim[0] + sim[i]
                    str_8a += str_sim + '\n'
                str_8a += sim[0] + sim[0] + sim[1] + sim[0] + '\n'
            else:
                for i in range(rand_sim):
                    str_sim = ''
                    str_sim += sim[0] + sim[0] + sim[0] + sim[0] + sim[i]
                    str_8a += str_sim + '\n'
                str_8a += sim[0] + sim[0] + sim[0] + sim[1] + sim[0] + '\n'
            if rand_end == 0:       # Требуется указать слово по номеру
                answer_num = randint(70, limit - 10)
                str_8a_end = f'Запишите слово, которое стоит на {answer_num}-м месте от начала списка'
            elif rand_end == 1:     # Требуется указать номер по слову
                answer_num = randint(70, limit - 10)
                str_8a_end = f'Укажите номер слова {gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num)}.'
            else:       # Требуется указать номер по первой букве
                answer_num = sample(sim[1:], k=1)[0]
                str_8a_end = f'Укажите номер первого слова, которое начинается с буквы {answer_num}.'
            str_8a += str_8a_end
            if num_step == 0:
                self.lab.setText(str_8a)
                self.answer1 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 1:
                self.lab_2.setText(str_8a)
                self.answer2 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 2:
                self.lab_3.setText(str_8a)
                self.answer3 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 3:
                self.lab_4.setText(str_8a)
                self.answer4 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 4:
                self.lab_5.setText(str_8a)
                self.answer5 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 5:
                self.lab_6.setText(str_8a)
                self.answer6 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 6:
                self.lab_7.setText(str_8a)
                self.answer7 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 7:
                self.lab_8.setText(str_8a)
                self.answer8 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 8:
                self.lab_9.setText(str_8a)
                self.answer9 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))
            elif num_step == 9:
                self.lab_10.setText(str_8a)
                self.answer10 = sortic(rand_end, gen_answer_for_8a_first_end(rand_sim, rand_word, answer_num),
                                      answer_num, gen_answer_for_8a_third_end(rand_sim, rand_word, answer_num))


def check_files():
    list_of_files = ['data/action.ui', 'data/choice.ui', 'data/enter.ui',
                     'data/pattern_num.ui', 'data/registr.db']
    for file in list_of_files:
        if not os.path.exists(file):
            print('Нехватка файлов')
            return False
    return True


list_8a_sim = ['А', 'О', 'У', 'К', 'Е', 'Р', 'Т', 'М', 'И'] # Нужные условия для заданий
if __name__ == '__main__' and check_files():
    app = QApplication(sys.argv)
    dbtaker = DataTaker()
    ex = EnterWindow()
    ex.show()
    sys.exit(app.exec())
