layui.use('table', function () {
    var table = layui.table;
    var $ = layui.$;
    var element = layui.element;

    table.render({
        elem: '#share'
        , url: '/home/share_list'
        , page: {limit: 15, limits: [15, 30, 45, 60]} //分页模块
        , where: {
            // 'type': (window.location.pathname).split('/')[2],  //使用切分去取访问的类型
            'type': 'share',
            'link':window.location.protocol + '//' + window.location.host + '/home/share_link/',

        }
        , height: 'full-230'
        , skin: 'line'
        // , page: true //开启分页
        , cols: [[
            {checkbox: true, fixed: true}
            , {field: 'id', title: 'ID', width: 80, sort: true, fixed: true}
            , {field: 'share_name', title: '分享名', sort: true}
            , {field: 'share_path', title: '分享链接', width: 370, sort: true}
            , {field: 'share_password', title: '分享密码', width: 180, sort: true}
            , {field: 'share_time', title: '分享日期', sort: true, width: 200}
            , {
                field: 'ope', title: '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;操作', templet: ' ' +
                    '<div>\n' +
                    '     <a class="layui-btn layui-btn-sm  layui-btn-primary"  lay-event="share_cancel">&nbsp;<i class="fa fa-close"></i>&nbsp;</a>\n' +
                    '     <a class="layui-btn layui-btn-sm  layui-btn-primary"  lay-event="copy_link">&nbsp;<i class="fa fa-copy"></i>&nbsp;</a>\n' +
                    '     </div>', width: 200
            }

        ]]


        , response: {
            statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
        },

    });

    //监听工具条
    table.on('tool(shares)', function (obj) { //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        var layEvent = obj.event; //获得 lay-event 对应的值（也可以是表头的 event 参数对应的值）
        var tr = obj.tr; //获得当前行 tr 的DOM对象

        if (layEvent === 'share_cancel') { //取消分享
            layer.confirm('真的取消分享么', function (index) {
                // ajax 向服务端发送删除指令 后台执行删除
                $.ajax({
                    url: '/home/share_cancel',
                    type: 'post',
                    data: {
                        'file_id': obj.data.t_id,
                    },
                    success: function (result) {
                        if (result.start == '1') {
                            layer.close(index);

                            layer.msg(result.msg)
                            obj.del(); //删除对应行（tr）的DOM结构，并更新缓存
                        } else {
                            layer.close(index);

                            layer.msg(result.msg)
                        }

                    }
                });
            });
        } else if (layEvent === 'copy_link') { //复制链接
            layer.prompt({ // 弹出框
                    formType: 2
                    , value: '分享链接：' + data.share_path + '提取密码为：' + data.share_password + ' 点击分享快去分享给好友啵~~'
                    , area: ['340px', '50px']
                    , title: '分享链接'
                    , btn: ['点击复制']
                },
                function (value, index, elem) {
                    $('.layui-layer-input').select(); // 选择对象
                    document.execCommand("Copy"); // 执行浏览器复制命令
                    layer.close(index);

                    layer.msg("已复制好，快去分享给好友吧。");
                })


        }
    })

// 选中取消分享
    $('#share_cancel_all').on('click', function () {
            var cancel_data = table.checkStatus('share');

            if (cancel_data.data == '') {
                layer.msg('没有已选中的！')
            } else {
                layer.confirm('真的取消所选分享么', function (index) {
                    $.ajax({
                        url: '/home/share_cancel',
                        type: 'post',

                        data: {
                            'id': 1,
                            'data': JSON.stringify(cancel_data)
                        },
                        success: function (result) {
                            if (result.start == '1') {
                                layer.close(index);
                                layer.msg(result.msg);
                                window.location.reload(true)
                            } else {
                                layer.close(index);
                                layer.msg(result.msg)
                            }

                        }


                    })
                })

            }
        }
    );
   $('#seeks').on('click', function () {
        //执行重载

        var demoReload = $('#demoReload');
        table.reload('share', {
            url: '/home/share_list'
            , method: 'post'
            , where: { //设定异步数据接口的额外参数，任意设
                filename: demoReload.val(),
                type:(window.location.pathname).split('/')[2],  //使用切分去取访问的类型
            }
            // , bbb: 'yyy'
            //…

            , page: {
                curr: 1 //重新从第 1 页开始
            }
        }); //只重载数据


    });
});
