# -*- coding: utf-8 -*-

from app import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

registrations = db.Table(
    'registrations',
    db.Column('task_id', db.Integer(), db.ForeignKey('tasks.id')),
    db.Column('case_id', db.Integer(), db.ForeignKey('testcases.id'))
)


relycases = db.Table(
    'relycases',
    db.Column('case_id', db.Integer(), db.ForeignKey('testcases.id')),
    db.Column('rely_case_id', db.Integer(), db.ForeignKey('testcases.id')),
)


class Role(db.Model):   # 角色表
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=True, unique=True)     # 角色名称
    default = db.Column(db.Boolean(), default=False)
    permissions = db.Column(db.Integer())   # 权限
    user = db.relationship('User', backref='roles', lazy='dynamic')     # 关联user表

    @staticmethod
    def insert_roles():
        roles = {
            'User': (7, True),
            'Leader': (15, False),
            'Admin': (255, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(db.Model):       # 用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True)    # 用户名，登录，唯一
    password = db.Column(db.String(255))    # 密码
    user_email = db.Column(db.String(64), unique=True)  # 邮箱，唯一
    status = db.Column(db.Boolean(), default=True)  # 状态，False为冻结
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))    # 角色ID，关联role表
    project = db.relationship('Project', backref='users', lazy='dynamic')   # 关联Project表
    model = db.relationship('Model', backref='users', lazy='dynamic')   # 关联Model表
    interface = db.relationship('Interface', backref='users', lazy='dynamic')   # 关联Interface表
    parameter = db.relationship('Parameter', backref='users', lazy='dynamic')   # 关联Parameter表
    test_case = db.relationship('TestCase', backref='users', lazy='dynamic')    # 关联TestCase表
    task = db.relationship('Task', backref='users', lazy='dynamic')     # 关联Task表
    environment = db.relationship('Environment', backref='users', lazy='dynamic')   # 关联Environment表
    test_result = db.relationship('TestResult', backref='users', lazy='dynamic')    # 关联TestResult表
    mock = db.relationship('Mock', backref='users', lazy='dynamic')     # 关联Mock表
    eq_log = db.relationship('EquipmentLog', backref='users', lazy='dynamic')   # 关联Equipment表
    # email = db.relationship('EmailReport', backref='users', lazy='dynamic')

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id


class Project(db.Model):        # 项目表
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(64))     # 项目名称
    project_desc = db.Column(db.String(64), default='')     # 项目描述
    status = db.Column(db.Boolean(), default=True)     # 状态，False为删除
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))      # 创建者ID，关联user表
    model = db.relationship('Model', backref='projects', lazy='dynamic')    # 关联Model表
    Interface = db.relationship('Interface', backref='projects', lazy='dynamic')    # 关联Interface表
    test_case = db.relationship('TestCase', backref='projects', lazy='dynamic')     # 关联TestCase表
    task = db.relationship('Task', backref='projects', lazy='dynamic')  # 关联Task表
    environment = db.relationship('Environment', backref='projects', lazy='dynamic')    # 关联Environment表
    test_result = db.relationship('TestResult', backref='projects', lazy='dynamic')     # 关联TestResult表

    def __repr__(self):
        return self.project_name


class Model(db.Model):      # 模块表
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(64))   # 模块名称
    model_desc = db.Column(db.String(64), default='')   # 模块描述
    status = db.Column(db.Boolean(), default=True)     # 状态，False为删除
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者ID，关联user表
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))  # 项目ID，关联Project表
    Interface = db.relationship('Interface', backref='models', lazy='dynamic')  # 关联Interface表
    test_case = db.relationship('TestCase', backref='models', lazy='dynamic')   # 关联TestCase表

    def __repr__(self):
        return self.model_name


class Environment(db.Model):      # 测试环境表
    __tablename__ = 'environments'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    env_name = db.Column(db.String(64))     # 环境名称
    desc = db.Column(db.String(64), default='')  # 描述信息
    url = db.Column(db.String(255))     # 域名地址
    use_db = db.Column(db.Boolean(), default=False)     # 是否使用数据库
    db_host = db.Column(db.String(255), default='')
    db_port = db.Column(db.String(16), default='')
    db_user = db.Column(db.String(64), default='')
    db_pass = db.Column(db.String(64), default='')
    database = db.Column(db.String(64), default='')     # 数据库名
    status = db.Column(db.Boolean(), default=True)  # 状态，False为删除
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))     # 项目ID，关联Project表
    test_case = db.relationship('TestCase', backref='environments', lazy='dynamic')  # 关联TestCase表
    task = db.relationship('Task', backref='environments', lazy='dynamic')  # 关联Task表
    case_result = db.relationship('CaseResult', backref='environments', lazy='dynamic')     # 关联CaseResult表

    def __repr__(self):
        return str(self.id)


class Interface(db.Model):      # 接口表
    __tablename__ = 'interfaces'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Interface_name = db.Column(db.String(64))   # 接口名称
    Interface_desc = db.Column(db.String(64), default='')   # 接口描述
    interface_type = db.Column(db.String(16), default='http')   # 接口协议类型
    method = db.Column(db.String(16), default='GET')    # 接口请求方式
    path = db.Column(db.String(255))    # 接口路径
    header = db.Column(db.Text())  # 接口header
    params = db.Column(db.String(255), default='')  # 接口参数
    response = db.Column(db.Text())    # 接口返回信息
    status = db.Column(db.Boolean(), default=True)  # 状态，False为删除
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者ID，关联user表
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))  # 项目ID，关联Project表
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'))  # 模块ID，关联Model表
    test_case = db.relationship('TestCase', backref='interfaces', lazy='dynamic')   # 关联TestCase表
    parameter = db.relationship('Parameter', backref='interfaces', lazy='dynamic')  # 关联Parameter表

    def __repr__(self):
        return self.Interface_name


class Parameter(db.Model):      # 参数表
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    param_name = db.Column(db.String(64))   # 参数名字
    param_desc = db.Column(db.Text())       # 参数描述
    param_type = db.Column(db.String(16), default='')   # 参数类型
    necessary = db.Column(db.Boolean(), default=False)  # 是否必须
    default = db.Column(db.String(255), default='')  # 示例，字典格式的字符串
    status = db.Column(db.Boolean(), default=True)  # 状态，False为删除
    c_uid = db.Column(db.Integer, db.ForeignKey('users.id'))    # 创建者ID，关联user表
    interface_id = db.Column(db.Integer, db.ForeignKey("interfaces.id"))  # 接口ID，关联Interface表

    def __repr__(self):
        return str(self.id)


class TestCase(db.Model):      # 测试用例表
    __tablename__ = 'testcases'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    case_name = db.Column(db.String(64))
    case_desc = db.Column(db.String(64), default='')
    case_type = db.Column(db.String(16), default='')
    method = db.Column(db.String(16), default='GET')
    path = db.Column(db.String(255))
    params = db.Column(db.Text())
    header = db.Column(db.Text())
    has_sign = db.Column(db.Integer(), default=0)       # 是否需要aksk签名验证
    ak = db.Column(db.String(64), default='')
    sk = db.Column(db.String(64), default='')
    res_assert = db.Column(db.String(255), default='')
    status = db.Column(db.Boolean(), default=True)
    rely_case = db.relationship(
        'TestCase',
        secondary=relycases,
        primaryjoin=(relycases.c.case_id == id),
        secondaryjoin=(relycases.c.rely_case_id == id),
        backref=db.backref('relycases', lazy='dynamic'),
        lazy='dynamic'
    )
    rely_params = db.Column(db.String(64), default='')
    has_output = db.Column(db.Integer(), default=0)     # 是否输出参数
    output_para = db.Column(db.String(64), default='')  # 出参信息
    has_input = db.Column(db.Integer(), default=0)      # 是否传入参数
    input_para = db.Column(db.String(64), default='')   # 接口参数入参信息
    input_header = db.Column(db.String(64), default='')     # 接口header入参信息
    is_debug = db.Column(db.Boolean(), default=False)   # 是否进行过调试
    is_pass = db.Column(db.Boolean(), default=False)    # 是否跑通
    save_result = db.Column(db.Boolean(), default=False)    # 是否记录用例结果
    use_db = db.Column(db.Boolean(), default=False)     # 是否校验数据库内容
    sql = db.Column(db.Text())      # sql语句
    field_value = db.Column(db.String(255), default='')     # 需校验的数据库字段
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'))
    interface_id = db.Column(db.Integer(), db.ForeignKey('interfaces.id'))
    env_id = db.Column(db.Integer(), db.ForeignKey('environments.id'))
    case_result = db.relationship('CaseResult', backref='testcases', lazy='dynamic')     # 关联CaseResult表

    def __repr__(self):
        return self.case_name


class CaseResult(db.Model):     # 测试用例结果
    __tablename__ = 'caseresults'
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(16), default='')
    method = db.Column(db.String(16), default='GET')
    path = db.Column(db.String(255))        # 接口地址
    params = db.Column(db.Text())           # 接口参数
    input_para = db.Column(db.Text())       # 接口参数入参信息
    header = db.Column(db.Text())           # 接口header
    input_header = db.Column(db.Text())     # 接口header入参信息
    aksk_header = db.Column(db.Text())      # 接口sign验证头信息
    res_assert = db.Column(db.String(255), default='')  # 返回信息的校验值
    result = db.Column(db.Boolean(), default=True)      # 用例执行结果，废弃
    case_result = db.Column(db.Integer(), default=1)    # 用例执行结果，0失败，1通过，2异常
    response = db.Column(db.Text())     # 返回信息
    output_para = db.Column(db.Text())  # 接口返回出参信息
    diff_res = db.Column(db.Text())     # 不同信息
    start_time = db.Column(db.DateTime(), default=datetime.datetime.now)  # 开始时间
    duration = db.Column(db.Integer())  # 运行时长
    case_id = db.Column(db.Integer, db.ForeignKey('testcases.id'), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    environment = db.Column(db.Integer, db.ForeignKey('environments.id'), nullable=True)

    def __repr__(self):
        return str(self.id)


class Task(db.Model):       # 定时任务表
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(64))     # 任务名称
    task_type = db.Column(db.Integer(), default=0)      # 任务类型，0立即执行、1间隔秒数、2日期执行、3crontab执行
    run_time = db.Column(db.String(255), default='')    # 任务执行时间
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)    # 任务的创建时间
    report_to = db.Column(db.String(255), default='')   # 收件人邮箱
    report_copy = db.Column(db.String(255), default='')     # 抄送人邮箱
    task_make_email = db.Column(db.String(255), default='')     # 任务维护者的邮箱
    status = db.Column(db.Boolean(), default=True)      # 状态，False为删除
    run_status = db.Column(db.Integer(), default=0)     # 任务的运行状态，默认是0创建,1启动,2停止
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者
    s_uid = db.Column(db.Integer(), default=0)  # 启动者
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))  # 任务所属的项目
    env_id = db.Column(db.Integer(), db.ForeignKey('environments.id'))
    case_result = db.relationship('CaseResult', backref='tasks', lazy='dynamic')  # 关联CaseResult表
    test_result = db.relationship('TestResult', backref='tasks', lazy='dynamic')  # 关联TestResult表
    interface = db.relationship(
        'TestCase',
        secondary=registrations,
        backref=db.backref('tasks'),
        lazy='dynamic'
    )   # 多对多到测试用例

    def __repr__(self):
        return self.task_name


class TestResult(db.Model):     # 测试结果表
    __tablename__ = 'testresults'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    case_num = db.Column(db.Integer())  # 用例数
    pass_num = db.Column(db.Integer())  # 通过数
    fail_num = db.Column(db.Integer())  # 失败数
    exception_num = db.Column(db.Integer(), default=0)     # 异常数
    not_expect_num = db.Column(db.Integer(), default=0)    # 未达到预期数
    unknown_num = db.Column(db.Integer(), default=0)       # 未知问题数
    start_time = db.Column(db.DateTime(), default=datetime.datetime.now)  # 开始时间
    duration = db.Column(db.Integer())  # 运行时长
    test_report = db.Column(db.String(64), default='')  # 测试报告文件名
    test_log = db.Column(db.String(64), default='')     # 测试日志文件名
    status = db.Column(db.Boolean(), default=True)     # 状态，False为删除
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))
    projects_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id'))

    def __repr__(self):
        return str(self.id)


class CaseStatistics(db.Model):     # case 统计信息记录表
    __tablename__ = 'casestatistics'
    id = db.Column(db.Integer, primary_key=True)
    interface_num = db.Column(db.Integer(), default=0)          # 接口数量
    case_num = db.Column(db.Integer(), default=0)               # 用例数量
    run_case_num = db.Column(db.Integer(), default=0)           # 全部执行用例次数
    success_case_num = db.Column(db.Integer(), default=0)       # 全部通过用例次数
    failure_case_num = db.Column(db.Integer(), default=0)       # 全部失败用例次数
    exception_case_num = db.Column(db.Integer(), default=0)     # 全部异常用例次数
    today_run_case_num = db.Column(db.Integer(), default=0)     # 今日执行用例次数
    today_suc_case_num = db.Column(db.Integer(), default=0)     # 今日通过用例次数
    today_fail_case_num = db.Column(db.Integer(), default=0)    # 今日失败用例次数
    today_exc_case_num = db.Column(db.Integer(), default=0)     # 今日异常用例次数
    open_date = db.Column(db.String(16), default='')            # 产出统计数据的日期 yyyy-mm-dd
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)  # 统计数据创建时间

    def __repr__(self):
        return self.open_date


class Mock(db.Model):     # mock server表
    __tablename__ = 'mocks'
    id = db.Column(db.Integer, primary_key=True)
    mock_name = db.Column(db.String(64))    # mock名字
    mock_desc = db.Column(db.String(64))    # mock描述
    method = db.Column(db.String(16))       # 请求方法
    path = db.Column(db.String(255))        # 请求路径
    params = db.Column(db.Text())           # 请求参数
    header = db.Column(db.Text())           # 请求头
    response = db.Column(db.Text())         # 返回数据
    res_type = db.Column(db.String(16))     # 返回类型
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now)     # 更新时间
    status = db.Column(db.Boolean(), default=True)      # mock状态，False为删除
    run_status = db.Column(db.Integer(), default=0)     # mock运行状态，默认是0停止,1启动
    check_params = db.Column(db.Integer(), default=0)   # 是否校验参数，默认是0不校验,1校验
    check_header = db.Column(db.Integer(), default=0)   # 是否校验header，默认是0不校验,1校验
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'))  # 创建者

    def __repr__(self):
        return self.mock_name


class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), comment='厂商名称')     # 厂商名称
    status = db.Column(db.Integer(), default=1, index=True, comment='厂商状态，0删除，1正常')     # 厂商状态，0删除，1正常
    equip = db.relationship('Equipment', backref='manufacturers', lazy='dynamic')  # 关联Equipment表
    ep_log = db.relationship('EquipmentLog', backref='manufacturers', lazy='dynamic')   # 关联Equipment表

    def __repr__(self):
        return str(self.name)


class Equipment(db.Model):      # 测试设备表
    __tablename__ = 'equipments'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    eq_code = db.Column(db.String(64), index=True, comment='设备编码')  # 设备编码
    eq_name = db.Column(db.String(64), comment='设备名称')  # 设备名称
    eq_desc = db.Column(db.String(64), default='', comment='设备描述')  # 设备描述
    eq_type = db.Column(db.Integer(), default=0, comment='设备类型，0其它，1手机，2pad')  # 设备类型，0其它，1手机，2pad
    eq_sys = db.Column(db.Integer(), default=0, comment='设备系统，0其它，1ios，2android')   # 设备系统，0其它，1ios，2android
    eq_sys_ver = db.Column(db.String(16), default='', comment='设备系统版本')     # 设备系统版本
    eq_owner = db.Column(db.String(16), default='', comment='设备管理者')    # 设备管理者
    borrower = db.Column(db.String(16), default='', comment='借用者姓名')    # 借用者姓名
    have_sim = db.Column(db.Integer(), default=0, comment='是否有sim卡，0没有，1有')  # 是否有sim卡，0没有，1有
    eq_status = db.Column(db.Integer(), default=1, index=True, comment='设备状态，0停用，1可外借，2已外借')    # 设备状态，0停用，1可外借，2已外借
    status = db.Column(db.Integer(), default=1, index=True, comment='设备是否删除，0删除，1正常')   # 设备是否删除，0删除，1正常
    mf_id = db.Column(db.Integer(), db.ForeignKey('manufacturers.id'), comment='设备厂商')  # 设备厂商
    eq_log = db.relationship('EquipmentLog', backref='equipments', lazy='dynamic')   # 关联Equipment表

    def __repr__(self):
        return str(self.id)


class EquipmentLog(db.Model):
    __tablename__ = 'equipment_log'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    eq_code = db.Column(db.String(64), comment='设备编码')  # 设备编码
    eq_name = db.Column(db.String(64), comment='设备名称')  # 设备名称
    eq_desc = db.Column(db.String(64), default='', comment='设备描述')  # 设备描述
    eq_type = db.Column(db.Integer(), default=0, comment='设备类型，0其它，1手机，2pad')   # 设备类型，0其它，1手机，2pad
    eq_sys = db.Column(db.Integer(), default=0, comment='设备系统，0其它，1ios，2android')   # 设备系统，0其它，1ios，2android
    eq_sys_ver = db.Column(db.String(16), default='', comment='设备系统版本')     # 设备系统版本
    eq_owner = db.Column(db.String(16), default='', comment='设备管理者')    # 设备管理者
    borrower = db.Column(db.String(16), default='', comment='借用者姓名')    # 借用者姓名
    have_sim = db.Column(db.Integer(), default=0, comment='是否有sim卡，0没有，1有')  # 是否有sim卡，0没有，1有
    status = db.Column(db.Integer(), comment='设备状态，0停用，1启用，2编辑，3归还，4外借，5删除')    # 设备状态，0停用，1启用，2编辑，3归还，4外借，5删除
    mf_id = db.Column(db.Integer(), db.ForeignKey('manufacturers.id'), comment='设备厂商')  # 设备厂商
    eq_id = db.Column(db.Integer(), db.ForeignKey('equipments.id'), comment='设备ID')      # 设备ID
    c_uid = db.Column(db.Integer(), db.ForeignKey('users.id'), comment='log创建者')        # log创建者

    def __repr__(self):
        return str(self.id)

class ReportDay(db.Model):
    __tablename__ = 'report_day'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer(), nullable=False, comment="产品id")
    module_id = db.Column(db.Integer(), nullable=False, comment="模块id")
    day_date = db.Column(db.String(64), nullable=False, comment="日期")
    total_num = db.Column(db.Integer(), default=0, comment="总数")
    open_num = db.Column(db.Integer(), default=0, comment="开启状态的数量")
    closed_num = db.Column(db.Integer(), default=0, comment="关闭状态的数量")
    resolve_num = db.Column(db.Integer(), default=0, comment="解决的数量")
    crash_num = db.Column(db.Integer(), default=0, comment="崩溃bug数量 severity:1")
    block_num = db.Column(db.Integer(), default=0, comment="阻断bug数量 severity:2")
    serious_num = db.Column(db.Integer(), default=0, comment="严重bug数量 severity:3")
    sort_num = db.Column(db.Integer(), default=0, comment="一般bug数量 severity:4")
    propose_num = db.Column(db.Integer(), default=0, comment="建议bug数量 severity:5")
    risks = db.Column(db.Text(), comment="风险")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_time = db.Column(db.DateTime())


class ReportUser(db.Model):
    __tablename__ = 'report_user'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer(), nullable=False, comment="产品id")
    module_id = db.Column(db.Integer(), nullable=False, comment="模块id")
    day_date = db.Column(db.String(64), comment="日期")
    user_name = db.Column(db.String(64), comment="人员姓名")
    total_num = db.Column(db.Integer(), nullable=False, default=0, comment="名下总数量")
    open_num = db.Column(db.Integer(), default=0, comment="开启状态的数量")
    resolve_num = db.Column(db.Integer(), default=0, comment="解决的数量")
    closed_num = db.Column(db.Integer(), default=0, comment="解决的数量")
    user_type = db.Column(db.Integer(), nullable=False, default=0, comment="用户类型 0创建人 1解决人 2关闭人")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_time = db.Column(db.DateTime())


class ReportProduct(db.Model):
    __tablename__ = 'report_product'
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer(), nullable=False, comment="产品id")
    product_name = db.Column(db.String(128), nullable=False, comment="产品名称")
    product_status = db.Column(db.Integer(), nullable=False, default=0, comment="产品状态 0未提测、1测试中、2测试完成 ")
    module_id = db.Column(db.Integer(), nullable=False, comment="模块id")
    module_name = db.Column(db.String(128), nullable=False,comment="模块名称")
    start_day = db.Column(db.String(128), default='', comment="统计开始日期")
    end_day = db.Column(db.String(128), default='', comment="统计结束日期")
    module_status = db.Column(db.Integer(), nullable=False, default=0, comment="模块状态 0未提测、1测试中、2测试完成 ")
    create_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    update_time = db.Column(db.DateTime())

