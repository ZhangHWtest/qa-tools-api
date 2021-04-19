from .report_bug import get_report
from app.api.report.utils.get_day_list import get_between_day
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import ReportDay, ReportUser, ReportProduct
import datetime


def update_data(product_id, module_id, product_name, module_name, start_day, end_day):

    if start_day == '':
        start_day = "2020-01-01"
    if end_day == '':
        end_day = datetime.datetime.now().strftime("%Y-%m-%d")

    # 调用方法获取 数据
    bugs, rds, rd_resolve, qas, users = get_report(product_id, module_id, start_day, end_day)

    # 判断 产品/模块是否存在
    exist_report_product = ReportProduct.query.filter_by(module_id=module_id).first()
    # report_product
    if not exist_report_product:
        try:
            db.session.add(
                ReportProduct(
                    product_id=product_id,
                    product_name=product_name,
                    module_id=module_id,
                    module_name=module_name,
                    start_day=start_day,
                    end_day=end_day,
                    create_time=datetime.datetime.now(),
                    update_time=datetime.datetime.now()
                )
            )
            db.session.commit()
        except IntegrityError as e:
            # 出错时 回滚数据库
            db.session.rollback()
            return str(e)
    else:
        try:
            update_product = {
                # 'start_day': start_day,
                'end_day': end_day,
                'update_time': datetime.datetime.now()
            }
            ReportProduct.query.filter_by(module_id=module_id).update(
                update_product)
            db.session.commit()
        except IntegrityError as e:
            # 出错时 回滚数据库
            db.session.rollback()
            return str(e)

    # report_day,report_user
    day_list = get_between_day(start_day, end_day)
    for day in day_list:
        # print('day:', day)
        # ReportDay
        exist_report = ReportDay.query.filter_by(module_id=module_id, day_date=day).first()
        if exist_report and bugs.get(day) is not None:
            # 更新
            try:
                update_report_day = {
                    'total_num': bugs.get(day)['bug_total'],
                    'open_num': bugs.get(day)['bug_open'],
                    'closed_num': bugs.get(day)['bug_closed'],
                    'resolve_num': bugs.get(day)['bug_resolve'],
                    'crash_num': bugs.get(day)['bug_crash'],
                    'block_num': bugs.get(day)['bug_block'],
                    'serious_num': bugs.get(day)['bug_serious'],
                    'sort_num': bugs.get(day)['bug_sort'],
                    'propose_num': bugs.get(day)['bug_propose'],
                    'risks': bugs.get(day)['risks'],
                    'update_time': datetime.datetime.now()
                }
                ReportDay.query.filter_by(module_id=module_id, day_date=day).update(
                    update_report_day)
                db.session.commit()
            except IntegrityError as e:
                # 出错时 回滚数据库
                db.session.rollback()
                return str(e)
        elif exist_report is None and bugs.get(day) is not None:
            # 创建
            try:
                db.session.add(
                    ReportDay(
                        product_id=product_id,
                        module_id=module_id,
                        day_date=day,
                        total_num=bugs.get(day)['bug_total'],
                        open_num=bugs.get(day)['bug_open'],
                        closed_num=bugs.get(day)['bug_closed'],
                        resolve_num=bugs.get(day)['bug_resolve'],
                        crash_num=bugs.get(day)['bug_crash'],
                        block_num=bugs.get(day)['bug_block'],
                        serious_num=bugs.get(day)['bug_serious'],
                        sort_num=bugs.get(day)['bug_sort'],
                        propose_num=bugs.get(day)['bug_propose'],
                        risks=bugs.get(day)['risks'],
                        create_time=datetime.datetime.now(),
                        update_time=datetime.datetime.now()
                    )
                )
                db.session.commit()
            except IntegrityError as e:
                # 出错时 回滚数据库
                db.session.rollback()
                return str(e)
        # ReportUser
        # 更新RD
        if rds.get(day) is not None:
            for rd in rds.get(day):
                if users.get(rd) is not None:
                    name = users[rd]
                else:
                    name = rd
                exist_report_rd = ReportUser.query.filter_by(module_id=module_id, day_date=day, user_name=name, user_type=1).first()
                if exist_report_rd is not None:
                    resolve_num = 0
                    if rd_resolve.get(day).get(rd) is not None:
                        resolve_num = rd_resolve.get(day)[rd]
                    try:
                        update_rd_user = {
                            'resolve_num': resolve_num,
                            'total_num': rds.get(day)[rd],
                            'open_num': rds.get(day)[rd] - resolve_num,
                            'update_time': datetime.datetime.now()
                        }
                        ReportUser.query.filter_by(module_id=module_id,user_type=1, day_date=day,user_name=users[rd]).update(
                            update_rd_user)
                        db.session.commit()
                    except IntegrityError as e:
                        # 出错时 回滚数据库
                        db.session.rollback()
                        return str(e)
                else:
                    # print('rd_resolve.get(day)', day, rd_resolve.get(day))
                    resolve_num = 0
                    if rd_resolve.get(day).get(rd) is not None:
                        resolve_num = rd_resolve.get(day)[rd]
                    try:
                        if users.get(rd) is not None:
                            name = users[rd]
                        else:
                            name = rd
                        db.session.add(
                            ReportUser(
                                product_id=product_id,
                                module_id=module_id,
                                day_date=day,
                                user_name=name,
                                user_type=1,
                                total_num=rds.get(day)[rd],
                                resolve_num=resolve_num,
                                open_num=rds.get(day)[rd] - resolve_num,
                                create_time=datetime.datetime.now(),
                                update_time=datetime.datetime.now()
                            )
                        )
                        db.session.commit()
                    except IntegrityError as e:
                        # 出错时 回滚数据库
                        db.session.rollback()
                        return str(e)
        # 跟新qa
        if qas.get(day) is not None:
            for qa in qas.get(day):
                exist_report_qa = ReportUser.query.filter_by(module_id=module_id, day_date=day, user_name=users[qa],
                                                             user_type=0).first()
                if exist_report_qa is not None:
                    try:
                        update_qa_user = {
                            'open_num': qas.get(day)[qa],
                            'update_time': datetime.datetime.now()
                        }
                        ReportUser.query.filter_by(module_id=module_id, day_date=day, user_type=0, user_name=users[qa]).update(
                            update_qa_user)
                        db.session.commit()
                    except IntegrityError as e:
                        # 出错时 回滚数据库
                        db.session.rollback()
                        return str(e)
                else:
                    try:
                        db.session.add(
                            ReportUser(
                                product_id=product_id,
                                module_id=module_id,
                                day_date=day,
                                user_name=users[qa],
                                user_type=0,
                                open_num=qas.get(day)[qa],
                                create_time=datetime.datetime.now(),
                                update_time=datetime.datetime.now()
                            )
                        )
                        db.session.commit()
                    except IntegrityError as e:
                        # 出错时 回滚数据库
                        db.session.rollback()
                        return str(e)


if __name__ == '__main__':
    # get_between_day('2021-01-01')
    update_data(120, 1403, '抱石云/SaaS产品', '教学系统后台','2020-12-01')
