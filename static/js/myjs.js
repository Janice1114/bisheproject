//###################cookie###################//
function setCookie(name,value,expires){
    document.cookie = name + "=" + value + "; " + expires;
}
function getCookie(name){
    var name = name + "=";
    var cname = document.cookie.split(';');
    for(var i=0; i<cname.length; i++)
    {
        var value = cname[i].trim();
        if (value.indexOf(name)==0)
            return value.substring(name.length,value.length);
    }
    return "";
}
//判断是否为图像类型
function get_type(imgFile){
    var rFilter = /^(?:image\/bmp|image\/cis\-cod|image\/gif|image\/ief|image\/jpeg|image\/jpeg|image\/jpeg|image\/pipeg|image\/png|image\/svg\+xml|image\/tiff|image\/x\-cmu\-raster|image\/x\-cmx|image\/x\-icon|image\/x\-portable\-anymap|image\/x\-portable\-bitmap|image\/x\-portable\-graymap|image\/x\-portable\-pixmap|image\/x\-rgb|image\/x\-xbitmap|image\/x\-xpixmap|image\/x\-xwindowdump)$/i;
    if (!rFilter.test(imgFile.type)) {
        return false
    }
    return true
}
// 单一图片预览
function previewCover(e){
    var file=e.files[0]   // 获取input上传的图片数据;
    if(file != null){
        if(get_type(file)) {
            url=getObjectURL(file)
            var showCover = document.getElementById("showCover");
            showCover.innerHTML += "<img id='img_cover' />";
            var imgObjPreview = document.getElementById("img_cover");
            imgObjPreview.style.width="20%"
            imgObjPreview.src = url
        }
        else{
            alert('图片格式不正确')
            e.value = ""
            e.outerHTML = e.outerHTML
        }
    }
}
// 多图图片预览
function previewImage(e,num){
    var file=e.files  // 获取input上传的图片数据;
    var len = file.length
    if(len > num){
        alert("最多上传"+num+"张图片")
        e.value = ""
        e.outerHTML = e.outerHTML
    }
    if(len > 0 && len <= num){
        var showImage = document.getElementById("showImage");
        for(var i = 0 ; i < len ;i++){
            if(get_type(file[i])) {
                url=getObjectURL(file[i])
                showImage.innerHTML += "<img id='img" + i + "'  />";
                var imgObjPreview = document.getElementById("img"+i);
                imgObjPreview.style.width="20%"
                imgObjPreview.src = url
            }
            else{
                alert('图片格式不正确')
                e.value = ""
                e.outerHTML = e.outerHTML
                showImage.innerHTML=""
                break;
            }
        }

    }
}
//建立一個可存取到該file的url
function getObjectURL(file) {
    var url = null ;
    if (window.createObjectURL!=undefined) { // basic
        url = window.createObjectURL(file) ;
    } else if (window.URL!=undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file) ;
    } else if (window.webkitURL!=undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file) ;
    }
    return url ;
}
//登录
function login_submin(type) {
    var name = document.getElementById("name").value
    if(name == '') {
      alert("用户帐号不能为空");
      name.focus();
        return false;
       }
     password = document.getElementById("password").value
       if(password =='') {
        alert("请输入登录密码!");
        password.focus();
        return false;
       }
     vcode = document.getElementById("vcode").value
     url = "";
     if(type == 0){
         url = '/user_login_check/'
     }
     else{
         url = '/store_login_check/'
     }
     $.post(url,{
         'name':name,'password':password,'vcode':vcode
     },function (data) {
         if(data.msg == "ok") {
             location.href = '/store_home/' //跳转到成功页面
         }else if(data.msg == "ok_user"){
             location.href = '/user_home/' //跳转到成功页面
         } else if(data.msg == 'fail'){
             alert("用户名或密码错误")
         }else if(data.msg == "fail_verify"){
             alert("验证码错误")
             window.location.reload()
         }
     })
}
//增加商品
function showGoods(){
    var AddGoods = document.getElementById("AddGoods")
    AddGoods.style.display = "block"
}
function hideGoods() {
     var AddGoods = document.getElementById("AddGoods")
    AddGoods.style.display = "none"
}
function addGoods(form) {
    if(form.goods_Allowcard_check.checked){
        form.goods_Allowcard.value = 0
    }
    else{
        form.goods_Allowcard.value = 1
    }
    var goods_name = form.goods_name.value
    var goods_message = form.goods_message.value
    //小数
    var goods_price = form.goods_price.value
    var stock_price = form.stock_price.value
    var goods_cardScore = form.goods_cardScore.value
    var goods_discount = form.goods_discount.value
    //整数
    var goosd_warn = form.goosd_warn.value
    var goods_left = form.goods_left.value

    if(goods_name == '') {
     alert("商品名不能为空");
    form.goods_name.focus();
       return false;
  }
    if(goods_message==''){
        alert("商品信息不能为空");
        form.goods_message.focus();
        return false;
    }
    var reg1 = /^[0-9]{1,}[.][0-9]*$/;
    var reg2 = /^[0-9]+$/;
    if(!reg1.exec(goods_price) && !reg2.exec(goods_price)){
       alert("价格只能为小数或者整数类型");
    form.goods_price.focus();
       return false;
    }
    if(!reg1.exec(stock_price) && !reg2.exec(stock_price)){
       alert("价格只能为小数或者整数类型");
    form.stock_price.focus();
       return false;
    }
    if(!reg1.exec(goods_cardScore) && !reg2.exec(goods_cardScore)){
       alert("积分只能为小数或者整数类型");
    form.goods_cardScore.focus();
       return false;
    }
    if(!reg1.exec(goods_discount) && !reg2.exec(goods_discount)){
        alert("折扣只能为小数或者整数类型");
      form.goods_discount.focus();
        return false;
    }
    if(goods_discount > 1){
         alert("折扣不能大于1");
      form.goods_discount.focus();
         return false;
    }
    if(!reg2.exec(goosd_warn)){
       alert("库存预警数量只能为整数类型");
    form.goosd_warn.focus();
       return false;
    }
     if(!reg2.exec(goods_left)){
       alert("商品数量只能为整数类型");
    form.goods_left.focus();
       return false;
    }
    return true
}
//增加库存s
function addStock(goods_id) {
    var number = document.getElementById('number').value
    var stock_price = document.getElementById('stock_price').value
    var reg1 = /^[0-9]+$/;
    var reg2 = /^[0-9]{1,}[.][0-9]*$/;
    if(!reg1.exec(number)){
        alert("数量只能为整数类型");
    }
    if(!reg1.exec(stock_price) && !reg2.exec(stock_price)){
       alert("价格只能为小数或者整数类型");
    }
    else{
        url="/goods_stock/"
         $.post(url,{
                 'goods_id':goods_id,'number':number,'stock_price':stock_price
             },function (data) {
                if(data.msg == "ok") {
                    alert('入库成功')
                    window.location.reload()
                }
                else if(data.msg=="fail"){
                    alert('入库失败')
                }
              })
    }
}
//会员卡注册
function card_register(user_name,store_name) {
    url="/card_register/"
    $.post(url,{
         'user_name':user_name,'store_name':store_name,
        },function (data) {
        if(data.msg == "ok") {
            alert('注册成功')
            window.location.reload()
        }
        else if(data.msg=="fail"){
            alert('注册失败')
        }
        else if(data.msg=="duplicate"){
            alert("重复注册")
        }
    })
}

var store_list = [];
var buy_list = {};
var number_list = {};
function buyGoods(id,number,store_name) {
    var buy_number = $('#buy_number').val();
    var reg1 = /^[0-9]+$/;
    if(!reg1.exec(buy_number)){
        alert("数量只能为整数类型");
        return ;
    }
    if(buy_number > number){
        alert("购买数量不能大于剩余数量");
        return ;
    }
    if(store_list.indexOf(store_name) == -1){
        store_list.push(store_name);
    }
    if(buy_list[store_name] == undefined){
        buy_list[store_name] = [];
        number_list[store_name]  = [];
    }
    else{
        if(buy_list[store_name].indexOf(id) == -1){
            buy_list[store_name].push(id);
            if(buy_number > number){
                alert("购买数量不能超过剩余数量");
                $("#addToCarModal").modal('hide');
                return ;
            }
            else{
                buy_list[store_name].push(buy_number);
            }
        }
        else{
            var n = buy_number+number_list[store_name];
            if(n > number){
                alert("购买数量不能超过剩余数量");
                $("#addToCarModal").modal('hide');
                return ;
            }
            number_list[store_name] = n;
        }
    }
    $("#addToCarModal").modal('hide');
    //  url="/buy_goods/"
    // $.post(url,{
    //     'goods_id':id,'number':buy_number,user_name:user_name,store_name:store_name
    //     },function (data) {
    //     if(data.msg == "ok") {
    //         alert('购买成功')
    //         window.location.reload()
    //     }
    //     else if(data.msg=="fail"){
    //         alert('购买失败')
    //     }
    //   })
}