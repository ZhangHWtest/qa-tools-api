# -*- coding: utf-8 -*-

from .views import *
from .views import tools

tools.add_url_rule('/tools/live_lesson_today', view_func=LiveLessonToday.as_view('live_lesson_today'))
tools.add_url_rule('/tools/live_lesson_yesterday', view_func=LiveLessonYesterday.as_view('live_lesson_yesterday'))
tools.add_url_rule('/tools/course_info_by_mobile', view_func=CourseInfoByMobile.as_view('course_info_by_mobile'))
tools.add_url_rule('/tools/auth_record_by_mobile', view_func=AuthRecordByMobile.as_view('auth_record_by_mobile'))
tools.add_url_rule('/tools/user_info_by_xid', view_func=UserInfoByXid.as_view('user_info_by_xid'))
tools.add_url_rule('/tools/course_info_by_live_id', view_func=CourseInfoByLiveId.as_view('course_info_by_live_id'))
