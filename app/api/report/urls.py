from .views import *
from .views import report

report.add_url_rule('/report/list', view_func=GetReportList.as_view('report_list'))
report.add_url_rule('/report/info', view_func=GetReportInfo.as_view('report_info'))
# report.add_url_rule('/report/add', view_func=AddReport.as_view('add_report'))
report.add_url_rule('/report/update', view_func=UpdateReport.as_view('update_report'))
report.add_url_rule('/report/product/list', view_func=GetProductList.as_view('report_product_list'))
report.add_url_rule('/report/del', view_func=DelReport.as_view('report_del'))