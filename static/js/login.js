// 设置参数方式
var qrcode = new QRCode('qrcode', {
    text: 'your content',
    width: 216,
    height: 216,
    colorDark: 'black',
    colorLight: 'white',

    correctLevel: QRCode.CorrectLevel.H
});

function qrcodes(var1) {
    // 使用 API
    res = "";
    res = ("Tips: please scan the left side of the small program, and then scan the qr code login " + var1);

    qrcode.clear();
    qrcode.makeCode(res);

}

// 生成随机数
function randomWord(randomFlag, min, max){
    var str = "",
        range = min,
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];

    // 随机产生
    if(randomFlag){
        range = Math.round(Math.random() * (max-min)) + min;
    }
    for(var i=0; i<range; i++){
        pos = Math.round(Math.random() * (arr.length-1));
        str += arr[pos];
    }
    return str;
}
// 执行随机数函数，并生成二维码
function tim(){
    random = randomWord(true, 32,32);
    qrcodes(random);

}

tim();

function random1(){
    $.ajax({
        url: "/login/random",
        type: "post",
        data: {
            "random": random
        },
        success:function (result) {
            if (result.status == "stop"){
               layer.alert('扫码成功，请确认授权！', {icon: 1});

                window.clearInterval(t1);
                window.clearInterval(t2);
            }
        }
});
}

// 1.倒计定时器：setTimeout
t2 =setInterval(random1,5000);
// 2.循环定时器：setInterval
t1 =setInterval(tim,20000);
// 关闭循环





