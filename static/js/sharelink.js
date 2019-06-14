layui.use('table', function () {
    var table = layui.table;
    var $ = layui.$;
    var element = layui.element;
    $('#select_share_link').on('click', function () {
        table.render({
            elem: '#share'
            , defaultToolbar: ['filter', 'print', 'exports']
            , url: '/home/select_share_link/'+window.location.pathname
            , page: {limit: 15, limits: [15, 30, 45, 60]} //分页模块
            , where: {

                'password': $('#share_password').val(),  //获取分享密码
            }
            , height: 'full-230'
            , skin: 'line'
            // , page: true //开启分页
            , cols: [[
                {checkbox: true, fixed: true, width: 80}
                // , {field: 'id', title: 'ID', width: 80, sort: true, fixed: true}

                , {
                    field: 'filename',
                    templet: '<div><i class="fa {{d.type}} fa-lg" style="bg"></i>&nbsp;&nbsp;{{d.filename}}</div>',
                    title: '文件名',
                    sort: true
                }
                , {
                    field: 'ope',
                    title: '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp操作',
                    templet: ' ' +
                        '<div><a href="/home/download/{{d.ope}}/{{d.filename}}" download  class="layui-btn layui-btn-sm  layui-btn-primary" ><i class="layui-icon">&#xe601;</i></a>\n' +
                        '     <a class="layui-btn layui-btn-sm  layui-btn-primary"  lay-event="delete"><i class="layui-icon">&#xe640;</i></a>\n' +
                        '     <a class="layui-btn layui-btn-sm  layui-btn-primary" lay-event="edit"><i class="layui-icon">&#xe642;</i></a>\n' +
                        '     </div>',
                    width: 200
                }
                , {field: 'size', title: '大小', width: 150, sort: true}
                , {field: 'datetime', title: '日期', width: 230, sort: true}
                , {field: 'experience', title: '类型', sort: true, width: 130}
            ]]
            , done: function (res, curr, count) {
                console.log(res['msg'])
            }
            , text: {none: '暂无相关数据'}

            , response: {


                statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
            },

        });
    });
    $('#seeks').on('click', function () {
        //执行重载

        var demoReload = $('#demoReload');
        table.reload('share', {
            url: '/home/select_share_link/'+ window.location.pathname.split('/')[3]
            , method: 'post'
            , where: { //设定异步数据接口的额外参数，任意设
                filename: demoReload.val(),
                'password': $('#share_password').val(),  //获取分享密码
            }
            // , bbb: 'yyy'
            //…

            , page: {
                curr: 1 //重新从第 1 页开始
            }
        }); //只重载数据


    });

});