$('#btn').on('change',function () {
   var name = $('#name').val()
   var password = $('#password').val()
    $.ajax({
        url:'/aaa',
        type:'post',
        data:{
            'name':name,
            'password':password
        },
        success:function (e) {
            if (e.start==1){
                swal("恭喜你", e.msg, "success");
            }else{
                swal("恭喜你", e.msg, "error");
            }
        },

    })



});