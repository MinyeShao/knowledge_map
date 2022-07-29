# -*- coding: utf-8 -*-
import sys
import time

sys.path.append("/data/knowledge_map")
from psycopg_pool import ConnectionPool
from common.logger_tool.ttalk_loggers import format_logger
from untils.nebula_tool import nebula
from multiprocessing import Pool as Process_Pool

from tqdm import tqdm
person_ngql1 = f'DELETE VERTEX '
person_ngql2 = f' WITH EDGE;'
person_ngql = f'INSERT VERTEX person (id, name) VALUES '
executive_person_company = 'INSERT EDGE executive(position) VALUES '
shareholder_gudong_company = 'INSERT EDGE shareholder(shareholder_type , ratio , capital) VALUES '


def name_disting(hid: str, del_vertex_person, person_vertex, executives_to_company, gudong_to_company):
    results = nebula.go_company_relationship(hid)
    dict_person = {}
    for r in results:
        list_line = []
        for z in r:
            z = str(z).strip("\"")
            list_line.append(z)
        if list_line[10] != '__EMPTY__':
            name = list_line[10]
            if name not in dict_person:
                dict_person[name] = {}
            if list_line[8] != '__EMPTY__':  # 为高管信息
                if int(list_line[8]) > 0:
                    hid = list_line[7]
                    person_id = list_line[6]
                else:
                    hid = list_line[6]
                    person_id = list_line[7]
                position = list_line[9]
                if person_id not in dict_person[name]:
                    dict_person[name][person_id] = [[hid, "executive", position]]
                else:
                    if [hid, "executive", position] not in dict_person[name][person_id]:
                        dict_person[name][person_id].append([hid, "executive", position])
            if list_line[2] != '__EMPTY__':  # 为股东信息
                if int(list_line[2]) > 0:
                    person_id = list_line[0]
                    hid = list_line[1]
                else:
                    hid = list_line[1]
                    person_id = list_line[0]
                edge_property = [list_line[3], list_line[4], list_line[5]]  # [shareholder_type, ratio, capital]
                if person_id not in dict_person[name]:
                    dict_person[name][person_id] = [[hid, "shareholder", edge_property]]
                else:
                    if [hid, "shareholder", edge_property] not in dict_person[name][person_id]:
                        dict_person[name][person_id].append([hid, "shareholder", edge_property])
            # print(list_line)
        elif list_line[11] != '__EMPTY__':
            name = list_line[11]
            if name not in dict_person:
                dict_person[name] = {}
            if list_line[8] != '__EMPTY__':  # 为高管信息
                if int(list_line[8]) > 0:
                    hid = list_line[7]
                    person_id = list_line[6]
                else:
                    hid = list_line[6]
                    person_id = list_line[7]
                position = list_line[9]
                if person_id not in dict_person[name]:
                    dict_person[name][person_id] = [[hid, "executive", position]]
                else:
                    if [hid, "executive", position] not in dict_person[name][person_id]:
                        dict_person[name][person_id].append([hid, "executive", position])
            if list_line[2] != '__EMPTY__':  # 为股东信息
                if int(list_line[2]) > 0:
                    hid = list_line[1]
                    person_id = list_line[0]
                else:
                    hid = list_line[0]
                    person_id = list_line[1]
                edge_property = [list_line[3], list_line[4], list_line[5]]  # [shareholder_type, ratio, capital]
                if person_id not in dict_person[name]:
                    dict_person[name][person_id] = [[hid, "shareholder", edge_property]]
                else:
                    if [hid, "shareholder", edge_property] not in dict_person[name][person_id]:
                        dict_person[name][person_id].append([hid, "shareholder", edge_property])

    # ----------------------------------------------------------------------------------------
    for name, values in dict_person.items():
        dicts = {}
        if len(values) == 1:
            continue
        else:
            # 合并节点
            for id, edges in values.items():  # {'"111745_孙宏洁"': [['"0909943728205566931"', 'executive', '"总经理"']], '"279709_孙宏洁"': [['"2070737668114566931"', 'executive', '"总经理"']]}
                for edge in edges:
                    if edge[1] not in dicts:
                        dicts[edge[1]] = {}
                    if edge[0] not in dicts[edge[1]]:
                        dicts[edge[1]][edge[0]] = []
                    if edge[1] == "executive":
                        post = edge[2].split(",")
                        for p in post:
                            if p not in dicts[edge[1]][edge[0]]:
                                dicts[edge[1]][edge[0]].append(p)
                    elif edge[1] == "shareholder":
                        if edge[2] not in dicts[edge[1]][edge[0]]:
                            dicts[edge[1]][edge[0]].append(edge[
                                                               2])  # dicts: {'executive': {'0909943728205566931': ['总经理'], '7014137805807355541': ['法定代表人']}}
                # nebula.del_vertex(id)
                del_vertex_person.append(f'"{id}"')

            personid = del_vertex_person[-1].strip("\"")
        # nebula.insert_person(personid, name)
        person_vertex.append(f'"{personid}":("{personid}","{name}")')
        for exec, values in dicts.items():  # {'executive': {'"0909943728205566931"': ['"总经理"'], '"2070737668114566931"': ['"总经理"']}}
            for hid, postion in values.items():
                if exec == "executive":
                    # nebula.insert_edge(personid, exec, hid, ",".join(postion))
                    executives_to_company.append(f'"{personid}"->"{hid}":("{",".join(postion)}")')
                elif exec == "shareholder":
                    # nebula.insert_edge(personid, exec, hid, postion[0])
                    gudong_to_company.append(
                        f'"{personid}"->"{hid}":("{postion[0][0]}", "{postion[0][1]}", "{postion[0][2]}")')


def remove_person(result, i):
    t1 = time.time()
    error_msg = None
    del_vertex_person = []
    person_vertex = []
    executives_to_company = []
    gudong_to_company = []
    for line in result:
        name_disting(line[0], del_vertex_person, person_vertex, executives_to_company, gudong_to_company)
    t2 = time.time()
    # 删除同名人
    if len(del_vertex_person) == 0:
        format_logger.info(f"step:{i}/del_vertex_person=0")

        return False
    try:
        if len(del_vertex_person) != 0:
            error_code, error_msg = nebula.del_entity(del_vertex_person, person_ngql1, person_ngql2)
            assert error_code == 0
        # 添加同命人和边
        if len(person_vertex) != 0:
            error_code, error_msg = nebula.insert_entity(person_vertex, person_ngql)
            assert error_code == 0
        if len(executives_to_company) != 0:
            error_code, error_msg = nebula.insert_entity(executives_to_company, executive_person_company)
            assert error_code == 0
        if len(gudong_to_company) != 0:
            error_code, error_msg = nebula.insert_entity(gudong_to_company, shareholder_gudong_company)
            assert error_code == 0
        t3 = time.time()
        format_logger.info(f"step:{i}/go time:{t2 - t1}s, nebula time:{t3 - t2} s , batch time:{t3 - t1} s ")
    except Exception as e:
        format_logger.error(
            f"图谱消歧:{i}/ batch: {error_msg} , Exception: {e}")


if __name__ == '__main__':
    conninfo = "postgresql:///postgres?host=121.46.196.82&port=5432&user=postgres&password=zd123@@"
    pool = ConnectionPool(conninfo, max_size=20)
      # 创建20个进程
    process_Pool = None
    t4 = time.time()
    with pool.connection() as cur:
        j = 0
        for i in tqdm(range(0, 500000)):
            if j % 60 == 0:
                if process_Pool is not None:
                    process_Pool.close()
                    process_Pool.join()
                process_Pool = Process_Pool(30)
            start_count = i * 100
            end_count = 100 * (i + 1)

            # ------------------------------------------------------------------------------------------------
            t1 = time.time()
            sql = f"""SELECT hid FROM td_zxk_company_base_info WHERE id >{start_count} and id <={end_count}"""
            result = cur.execute(sql)
            result = list(result)
            t2 = time.time()

            if len(result) > 0:
                process_Pool.apply_async(remove_person, args=(result, i))
            j += 1
        # ---------------------------------------------------


        t5 = time.time()
        format_logger.info(f'任务完成,总时间:{t5 - t4} s')
