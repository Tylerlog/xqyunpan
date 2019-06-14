var res_md5 = {};
// 监听a标签，把a标签请求方式改为post请求
//注意进度条依赖 element 模块，否则无法进行正常渲染和功能性操作

layui.use('table', function () {
    var table = layui.table;
    var $ = layui.$;
    var element = layui.element;

    table.render({
        elem: '#test'
        , defaultToolbar: ['filter', 'print', 'exports']
        , url: '/home/select_file'
        , page: {limit: 15, limits: [15, 30, 45,60]} //分页模块
        , where:{
            'type': (window.location.pathname).split('/')[2],  //使用切分去取访问的类型
        }
        , height: 'full-230'
        , skin: 'line'
        // , page: true //开启分页
        , cols: [[
            {checkbox: true, fixed: true , width: 80}
            // , {field: 'id', title: 'ID', width: 80, sort: true, fixed: true}

            , {
                field: 'filename',
                templet: '<div><i class="fa {{d.type}} fa-lg" style="bg"></i>&nbsp;&nbsp;{{d.filename}}</div>',
                title: '文件名',
                sort: true
            }
            , {
                field: 'ope', title: '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp操作', templet: ' ' +
                    '<div><a href="/home/download/{{d.ope}}/{{d.filename}}" download  class="layui-btn layui-btn-sm  layui-btn-primary" ><i class="layui-icon">&#xe601;</i></a>\n' +
                    '     <a class="layui-btn layui-btn-sm  layui-btn-primary"  lay-event="delete"><i class="layui-icon">&#xe640;</i></a>\n' +
                    '     <a class="layui-btn layui-btn-sm  layui-btn-primary" lay-event="edit"><i class="layui-icon">&#xe642;</i></a>\n' +
                    '     </div>', width: 200
            }
            , {field: 'size', title: '大小', width: 150, sort: true}
            , {field: 'datetime', title: '日期', width: 230, sort: true}
            , {field: 'experience', title: '类型', sort: true, width: 130}
        ]]


        , response: {
            statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
        },

    });
//监听事件
    //监听工具条
    table.on('tool(user)', function (obj) { //注：tool是工具条事件名，test是table原始容器的属性 lay-filter="对应的值"
            var data = obj.data; //获得当前行数据
            var layEvent = obj.event; //获得 lay-event 对应的值（也可以是表头的 event 参数对应的值）
            var tr = obj.tr; //获得当前行 tr 的DOM对象

            if (layEvent === 'delete') { //删除
                layer.confirm('真的删除行么', function (index) {
                    // ajax 向服务端发送删除指令 后台执行删除
                    $.ajax({
                        url: '/home/delete',
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
            } else if (layEvent === 'edit') { //编辑
                //do something
                layer.prompt({ // 弹出框
                    title: '修改文件名',
                    formType: 0
                    , value: data.filename
                }, function (value, index) {
                    $.ajax({
                        url: '/home/update',
                        type: 'post',
                        data: {
                            'file_id': obj.data.t_id,
                            'file_name': value,
                        },
                        success: function (result) {
                            if (result.start == '1') {
                                layer.close(index);
                                layer.msg(result.msg)
                                //同步更新缓存对应的值
                                obj.update({
                                    filename: value
                                });
                            } else {
                                layer.close(index);
                                layer.msg(result.msg)
                            }
                        }
                    });


                });
            }
        }
    );
    // 按钮监听


    // 删除选中
    $('#del').on('click', function () {
        var type = $(this).data('type');
        var data_del = table.checkStatus('test');
        console.log(data_del.data)

        if (data_del.data == '') {
            layer.msg('没有已选中的！')
        } else {
            layer.confirm('真的删除行么', function (index) {
                $.ajax({
                    url: '/home/delete',
                    type: 'post',

                    data: {
                        'id': 1,
                        'data': JSON.stringify(data_del)
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
    });

    // 选中下载分享
    $('#download').on('click', function () {
            var download_data = table.checkStatus('test');
            if (download_data.data == '') {
                layer.msg('没有已选中的！')
            } else {
                $.ajax({
                    url: '/home/download_pack',
                    type: 'post',
                    data: {
                        'type': this.id,
                        'data': JSON.stringify(download_data)
                    },
                    success: function (result) {
                        if (result.start == '1') {

                            layer.msg(result.msg);
                            console.log(result.file_path);
                            $('#url').attr('href', result.file_path)[0].click()
                        } else {
                            layer.msg(result.msg)


                        }
                    }
                })

            }
        }
    );

    // 分享选中
    $('#share').on('click', function () {
        var type = $(this).data('type');
        console.log(this.id)

        var download_data = table.checkStatus('test');
        if (download_data.data == '') {
            layer.msg('没有已选中的！')
        } else {
            $.ajax({
                url: '/home/share_page/',
                type: 'post',
                data: {

                    'data': JSON.stringify(download_data),
                    'link': window.location.protocol + '//' + window.location.host + '/home/share_link/',  //使用切分去取访问的类型

                },
                success: function (result) {
                    if (result.start == '1') {

                        layer.prompt({ // 弹出框
                                formType: 2
                                , value: '分享链接：' + result.file_path + '提取密码为：' + result.password + ' 点击分享快去分享给好友啵~~'
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


                    } else {
                        layer.msg(result.msg)
                    }
                }
            })
        }
    });


// 搜索
    $('#seek,#all,#pic,#doc,#video,#music,#rests').on('click', function () {
        //执行重载

        var demoReload = $('#demoReload');
        table.reload('test', {
            url: '/home/select_file'
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


layui.use('layer', function () { //独立版的layer无需执行这一句
    var $ = layui.jquery, layer = layui.layer; //独立版的layer无需执行这一句

    //触发事件
    var active = {
        offset: function (othis) {
            var type = othis.data('type')
                , text = othis.text();

            layer.open({
                type: 1
                , area: ['900px', '500px']
                , offset: type //具体配置参考：http://www.layui.com/doc/modules/layer.html#offset
                , id: 'layerDemo' + type //防止重复弹出
                , content: '<div > <div class="layui-upload">\n' +
                    '&emsp;&emsp;<button type="button" class="layui-btn layui-btn-normal" id="testList">选择多文件</button> \n' +
                    '  <div class="layui-upload-list">\n' +
                    '    <table class="layui-table">\n' +
                    '      <thead>\n' +
                    '        <tr><th>文件名</th>\n' +
                    '        <th>大小</th>\n' +
                    '        <th>状态</th>\n' +
                    '        <th>操作</th>\n' +
                    '      </tr></thead>\n' +
                    '      <tbody id="demoList"></tbody>\n' +
                    '    </table>\n' +
                    '  </div>\n' +
                    '  &emsp;&emsp;<button type="button" class="layui-btn" id="testListAction">开始上传</button>\n' +
                    '</div> <script>layui.use(\'upload\', function(){\n' +
                    '  var $ = layui.jquery\n' +
                    '  ,upload = layui.upload;\n' +
                    '  //多文件列表示例\n' +
                    '  var demoListView = $(\'#demoList\')\n' +
                    '  ,uploadListIns = upload.render({\n' +
                    '    elem: \'#testList\'\n' +
                    '    ,url: \'/home/upload/\'\n' +
                    '    ,accept: \'file\'\n' +
                    '    ,multiple: true\n' +
                    '    ,auto: false\n' +
                    '    ,size:1073741824\n' +
                    '    ,bindAction: \'#testListAction\'\n' +
                    '        ,headers: {token: \'sasasas\'} \n' +
                    '    ,choose: function(obj){\n' +
                    '      var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列\n' +
                    '      //读取本地文件\n' +
                    '      obj.preview(function(index, file, result){\n' +
                    '        check(file); // 执行获取md5    \n' +
                    '        var tr = $([\'<tr id="upload-\'+ index +\'">\'\n' +
                    '          ,\'<td>\'+ file.name +\'</td>\'\n' +
                    '          ,\'<td>\'+ (file.size/1014).toFixed(1) +\'kb</td>\'\n' +
                    '          ,\'<td>等待上传</td>\'\n' +
                    '          ,\'<td>\'\n' +
                    '            ,\'<button class="layui-btn layui-btn-xs demo-reload layui-hide">重传</button>\'\n' +
                    '            ,\'<button class="layui-btn layui-btn-xs layui-btn-danger demo-delete">删除</button>\'\n' +
                    '          ,\'</td>\'\n' +
                    '        ,\'</tr>\'].join(\'\'));\n' +
                    '\n' +
                    '        //单个重传\n' +
                    '        tr.find(\'.demo-reload\').on(\'click\', function(){\n' +
                    '          obj.upload(index, file);\n' +
                    '        });\n' +
                    '\n' +
                    '        //删除\n' +
                    '        tr.find(\'.demo-delete\').on(\'click\', function(){\n' +
                    '          delete files[index]; //删除对应的文件\n' +
                    '          tr.remove();\n' +
                    '          uploadListIns.config.elem.next()[0].value = \'\'; //清空 input file 值，以免删除后出现同名文件不可选\n' +
                    '        });\n' +
                    '\n' +
                    '        demoListView.append(tr);\n' +
                    '      });\n' +
                    '    }\n' +
                    ',before: function(obj){ //obj参数包含的信息，跟 choose回调完全一致，可参见上文。\n' +
                    'this.data={\'md5\':JSON.stringify(res_md5)}\n' +
                    '} \n' +
                    '    ,done: function(res, index, upload){\n' +
                    'delete res_md5[res.file_name] \n' +
                    'if(res.code == 0){ //上传成功\n' +
                    '        var tr = demoListView.find(\'tr#upload-\'+ index)\n' +
                    '        ,tds = tr.children();\n' +
                    '        tds.eq(2).html(\'<span style="color: #5FB878;">上传成功！</span>\');\n' +
                    '        tds.eq(3).html(\'\'); //清空操作\n' +
                    '        return delete this.files[index]; //删除文件队列已经上传成功的文件\n' +
                    '      }if(res.code == 1){ //上传成功\n' +
                    '        var tr = demoListView.find(\'tr#upload-\'+ index)\n' +
                    '        ,tds = tr.children();\n' +
                    '        tds.eq(2).html(\'<span style="color: red;">文件已存在</span>\');\n' +
                    '        tds.eq(3).html(\'\'); //清空操作\n' +
                    '        return delete this.files[index]; //删除文件队列已经上传成功的文件\n' +
                    '      }if(res.code == 2){ //上传成功\n' +
                    '        var tr = demoListView.find(\'tr#upload-\'+ index)\n' +
                    '        ,tds = tr.children();\n' +
                    '        tds.eq(2).html(\'<span style="color: #5FB878;">秒传成功！</span>\');\n' +
                    '        tds.eq(3).html(\'\'); //清空操作\n' +
                    '        return delete this.files[index]; //删除文件队列已经上传成功的文件\n' +
                    '      }\n' +
                    '\n' +
                    '      this.error(index, upload);\n' +
                    '    }\n' +
                    '    ,error: function(index, upload){\n' +
                    '      var tr = demoListView.find(\'tr#upload-\'+ index)\n' +
                    '      ,tds = tr.children();\n' +
                    '      tds.eq(2).html(\'<span style="color: #FF5722;">上传失败</span>\');\n' +
                    '      tds.eq(3).find(\'.demo-reload\').removeClass(\'layui-hide\'); //显示重传\n' +
                    '    }\n' +
                    '    ,cancel: function (index,upload) {\n' +
                    '      alert(\'aaa\')\n' +
                    '\n' +
                    '      }\n' +
                    '  });\n' +
                    '\n' +
                    '\n' +
                    '});</script></div>'

                , btn: '关闭全部'
                , btnAlign: 'c' //按钮居中
                , shade: 0 //不显示遮罩
                , yes: function () {
                    // layer.closeAll();
                    window.location.reload(true)


                }
            });
        }
    };

    $('#layerDemo .layui-btn').on('click', function () {
        var othis = $(this), method = othis.data('method');
        active[method] ? active[method].call(this, othis) : '';
    });

});

// 生成MD5的函数
function md5s(str) {
    var MD5 = new Hashes.MD5().hex(str)
    return MD5
}

// Button按钮点击调用此函数。fileId为上传文件input的id值
function check(fileId, split_num = 32, get_byte = 64) {
    var info = new String;
    var sum = 0;
    /*fileId：文件对象
    split_num: 需要分割生成MD5的数量，默认32
    get_byte: 每段需要取的字节个数，默认64字节
    小于2MB的文件直接MD5*/

    // 判断 split_num和get_byte 是否为数字
    // fileId为：
    // file {name: "System Toolkit_2.2.1_xclient.info.dmg", lastModified: 1559223750878, lastModifiedDate: Thu May 30 2019 21:42:30 GMT+0800 (中国标准时间), webkitRelativePath: "", size: 18142208, …}lastModified: 1559223750878lastModifiedDate: Thu May 30 2019 21:42:30 GMT+0800 (中国标准时间) {}name: "System Toolkit_2.2.1_xclient.info.dmg"size: 18142208type: ""webkitRelativePath: ""__proto__: File "1212"

    var blob = fileId;
    // 定义常量 const ，不可修改
    // 获取文件的总大小
    const size = blob.size;
    // 计算每段的大小
    const mean_size = Math.floor(size / split_num);
    // 判断文件大小，如果小于 split_num * get_byte 就直接MD5
    if (size < split_num * get_byte) {


        var read = new FileReader();             //创建读取器对象FileReader
        read.readAsBinaryString(blob);            //开始读取文件
        read.onload = function () {              //数据读完会触发onload事件
            res_md5[fileId.name] = md5s(read.result)
            return res_md5
        }

    } else {
        var start = 0;  // 定义开始位置
        var end = get_byte; // 定义截取结束位置

        while (start < size) {
            var read = new FileReader();              //创建读取器对象FileReader
            blobs = blob.slice(start, end); //创建Blob对象
            read.readAsText(blobs);                  //开始读取文件
            start = start + mean_size;              // 下一段开始位置
            end = start + get_byte;                 // 定义截取结束位
            read.onload = function (aa) {               //数据读完会触发onload事件
                sum += 1;
                info = info + aa.currentTarget.result;              //read有个result属性存放这结果，从result获取到数据,再拼接字符

                if (sum === split_num) {
                    res_md5[fileId.name] = md5s(info);                //进行加密
                    info = null;
                    return res_md5
                }
            };

        }


    }
}


