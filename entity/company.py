class InvestmentCompany():
    def __init__(self, invest_name, invest_oper_name, invest_regist_capi, should_capi, stock_percentage):
        # 投资公司id 唯一标志
        self.id = id
        # 投资企业名称
        self.invest_name = invest_name
        # 被投资公司的法人代表
        self.invest_oper_name = invest_oper_name
        # 被投资企业注册资本
        self.invest_regist_capi = invest_regist_capi
        # 投资企业投资金额
        self.should_capi = should_capi
        # 投资企业投资比例
        self.stock_percentage = stock_percentage

    def getId(self):
        return self.id

    def getInvestName(self):
        return self.invest_name

    def getInvestOperName(self):
        return self.invest_oper_name

    def getInvestRegistCapi(self):
        return self.invest_regist_capi

    def getStockPercentage(self):
        return self.stock_percentage

    def setInvestName(self, invest_name):
        self.invest_name = invest_name

    def setInvestOperName(self, invest_oper_name):
        self.invest_oper_name = invest_oper_name

    def setInvestRegistCapi(self, invest_regist_capi):
        self.invest_regist_capi = invest_regist_capi

    def setStockPercentage(self, stock_percentage):
        self.stock_percentage = stock_percentage


class BranchCompany():
    # 待定
    pass


class Company(InvestmentCompany, BranchCompany):

    def __init__(self, id, company_name, scc, license_number, address, province, city, district, currency, money_unit,
                 amount, tax_payer_num, org_num, legal_person_name, company_type, reg_status, establish_time,
                 check_date, reg_org, op_from, op_to, business_scope, reg_address, reg_capital, industy, industy_code,
                 subindusty, subindusty_code, history_name):
        # 投资公司id 唯一标志
        self.id = id
        # 公司名称
        self.company_name = company_name
        # 公司统一信用号码
        self.scc = scc
        # 工商注册号
        self.license_number = license_number
        # 公司地址
        self.address = address
        # 省份
        self.province = province
        # 城市
        self.city = city
        # 区镇
        self.district = district
        # 币种
        self.currency = currency
        # 货币单位（万元）
        self.money_unit = money_unit
        # 注册资本
        self.amount = amount
        # 纳税人识别号
        self.tax_payer_num = tax_payer_num
        # 组织机构代码
        self.org_num = org_num
        # 法人名称
        self.legal_person_name = legal_person_name
        # 公司类型
        self.company_type = company_type
        # 公司注册状态
        self.reg_status = reg_status
        # 公司创建日期 (yyyy-mm-dd)
        self.establish_time = establish_time
        # 核准日期(yyyy-mm-dd)
        self.check_date = check_date
        # 登记机关
        self.reg_org = reg_org
        # 经营日期自
        self.op_from = op_from
        # 经营日期至
        self.op_to = op_to
        # 业务经营范围
        self.business_scope = business_scope
        # 注册地址
        self.reg_address = reg_address
        # 注册资本
        self.reg_capital = reg_capital
        # 公司所属行业
        self.industy = industy
        # 行业编号
        self.industy_code = industy_code
        # 子行业
        self.subindusty = subindusty
        # 子行业编号
        self.subindusty_code = subindusty_code
        # 曾用名
        self.history_name = history_name
