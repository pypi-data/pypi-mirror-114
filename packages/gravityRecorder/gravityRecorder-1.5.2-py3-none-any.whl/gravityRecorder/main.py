from traceback import format_exc
import datetime
from gravityRecorder import functions
from gravityRecorder.alerts import alert_funcs
from wsqluse.wsqluse import Wsqluse
from gravityRecorder import settings


class Recorder(Wsqluse):
    """ Класс, генерирующий факты взвешивания """
    def __init__(self, dbname, user, password, host, debug=False,
                 auto_table_name='auto',
                 records_table_name='records',
                 disputs_table_name='disputs'):
        Wsqluse.__init__(self, dbname, user, password, host, debug=debug)
        self.auto_table_name = auto_table_name
        self.records_table_name = records_table_name
        self.disputs_table_name = disputs_table_name

    def get_auto_protocol_info(self, auto_id):
        """ Вернуть информацию о протоколе авто по его id """
        protocol_name = functions.get_auto_protocol(self, auto_id)
        protocol_settings = functions.get_auto_protocol_settings(self,
                                                                 protocol_name,
                                                                 auto_id)
        return protocol_settings

    def register_car(self, car_number):
        """ Проверить, есть ли в таблице auto машина с таким гос.номером,
        если нет - зарегистрировать """
        auto_id = functions.check_car_registered(self, car_number)
        if not auto_id:
            auto_id = functions.register_new_car(self, car_number)
        return auto_id

    def init_round(self, weight, car_number, carrier=None, operator=None,
                   trash_cat=None, trash_type=None, notes=None, polygon_int=1,
                   *args, **kwargs):
        """
        Обработать взвешивание
        :param trash_cat:
        :param car_number:
        :param carrier:
        :param operator:
        :param trash_type:
        :param notes:
        :param polygon_int:
        :param args:
        :param kwargs:
        :return:
        """
        # Извлечь auto_id (уже зареганного или зарегать, если не зареган)
        auto_id = self.register_car(car_number)
        response = self.fix_weight_general(weight, trash_cat, trash_type, notes, operator,
                                auto_id, carrier,
                                datetime=datetime.datetime.now())
        self.reg_act_to_polygon(polygon_int, response['record_id'])
        response['auto_id'] = auto_id
        return response

    def get_rfid_by_carnum(self, carnum):
        """ Вернуть RFID-номер машины по его гос.номеру """
        command = "SELECT rfid FROM auto WHERE car_number='{}'".format(carnum)
        response = self.try_execute_get(command)
        return response

    def check_car_choose_mode(self, alerts, choose_mode, car_number, course):
        # Проверить, как была выбрана машина (вручную/автоматоически)
        rfid = self.get_rfid_by_carnum(car_number)[0][0]
        alerts = alert_funcs.check_car_choose_mode(rfid, alerts, choose_mode,
                                                   car_number, course)
        return alerts

    def get_rfid_by_id(self, auto_id):
        """ Вернуть RFID-номер машины по его ID """
        command = "SELECT rfid FROM auto WHERE id={}".format(auto_id)
        response = self.try_execute_get(command)
        return response

    def check_car(self, cargo, alerts):
        alerts = alert_funcs.cargo_null(cargo, alerts)
        return alerts

    def fast_car(self, carnum, alerts):
        # Проверить, не слишком ли быстро вернулась машина,
        # если да - дополнить алерт кодом из wsettings и вернуть
        print('\nИнициирована проверка на FastCar')
        timenow = datetime.datetime.now()
        command = "SELECT le.date from last_events le " \
                  "INNER JOIN auto a ON (le.car_id=a.id) " \
                  "where a.car_number='{}'".format(carnum)
        try:
            last_visit_date = self.try_execute_get(command)[0][0]
            alerts = alert_funcs.check_fast_car(last_visit_date, timenow,
                                                alerts)
        except:
            print('\tОшибка при проверке заезда')
            print(format_exc())
        return alerts

    def check_car_has_gross(self, auto_id):
        """
        :param auto_id:
        :return:
        Проверить взвешивала ли машина брутто
        """
        command = "select id from {} where auto='{}' and time_out is " \
                  "null".format(self.records_table_name, auto_id)
        response = self.try_execute_get(command)
        if len(response) > 0:
            return response[0][0]

    def add_alerts(self, alerts, rec_id):
        """
        Добавляет строку в таблицу disputs, где указываются данные об инциденте
        :param alerts: алерт
        :param rec_id: идентификатор записи
        :return:
        """
        timenow = datetime.datetime.now()
        command = "INSERT INTO disputs " \
                  "(date, records_id, alerts) " \
                  "VALUES ('{}', {}, '{}') " \
                  "ON CONFLICT (records_id) DO UPDATE SET " \
                  "alerts = disputs.alerts || '{}'"
        command = command.format(timenow, rec_id, alerts, alerts)
        self.try_execute(command)

    def update_last_events(self, auto_id, trash_cat, trash_type, carrier,
                           timestamp=None):
        """
        Обновляет запись в таблице last_events, где хранятся данные о последнем
        посещении авто
        :param auto_id: ID авто
        :param carrier: ID перевозчика
        :param trash_type: ID вида груза
        :param trash_cat: ID категории груза
        :param timestamp: Время посещения
        :return:
        """
        if not timestamp:
            timestamp = datetime.datetime.now()
        comm = "INSERT INTO last_events " \
               "(car_id, carrier, trash_type, trash_cat, date) " \
               "values ({},{},{},{},'{}') " \
               "ON CONFLICT (car_id) DO UPDATE " \
               "SET carrier={}, trash_cat={}, trash_type={}, date='{}'"
        command = comm.format(auto_id, carrier, trash_type, trash_cat,
                              timestamp, carrier, trash_cat, trash_type,
                              timestamp)
        return self.try_execute(command)

    def get_last_event(self, auto_id: int):
        """ Вернуть запись о последнем посещении авто из last_events """
        command = "SELECT * FROM last_events WHERE car_id={}".format(auto_id)
        response = self.get_table_dict(command)
        if response['status'] == 'success':
            return response['info'][0]

    def upd_old_num(self, old_carnum, new_carnum):
        # Обновляет старый номер на новый
        command = "UPDATE {} SET car_number='{}' WHERE car_number='{}'"
        command = command.format('auto', new_carnum, old_carnum)
        self.try_execute(command)

    def check_access(self, rfid):
        ''' Проверяет, разрешается ли машине въезд '''
        command = "SELECT rfid FROM {} WHERE rfid='{}'".format(s.auto, rfid)
        response = self.try_execute_get(command)
        if len(response) > 0:
            return True

    def fix_weight_general(self, weight, trash_cat, trash_type, notes,
                           operator, auto_id, carrier=None,
                           datetime=datetime.datetime.now()):
        have_gross = self.check_car_has_gross(auto_id)
        if have_gross:
            response = self.fix_weight_tare(auto_id, weight, notes, datetime)
            response['weight_stage'] = 'tare'
        else:
            response = self.fix_weight_gross(auto_id, weight, carrier,
                                             trash_cat, trash_type, notes,
                                             operator, datetime)
            response['weight_stage'] = 'gross'
        response['record_id'] = response.pop('info')[0][0]
        return response

    def fix_weight_tare(self, auto_id, weight_tare, notes, datetime=datetime.datetime.now()):
        """ Зафиксировать вес ТАРА """
        gross = self.get_gross(auto_id, self.records_table_name)        # Извлечь вес БРУТТО
        cargo = functions.get_cargo(gross, weight_tare)                 # Вычислить вес НЕТТО
        if weight_tare > gross and self.get_auto_protocol_info(auto_id)['name'] != 'rfid':
            old_gross = gross
            gross = weight_tare
            weight_tare = old_gross
        # Сформировать команду на обновление записи по auto_id
        sql_command = "UPDATE {} SET brutto={}, tara={}, cargo={}, time_out='{}', " \
                      "notes =  notes || 'Выезд: {}| ' " \
                      "WHERE auto={} and time_out is null"
        sql_command = sql_command.format(self.records_table_name,
                                         gross, weight_tare, abs(cargo),
                                         datetime, notes, auto_id)
        response = self.try_execute(sql_command)                        # Выполнить команду
        return response

    def get_gross(self, auto_id, records_table_name: str):
        command = "SELECT brutto FROM {} " \
                  "WHERE auto={} and time_out is null"
        command = command.format(records_table_name, auto_id)
        gross = self.try_execute_get(command)
        return gross[0][0]

    def fix_weight_gross(self, auto_id, weight, carrier, trash_cat, trash_type,
                         notes, operator, timenow=datetime.datetime.now()):
        """ Создать новую запись с брутто """
        command = """ INSERT INTO records (auto, brutto, time_in, carrier, 
                    trash_cat, trash_type, notes, operator) 
                    values (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""
        cursor, conn = self.get_cursor_conn()
        values = (auto_id, weight, timenow, carrier, trash_cat, trash_type,
                  'Въезд: {}| '.format(notes), operator)
        cursor.execute(command, values)
        response = cursor.fetchall()
        conn.commit()
        self.update_last_events(auto_id, trash_cat, trash_type, carrier)
        return {'status': 'success', 'info': response}    # response = [(int)]

    def delete_record(self, record_id, table_name=None):
        """ Удалить запись с id=record_id"""
        if not table_name:
            table_name = self.records_table_name
        command = "DELETE FROM {} WHERE id={}".format(table_name, record_id)
        response = self.try_execute(command)
        return response

    def reg_act_to_polygon(self, polygon_id:int, record_id:int):
        """ Зафиксировать акт за полигоном """
        return functions.register_act_to_polygon(self, polygon_id, record_id)

    def add_comment(self, record_id, comment, *args, **kwargs):
        """ ДОбавить комментарий к записи """
        command = "UPDATE {} set notes = notes || '... Добавочно: {}' where id={}"
        command = command.format(self.records_table_name, comment, record_id)
        self.try_execute(command)

    def close_opened_record(self, record_id, time_out=None, *args, **kwargs):
        """ Закрыть запись без тары """
        if not time_out:
            time_out = datetime.datetime.now()
        command = "UPDATE {} SET time_out='{}', tara=0, cargo=brutto WHERE id={}"
        command = command.format(self.records_table_name, time_out, record_id)
        alert = 'Запись была закрыта вручную |'
        self.add_alerts(alert, record_id)
        response = self.try_execute(command)
        return response

    def update_opened_record(self, record_id, car_number, carrier, trash_cat_id, trash_type_id,
                             comment, polygon=None, auto_id=None, *args, **kwargs):
        """ Изменить запись, у которой уже есть брутто """
        if auto_id is None:                 # Если auto_id = None (гос. номер вбит вручную, такой машины нет в таблице auto)
            auto_id = self.register_car(car_number)    # Зарегистрировать ее (завести запсиь в таблице auto)
        command = "UPDATE {} SET auto={}, carrier={}, trash_cat={}, " \
                  "trash_type={}, notes='{}' " \
                  "WHERE id={}"
        command = command.format(self.records_table_name, auto_id, carrier,
                                 trash_cat_id, trash_type_id, comment,
                                 record_id)
        response = self.try_execute(command)
        functions.add_change_notes(self, response['info'][0][0], comment)
        if polygon:
            # Если поддерживается DUO - изменить присваивание
            self.reg_act_to_polygon(polygon, response['info'][0][0])
        return {'status': 'success', 'info': 'Данные успешно изменены'}

    def get_unfinished_cycles(self, *args, **kwargs):
        """ Вернуть все открытые записи (без тары) """
        my_timedelta = datetime.datetime.now() - datetime.timedelta(minutes=5)
        command = "SELECT * FROM records WHERE time_out is null or time_out > '{}'"
        command = command.format(my_timedelta)
        response = self.get_table_dict(command)
        return response

    def get_history(self, time_start, time_end, what_time='time_in',
                    trash_cat=None, trash_type=None, carrier=None, auto_id=None,
                    polygon_object_id=None, alerts=None, *args, **kwargs):
        """ Вернуть статистику по заданным фильтрам """
        command = "SELECT rt.id as record_id, rt.trash_cat, rt.trash_type, rt.brutto, rt.cargo, rt.tara, rt.time_in, " \
                  "rt.time_out, rt.inside, rt.carrier, rt.notes, rt.operator, rt.wserver_sent, rt.wserver_get, " \
                  "rt.wserver_id, rt.auto, auto_table.rfid, dpo.id, at.alerts FROM {} rt " \
                  "LEFT JOIN {} auto_table ON (rt.auto=auto_table.id) " \
                  "LEFT JOIN {} dro ON (rt.id=dro.record) " \
                  "LEFT JOIN {} dpo ON (dro.owner = dpo.id) " \
                  "LEFT JOIN {} at ON (at.records_id=rt.id) " \
                  "WHERE {}::date>='{}' and {}::date<='{}'"
        command = command.format(self.records_table_name,
                                 self.auto_table_name,
                                 'duo_records_owning',
                                 'duo_pol_owners',
                                 'disputs',
                                 what_time, time_start, what_time, time_end)
        if auto_id:
            command += " and auto_table.id={}".format(auto_id)
        if alerts == 'да':
            command += " and not at.alerts is null"
        if alerts == 'нет':
            command += " and at.alerts is null"
        if trash_cat:
            command += " and trash_cat={}".format(trash_cat)
        if trash_type:
            command += " and trash_type={}".format(trash_type)
        if carrier:
            command += " and carrier={}".format(carrier)
        if polygon_object_id:
            command += " and dpo.id={}".format(polygon_object_id)
        response = self.get_table_dict(command)
        return response

    def get_table_info(self, tablename, only_active=True, *args, **kwargs):
        """ Возвращает все содержимое таблицы tablename для взаимодействия по API """
        # Проверить, разрешается ли отправлять данные об этой табоице
        if tablename in list(settings.send_allowed_table_rules.keys()):
            response = functions.get_table_info(self, tablename, only_active)
            for except_column in settings.send_allowed_table_rules[tablename]['except_columns']:
                # Перебрать все поля таблицы и удалить из отправки запрещенные
                for record_info in response['info']:
                    record_info.pop(except_column)
        else:
            response = {'status': 'failed',
                        'info': 'У вас нет доступа к просмотру информации с данной таблицы!'}
        response['tablename'] = tablename
        return response

    def get_record_info(self, record_id, tablename='records', *args, **kwargs):
        """ Получить всю информацию по записи """
        command = "SELECT * FROM {} WHERE id={}".format(tablename, record_id)
        response = self.get_table_dict(command)
        if response['status'] == 'success':
            return response['info'][0]

    def get_record_id(self, auto_id):
        """ Вернуть будущий ID этого заезда, перед его совершением """
        if self.check_car_has_gross(auto_id):
            response = functions.get_current_id(self, auto_id)
        else:
            response = functions.get_next_id(self)
        return response
