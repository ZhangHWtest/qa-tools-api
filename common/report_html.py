# encoding: utf-8

default_title = '接口测试'


def create_title(t=default_title):
    title = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>%s</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <!-- 引入 Bootstrap -->
            <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
            <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
            <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
            <!--[if lt IE 9]>
             <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
             <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
            <![endif]-->
            <style type="text/css">
                .hidden-detail,.hidden-tr{
                    display:none;
                }
            </style>
        </head>
        <body>
    ''' % t
    return title


content = '''
<div  class='col-md-11 col-md-offset-11' style="margin-left:2%;margin-top:5px;">
<h1>测试平台接口测试的结果</h1>'''


def statistic(st, et, passes, fails, excepts, unknown, maxi, mini, aver):
    stat = '''
    <div>
        <table  class="table table-hover table-condensed">
            <tbody>
                <tr>
                    <td><strong>开始时间:</strong> %s</td></tr>
                    <td><strong>结束时间:</strong> %s</td></tr>
                    <td><strong>耗时:</strong> %s</td></tr>
                    <td>
                        <strong>结果: </strong>
                        <span>
                        通过: <strong >%s</strong>
                        失败: <strong >%s</strong>
                        异常: <strong >%s</strong>
                        未知: <strong >%s</strong>
                    </td>                 
                </tr>
                <tr>
                    <td>
                       <strong>单接口耗时最大值:</strong>%s s，
                       <strong>最小值:</strong> %s s，
                       <strong>平均耗时:</strong> %s s
                   </td>
               </tr> 
           </tbody>
       </table>
    </div> 
    ''' % (st, et, (et-st), passes, fails, excepts, unknown, maxi, mini, aver)
    return stat


table_header = '''
<div class="row " style="margin:35px">
    <div style='    margin-top: 5%;' >
        <div class="btn-group" role="group" aria-label="...">
            <button type="button" id="check-all" class="btn btn-primary">所有用例</button>
            <button type="button" id="check-success" class="btn btn-success">成功用例</button>
            <button type="button" id="check-danger" class="btn btn-danger">失败用例</button>
            <button type="button" id="check-warning" class="btn btn-warning">错误用例</button>
            <button type="button" id="check-except" class="btn btn-defult">异常用例</button>
        </div>
        <div class="btn-group" role="group" aria-label="...">
        </div>
        <table class="table table-hover table-condensed table-bordered" 
            style="word-wrap:break-word; word-break:break-all;  margin-top: 7px;">
        <tr >
            <td style="width:4%"><strong>用例ID&nbsp;</strong></td>
            <td style="width:5%"><strong>项目</strong></td>
            <td style="width:5%"><strong>请求方式</strong></td>
            <td style="width:10%"><strong>url</strong></td>
            <td style="width:6%"><strong>参数</strong></td>
            <td style="width:6%"><strong>headers</strong></td>
            <td style="width:5%"><strong>预期</strong></td>
            <td><strong>实际返回</strong></td>  
            <td style="width:3%"><strong>结果</strong></td>
            <!-- <td style="width:60px"><strong>用例ID&nbsp;</strong></td>
            <td style="width:80px"><strong>项目</strong></td>
            <td style="width:80px"><strong>请求方式</strong></td>
            <td style="width:100px"><strong>url</strong></td>
            <td style="width:100px"><strong>参数</strong></td>
            <td style="width:100px"><strong>headers</strong></td>
            <td style="width:100px"><strong>预期</strong></td>
            <td><strong>实际返回</strong></td>  
            <td style="width:60px"><strong>结果</strong></td> -->
        </tr>
'''


def pass_fail(result):
    if result == 1:
        htl = ' <td bgcolor="green">通过</td>'
    elif result == 0:
        htl = ' <td bgcolor="fail">失败</td>'
    elif result == 2:
        htl = '<td bgcolor="#8b0000">异常</td>'
    else:
        htl = '<td bgcolor="#8b0000">未知错误</td>'
    return htl


def case_info(class_id, cid, name, method, path, params, header, expect, response, result):
    info = '''
    <tr class="case-tr %s">
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        %s
    </tr>
    ''' % (class_id, cid, name, method, path, params, header, expect, response, (pass_fail(result)))
    return info


footer = '''
</div></div></table>
<script src="https://code.jquery.com/jquery.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
<script type="text/javascript">
    $("#check-danger").click(function(e){
        $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    });
    $("#check-warning").click(function(e){
         $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    });
    $("#check-success").click(function(e){
         $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    });
    $("#check-except").click(function(e){
         $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".success").addClass("hidden-tr");
    });
    $("#check-all").click(function(e){
        $(".case-tr").removeClass("hidden-tr");
    });
</script>
</body>
</html>
'''


def case_res(titles, st, et, passes, fails, excepts, unknown, id_list, name_list, method_list, path_list, params_list,
             header_list, assert_list, resp_list, result_list, maxi, mini, aver):
    result = ' '
    for i in range(len(id_list)):
        if result_list[i] == 1:
            class_id = "success"
        elif result_list[i] == 0:
            class_id = "warning"
        elif result_list[i] == 2:
            class_id = "danger"
        else:
            class_id = 'error'
        result += (case_info(class_id, id_list[i], name_list[i], method=method_list[i], path=path_list[i],
                             params=params_list[i], header=header_list[i], expect=assert_list[i],
                             response=resp_list[i], result=result_list[i]))
    text = create_title(titles) + content + statistic(st, et, passes, fails, excepts, unknown,
                                                      maxi, mini, aver) + table_header + result + footer
    return text


def generate_report(filepath, tit, st, et, passes, fails, excepts, unknown, cid, cname, method_list, path_list,
                    params_list, header_list, assert_list, resp_list, result_list, maxi, mini, aver):
    texts = case_res(titles=tit, st=st, et=et, passes=passes, fails=fails, excepts=excepts, unknown=unknown,
                     id_list=cid, name_list=cname, method_list=method_list, path_list=path_list,
                     params_list=params_list, header_list=header_list, assert_list=assert_list,
                     resp_list=resp_list, result_list=result_list, maxi=maxi, mini=mini, aver=aver)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(texts)
