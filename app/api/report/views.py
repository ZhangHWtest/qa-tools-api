from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_login import login_required
from app.models import ReportDay, ReportUser, ReportProduct
from app import db
from common.response import ResMsg
from sqlalchemy import func
from app.api.report.utils.update_data import update_data
import math
import datetime


report = Blueprint('report', __name__)


class GetReportList(MethodView):
    @login_required
    def post(self):
        # 返回
        res = ResMsg()
        report_list = list()
        # 获取请求数据
        data = request.get_json()
        product_id = data.get("product_id")
        module_id = data.get("module_id")
        product_name = data.get("product_name")
        module_name = data.get("module_name")
        start_day = data.get("start_day")
        end_day = data.get("end_day")
        page_num = data.get('page_num')
        page_size = data.get('page_size', 10)


        # 调用方法，创建/跟新数据
        if product_id != '' and end_day != '':
            new_end_day = datetime.datetime.now().strftime("%Y-%m-%d")
            update_data(product_id, module_id, product_name, module_name, start_day, new_end_day)

        try:
            if product_id == '' and module_id == '' and start_day == '' and end_day == '':
                report_product_list = ReportProduct.query.filter() \
                    .order_by(ReportProduct.id.desc()).limit(page_size) \
                    .offset((page_num - 1) * page_size) \
                    .all()
            elif start_day != '' or end_day != '':
                report_product_list = ReportProduct.query.filter(ReportProduct.start_day >= start_day,
                                                                 ReportProduct.start_day <= end_day) \
                    .order_by(ReportProduct.id.desc()).limit(page_size) \
                    .offset((page_num - 1) * page_size) \
                    .all()
            else:
                report_product_list = ReportProduct.query.filter(ReportProduct.product_id == product_id,
                                                                 ReportProduct.module_id == module_id,
                                                                 ReportProduct.start_day >= start_day,
                                                                 ReportProduct.start_day <= end_day) \
                    .order_by(ReportProduct.id.desc()).limit(page_size) \
                    .offset((page_num - 1) * page_size) \
                    .all()

            total = db.session.query(func.count(ReportProduct.id)).scalar()
            for product in report_product_list:
                report_info = {
                    'id': product.id,
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'module_id': product.module_id,
                    'module_name': product.module_name,
                    'start_day': product.start_day,
                    'end_day': product.end_day
                    }
                report_list.append(report_info)
            res.update(code=1, data=report_list, msg='获取成功！')
            res.add_field(name='page_num', value=page_num)
            res.add_field(name='page_size', value=page_size)
            res.add_field(name='total', value=total)
            return jsonify(res.data)
        except Exception as e:
            res.update(code=-1, data='', msg='获取失败！')
            return jsonify(res.data)


class GetReportInfo(MethodView):
    @login_required
    def post(self):
        # 返回
        res = ResMsg()
        # 获取请求数据
        data = request.get_json()
        product_id = data.get('product_id')
        module_id = data.get('module_id')
        start_day = data.get('start_day')
        end_day = data.get('end_day')
        # 数据库操作
        try:
            report_day = ReportDay.query.filter(
                ReportDay.product_id == product_id,
                ReportDay.module_id == module_id,
                ReportDay.day_date.between(start_day, end_day)).all()
            report_product = ReportProduct.query.filter_by(product_id=product_id, module_id=module_id).first()
            total, open, closed, resolve, crash, block, serious, sort, propose = 0, 0, 0, 0, 0, 0, 0, 0, 0
            #new
            rd_user_info = {}
            qa_user_info = {}

            for re_day in report_day:
                total += re_day.total_num
                open += re_day.open_num
                closed += re_day.closed_num
                resolve += re_day.resolve_num
                crash += re_day.crash_num
                block += re_day.block_num
                serious += re_day.serious_num
                sort += re_day.sort_num
                propose += re_day.propose_num

                # 根据ReportProduct 中的天去取user里数据
                report_user = ReportUser.query.filter_by(product_id=product_id, module_id=module_id, day_date=re_day.day_date).order_by(ReportUser.total_num.desc())

                # 组装数据
                for i in report_user:
                    if i.user_type == 1:
                        if rd_user_info.get(i.user_name) is None:
                            rd_user_info[i.user_name] = {
                                'total': i.total_num,
                                'resolve': i.resolve_num,
                                'open': i.open_num,
                            }
                        else:
                            rd_user_info.get(i.user_name)['total'] = rd_user_info.get(i.user_name).get(
                                'total') + i.total_num
                            rd_user_info.get(i.user_name)['resolve'] = rd_user_info.get(i.user_name).get(
                                'resolve') + i.resolve_num
                            rd_user_info.get(i.user_name)['open'] = rd_user_info.get(i.user_name).get(
                                'open') + i.open_num

                    elif i.user_type == 0:
                        if qa_user_info.get(i.user_name) is None:
                            qa_user_info[i.user_name] = {
                                'open':i.open_num
                            }
                        else:
                            qa_user_info[i.user_name]['open'] = qa_user_info.get(i.user_name).get(
                                'open') + i.open_num

            # print('rd_user_info:', rd_user_info)
            # print('qa_user_info:', qa_user_info)

            # 项目基本信息
            report_info = {
                'product_name': report_product.product_name,
                'module_name': report_product.module_name,
                'total': total,
                'open': open,
                'closed': closed,
                'resolve': resolve,
                'crash': crash,
                'block': block,
                'serious': serious,
                'sort': sort,
                'propose': propose,
                'start_day': report_product.start_day,
                'end_day': report_product.end_day,
                'risks': report_day[-1].risks
            }

            # rd
            rd_user_list = []
            rd_total_list = []
            rd_resolve_list = []
            rd_open_list = []
            rd_rate_list = []
            # qa
            qa_user_list = []
            qa_total_list = []

            # 排序
            new_rd_user_list = ((key, value) for key, value in rd_user_info.items())
            rd_user_sort_list = sorted(new_rd_user_list, key=lambda x: x[1]["total"], reverse=True)
            # for i in rd_user_sort_list:
            #     print(i[0])
            #     print(i[1].get('total'))
            # print('sort:', rd_user_sort_list)
            for i in rd_user_sort_list:
                rd_user_list.append(i[0])
                rd_total_list.append(i[1].get('total'))
                rd_resolve_list.append(i[1].get('resolve'))
                rd_open_list.append(i[1].get('open'))
                rd_rate_list.append(math.ceil(i[1].get('total')/report_info.get('total')*100))

            for i in qa_user_info:
                qa_user_list.append(i)
                qa_total_list.append(qa_user_info.get(i)['open'])

            report_info['qa_user_list'] = qa_user_list
            report_info['qa_total_list'] = qa_total_list
            report_info['rd_user_list'] = rd_user_list
            report_info['rd_total_list'] = rd_total_list
            report_info['rd_resolve_list'] = rd_resolve_list
            report_info['rd_open_list'] = rd_open_list
            report_info['rd_rate_list'] = rd_rate_list

            res.update(code=1, data=report_info, msg='获取成功！')
            return jsonify(res.data)
        except Exception as e:
            res.update(code=-1, data='', msg='获取失败！'+str(e))
            return jsonify(res.data)


class UpdateReport(MethodView):
    @login_required
    def post(self):
        # 返回
        res = ResMsg()
        # 获取请求数据
        data = request.get_json()
        product_id = data.get("product_id")
        module_id = data.get("module_id")
        product_name = data.get("product_name")
        module_name = data.get("module_name")
        start_day = data.get("start_day")
        end_day = data.get("end_day")
        if end_day == '':
            end_day = datetime.datetime.now().strftime("%Y-%m-%d")
        update_return = update_data(product_id, module_id, product_name, module_name, start_day, end_day)
        if update_return is None:
            res.update(code=1, data='', msg='创建/更新成功！')
            return jsonify(res.data)
        else:
            res.update(code=-1, data='', msg=str(update_return))
            return jsonify(res.data)


class GetProductList(MethodView):
    @login_required
    def get(self):
        # 返回
        res = ResMsg()
        product_list = []
        # 要返回的形式 [product_list:[{id:1,name:1}]]
        try:
            report_product_list = ReportProduct.query.filter().order_by(ReportProduct.id.desc()).all()
            product_info = {}
            for pi in report_product_list:
                module_list = []
                if product_info.get('id') is None:

                    module_info = {
                            'id': pi.module_id,
                            'name': pi.module_name,
                        }
                    module_list.append(module_info)
                    product_info = {
                        'id': pi.product_id,
                        'name': pi.product_name,
                        'module_list': module_list
                    }
                try:
                    report_product_list = ReportProduct.query.filter(ReportProduct.product_id == pi.product_id).order_by(ReportProduct.id.desc()).all()
                    for i in report_product_list:
                        if i.module_id != pi.module_id:
                            module_info = {
                                'id': i.module_id,
                                'name': i.module_name
                            }
                            module_list.append(module_info)

                except Exception as e:
                    res.update(code=-1, data='', msg='获取失败！' + str(e))
                    return jsonify(res.data)

            product_list.append(product_info)
            res.update(code=1, data=product_list, msg='sucess！')
            return jsonify(res.data)
        except Exception as e:
            res.update(code=-1, data='', msg='获取失败！' + str(e))
            return jsonify(res.data)


class DelReport(MethodView):
    @login_required
    def post(self):
        # 返回
        res = ResMsg()
        # 获取请求数据
        data = request.get_json()
        product_id = data.get("product_id")
        module_id = data.get("module_id")
        report_product = ReportProduct.query.filter_by(product_id=product_id, module_id=module_id).first()
        if report_product:
            try:
                ReportProduct.query.filter_by(product_id=product_id, module_id=module_id).delete()
                ReportUser.query.filter_by(product_id=product_id, module_id=module_id).delete()
                ReportDay.query.filter_by(product_id=product_id, module_id=module_id).delete()
                db.session.commit()
                res.update(code=1, data='', msg='删除成功！')
                return jsonify(res.data)
            except Exception as e:
                db.session.rollback()
                res.update(code=-1, data='', msg='删除失败！' + str(e))
                return jsonify(res.data)
        else:
            res.update(code=1, data='', msg='删除失败，请检查信息！')
            return jsonify(res.data)


