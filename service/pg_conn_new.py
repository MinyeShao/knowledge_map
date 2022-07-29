# --coding:utf-8--
import time
import uuid

from psycopg_pool import ConnectionPool
import psycopg
from common.logger_tool.ttalk_loggers import format_logger
from untils.nebula_tool import nebula
import re
from concurrent.futures import ProcessPoolExecutor


def print_run_time(func):
    def wrapper(*args, **kwargs):
        local_time = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} run time is {time.time() - local_time}s")
        return result

    return wrapper


company_all_num = 0


def sub_str(params: str):
    params = re.sub(r"\\", "/", params)
    params = re.sub(r"\n", "", params)
    params = re.sub(r"\t", "", params)
    response = re.sub(r"\"", "", params)

    return response
    # return params


def step_to_write(entity_params, _ngql):
    if len(entity_params) != 0:
        # error_code, error_msg = None, None
        if len(entity_params) > 100000:
            if not isinstance(entity_params, list):
                entity_params = list(entity_params)
            batch_ = len(entity_params) // 100000
            for ind_ in range(batch_ + 1):
                error_code, error_msg = nebula.insert_entity(entity_params[ind_ * 100000: (ind_ + 1) * 100000], _ngql)
                if error_code != 0:
                    return error_code, error_msg
        else:
            error_code, error_msg = nebula.insert_entity(entity_params, _ngql)

        # return error_code, error_msg




def get_invest_company(invest_company_sql):
    company_vs = set()
    person_vs = set()
    person_to_company = {}  # "12"->"13":("n1", 1), "13"->"14":("n2", 2)
    company_to_invest = []
    invest_vs = []

    invest_company_result = cur.execute(invest_company_sql)

    # 公司节点添加
    for line in invest_company_result:
        company_name = sub_str(str(line[1]))  # 特殊符号处理
        address = sub_str(str(line[3]))
        legal_person_name = sub_str(str(line[6]))
        company_type = sub_str(str(line[7]))
        reg_status = sub_str(str(line[8]))
        reg_org = sub_str(str(line[9]))
        history_name = sub_str(str(line[14]))
        invest_name = sub_str(str(line[16]))

        company_vs.add(f'"{line[0]}":("{line[0]}","{company_name}", "{line[2]}", "{address}", "{line[4]}",'
                       f'"{line[5]}", "{legal_person_name}", "{company_type}", "{reg_status}", "{reg_org}",'
                       f'"{line[10]}", "{line[11]}", "{line[12]}", "{line[13]}", "{history_name}")')

        if legal_person_name != 'None':
            # company_id_legal_person_name
            person_id = str(line[-1]) + "_" + legal_person_name[:5]

            person_vs.add(f'"{person_id}":("{person_id}","{legal_person_name}")')
            # person_to_company.append(f'"{person_id}"->"{line[0]}":("法定代表人")')
            key = str(f'"{person_id}"->"{line[0]}":')
            if person_to_company.get(key, None) is None:
                person_to_company[key] = {"法定代表人"}

        if line[15] is not None:
            invest_vs.append(f'"{line[15]}":("{line[15]}", "{invest_name}")')
            company_to_invest.append(
                f'"{line[0]}"->"{line[15]}":("{line[17]}", "{line[18]}", "{line[19]}", "{line[20]}")')

    return company_vs, person_vs, person_to_company, invest_vs, company_to_invest


def get_company_executives(company_executives_sql, person_to_company):
    executives_vs = set()
    executives_to_company = person_to_company
    company_executives_result = cur.execute(company_executives_sql)

    for line in company_executives_result:
        person_name = sub_str(str(line[1]))
        position = sub_str(str(line[2]))
        if person_name is not None:
            # company_id_legal_person_name
            person_id_e = str(line[3]) + "_" + person_name[:5]
            executives_vs.add(f'"{person_id_e}":("{person_id_e}","{person_name}")')
            # executives_to_company.append(f'"{person_id_e}"->"{line[0]}":("{position}")')
            key = str(f'"{person_id_e}"->"{line[0]}":')
            # if key not in executives_to_company.keys():
            if executives_to_company.get(key, None) is None:
                executives_to_company[key] = {position}
            else:
                executives_to_company[key].add(position)

    executives_to_company_list = []
    for key, value in executives_to_company.items():
        val = ",".join(value)
        line = key + f'("{val}")'
        executives_to_company_list.append(line)

    return executives_vs, executives_to_company_list


def get_company_branch(company_branch_sql):
    branch_vs = []
    company_to_branch = []

    company_branch_result = cur.execute(company_branch_sql)
    # 分支机构添加
    for line in company_branch_result:
        branch_name = sub_str(str(line[2]))
        if line[1] is not None:
            branch_vs.append(f'"{line[1]}":("{line[1]}","{branch_name}")')
            company_to_branch.append(f'"{line[0]}"->"{line[1]}":("{line[3]}")')
    return branch_vs, company_to_branch


def get_company_gudong(company_gudong_sql):
    gudong_com_vs = []
    gudong_to_company = set()
    gudong_per_vs = set()

    company_gudong_result = cur.execute(company_gudong_sql)

    # 股东信息添加
    for line in company_gudong_result:
        shareholder = sub_str(str(line[2]))
        if line[1] is not None and line[3] == '企业法人':  # 当股东是企业法人时
            gudong_com_vs.append(f'"{line[1]}":("{line[1]}","{shareholder}")')
            gudong_to_company.add(
                f'"{line[1]}"->"{line[0]}":("{line[3]}", "{line[4]}", "{line[5]}")')

        elif line[3] == '自然人股东':
            # company_id_legal_person_name
            person_id_g = str(line[6]) + "_" + shareholder[:5]
            gudong_per_vs.add(f'"{person_id_g}":("{person_id_g}","{shareholder}")')
            gudong_to_company.add(
                f'"{person_id_g}"->"{line[0]}":("{line[3]}", "{line[4]}", "{line[5]}")')

    return gudong_com_vs, gudong_to_company, gudong_per_vs


if __name__ == '__main__':
    conninfo = "postgresql:///postgres?host=172.31.255.36&port=5432&user=postgres&password=zd123@@"
    pool = ConnectionPool(conninfo, max_size=20)
    # 查询td_zxk_company_base_info公司基本信息表
    i = 0
    while True:
        with pool.connection() as cur:
            start_count = i * 10000
            end_count = 10000 * (i + 1)
            # -----------------------------------------------------
            person_ngql = f'INSERT VERTEX IF NOT EXISTS person (id, name) VALUES '

            invest_ngql = f'INSERT VERTEX IF NOT EXISTS company (hid, company_name) VALUES  '
            investment_company_invest = "INSERT EDGE IF NOT EXISTS " \
                                        "investment(should_capi,stock_percentage,invest_start_date,invest_status) VALUES "
            executive_person_company = 'INSERT EDGE IF NOT EXISTS executive(position) VALUES '
            branch_company_branch = 'INSERT EDGE IF NOT EXISTS branch(branch_status) VALUES '
            shareholder_gudong_company = 'INSERT EDGE IF NOT EXISTS shareholder(shareholder_type , ratio , capital) VALUES '
            company_ngql = f'INSERT VERTEX company(hid, company_name, scc, address, amount, org_num, legal_person_name,' \
                           f'company_type, reg_status, reg_org, op_from, op_to, industy_code, subindusty_code, ' \
                           f'history_name) VALUES  '

            t1 = time.time()
            # sql#1 -------------------------------------------------------------

            invest_company_sql = f"""select
                                c.hid as hid,
                                c.company_name as company_name,
                                c.scc as scc,
                                c.address as address,
                                c.amount as amount,
                                c.org_num as org_num,
                                c.legal_person_name as legal_person_name,
                                c.company_type as company_type,
                                c.reg_status as reg_statusa,
                                c.reg_org as reg_org,
                                c.op_from as op_form,
                                c.op_to as op_to,
                                c.industy_code as industy_code,
                                c.subindusty_code as subindusty_code,
                                c.history_name as history_name,
                                it.invest_name_id as invest_name_id,
                                it.invest_name as invest_name,
                                it.should_capi as should_capi,
                                it.stock_percentage as stock_percentage,
                                it.invest_start_date as invest_start_date,
                                it.invest_status as invest_status,
                                c.id as id
                            from
                                td_zxk_company_base_info
                                as c left join td_zxk_investment_info as it on c.hid = it.hid
                            where
                                c.id > {start_count} and c.id <= {end_count}"""

            company_vs, person_vs, person_to_company, invest_vs, company_to_invest = get_invest_company(
                invest_company_sql)
            if len(company_vs) == 0:
                break

            # sql#2--------------------------------------------
            company_executives_sql = f"""select cb.hid as hid,
                                ex.person_name as person_name,
                                ex.position as position,
                                cb.id as id
                            from
                                td_zxk_company_base_info as cb
                            right join td_zxk_companyexecutives_info as ex
                            on cb.hid = ex.hid
                            where cb.id > {start_count} and cb.id <= {end_count}"""  # 检查sql的输出和下面的line[x] 是否对应

            executives_vs, executives_to_company_list = get_company_executives(company_executives_sql,
                                                                               person_to_company)

            # 人名点和边的合并

            # sql#3--------------------------------------------
            company_branch_sql = f"""select c.hid as hid,
                        bc.branch_name_id as branch_name_id,
                        bc.branch_name as branch_name,
                        bc.branch_status as branch_status
                        
                    from
                        td_zxk_company_base_info
                        as c
                        right join td_zxk_branch_info as bc on c.hid = bc.hid
                    where
                        c.id > {start_count}
                        and c.id <= {end_count}"""

            branch_vs, company_to_branch = get_company_branch(company_branch_sql)

            # sql#4--------------------------------------------
            company_gudong_sql = f"""select c.hid as hid,
                                gu.shareholder_id as shareholder_id,
                                gu.shareholder as shareholder,
                                gu.shareholder_type as shareholder_type,
                                gu.ratio as ratio,
                                gu.capital as capital,
                                c.id as id
                            from
                                td_zxk_company_base_info
                                as c
                                right join td_zxk_companygudong_info as gu on c.hid = gu.hid
                            where
                                c.id > {start_count}
                                and c.id <= {end_count}"""

            gudong_com_vs, gudong_to_company, gudong_per_vs = get_company_gudong(company_gudong_sql)

            # 开始插入图谱--------------------------------------------------------------
            t2 = time.time()
            try:

                with ProcessPoolExecutor(max_workers=5) as threadPool:
                    task_1 = threadPool.submit(step_to_write, *(company_vs, company_ngql))
                    invest_vs.extend(gudong_com_vs)
                    invest_vs.extend(branch_vs)
                    task_3 = threadPool.submit(step_to_write, *(invest_vs, invest_ngql))
                    # task_9 = threadPool.submit(step_to_write, *(gudong_com_vs, invest_ngql))
                    # task_7 = threadPool.submit(step_to_write, *(branch_vs, invest_ngql))
                    threadPool.shutdown(wait=True)
            # ----------------------------------------------------------------------------
                with ProcessPoolExecutor(max_workers=10) as threadPool:
                    person_vs = person_vs.union(executives_vs).union(gudong_per_vs)
                    task_2 = threadPool.submit(step_to_write, *(person_vs, person_ngql))

                    # task_5 = threadPool.submit(step_to_write, *(executives_vs, person_ngql))
                    #
                    # task_10 = threadPool.submit(step_to_write, *(gudong_per_vs, person_ngql))

                    task_4 = threadPool.submit(step_to_write, *(company_to_invest, investment_company_invest))

                    task_6 = threadPool.submit(step_to_write, *(executives_to_company_list, executive_person_company))

                    task_8 = threadPool.submit(step_to_write, *(company_to_branch, branch_company_branch))

                    task_11 = threadPool.submit(step_to_write, *(gudong_to_company, shareholder_gudong_company))

                    threadPool.shutdown(wait=True)
                # ---------------------------------------------------------------------------------

                t3 = time.time()
                format_logger.info(
                    f"图谱插入:{i}/ sql time:{t2 - t1} s, nebula time:{t3 - t2} s, batch:{t3 - t1} s")
            except Exception as e:
                print("error")
            # 插入图谱完成-------------------------------------------------------

            i += 1
    print("插入图谱完成")
