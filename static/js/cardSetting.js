
function settingShow(){
    setting()
    $("input[name=Setting]").change(function () {
        setting()
    });
    $("input[name=level]").change(function () {
        number = 2;
        $('#add').html("");
    })
}
function setting() {
    var id = $("input[name=Setting]:checked").attr("id")
    if(id == "Setting1"){
         $('#cardsetting').css("display","block")
        $('#cardsetting').html(main)
    }
    else{
        $('#cardsetting').css("display","none")
    }
}
window.onload = settingShow

var main = "<form  method=\"post\" enctype=\"multipart/form-data\">"+
            "前缀：<input type=\"text\" name=\"store_card_prefix\" maxlength='5' placeholder=\"请输入会员卡前缀，选填\">" +
            "<div>" +
                "等级上升的方法：<br><input type='radio' name='level' id='methon1' checked/>通过积分"+
                             " <input type='radio' name='level'id='methon2' />其他"+
                "<br>会员卡等级和对应的折扣划分：<br>" +
                "1:<input type=\"text\" name=\"store_card_level\" maxlength='5' placeholder=\"会员卡初始等级\">" +
                "<input type=\"text\" name=\"store_card_discount\" maxlength='5' placeholder=\"对应初始折扣\">" +
                "<input type='button' onclick=\"addfunc()\"  value=\"点击增加\">"+
            "</div>" +
            "<div id=\"add\">" +
            "</div>"+
            "会员卡说明：<br><textarea rows=\"4\" cols=\"50\" name='store_card_message'></textarea><br>"+
            "有效期(0表示无限期)：<input maxlength='3' size='4'name='store_card_date' onkeyup=\"value=value.replace(/[^\\d]/g,'')\"/>"+
            "<select id='dateSelect'>" +
                "<option value =\"year\">年</option>" +
                "<option value =\"month\">月</option>" +
                "<option value=\"day\">日</option>" +
           "</select>"+
            "</form>"
var submain1 =  "<input type=\"text\" name=\"store_card_level\" maxlength='5' placeholder=\"会员卡等级\">" +
                "<input type=\"text\" name=\"store_card_discount\" maxlength='5' placeholder=\"会员卡折扣\">"
var submain2 = "<input type=\"text\" name=\"store_card_up_style\" maxlength='5' placeholder=\"等级上升对应的积分\">"
var number = 2;
function addfunc() {
    if(number <= 6){
        $('#add').html($('#add').html()+number+":"+submain1);
        if($('#methon1').attr('checked')){
            $('#add').html($('#add').html()+submain2);
        }
        $('#add').html($('#add').html()+"<br>");
        number = number + 1;
    }
    else{
        alert("增加已经达到上限")
    }
}
function setting_submit(){
    if($("input[name=Setting]:checked").attr("id") == "Setting1"){
        var store_card_prefix = $("input[name=store_card_prefix]").val();
        var levelList = $("input[name=store_card_level]");
        var discountList = $("input[name=store_card_discount]");
        var styleList =  $("input[name=store_card_up_style]");
        var store_card_level="";
        var store_card_discount="";
        var store_card_up_style="";
        var store_card_Ddiscount="";
        var store_card_Dlever=""
        var reg1 = /^[0-9]{1,}[.][0-9]*$/;
        var reg2 = /^[0-9]+$/;
        for(var i = 0 ; i < levelList.length;i++){
            if(levelList[i].value == ""){
                alert('会员等级不能为空');
                return ;
            }
            if(!reg1.exec(discountList[i].value) && !reg2.exec(discountList[i].value)){
                alert('折扣只能为小数或整数');
                return ;
            }
            else{
                if(i == 0){
                    store_card_level = levelList[i].value;
                    store_card_Dlever = levelList[i].value;
                    store_card_discount = discountList[i].value;
                    store_card_Ddiscount = discountList[i].value;
                    store_card_up_style = "0";
                }else{
                    store_card_level = store_card_level + ','+levelList[i].value;
                    store_card_discount =store_card_discount + ',' + discountList[i].value;
                    if($("input[name=level]:checked").attr("id") == "methon1"){
                        if(styleList[i].value == ""){
                            alert("对应积分不能为空");
                            return ;
                        }
                        store_card_up_style = store_card_up_style + ',' + styleList[i].value;
                    }else{
                        store_card_up_style = store_card_up_style + ',' +  "0";
                    }
                }
            }
        }
        var number=1;
        if($('#dateSelect').val()=='year'){
            number = 365;
        }
        else if($('#dateSelect').val()=='month'){
            number = 30;
        }
        var store_card_date = $("input[name=store_card_date]").val()*number;
        var store_card_message = $("input[name=store_card_message]").val();

        url="/card_setting/"
        $.post(url,{
            'store_card_prefix':store_card_prefix,'store_card_level':store_card_level,
            'store_card_discount':store_card_discount,'store_card_Ddiscount':store_card_Ddiscount,
            'store_card_Dlever':store_card_Dlever,'store_card_up_style':store_card_up_style,
            'store_card_date':store_card_date,'store_card_message':store_card_message
        },function (data) {
            if (data.msg=="ok"){
                location.href = '/store_home/'
            }
            if(data.msg=="fail"){
                alert('设置失败,请稍后再试');
                window.location.reload()
            }
        })
    }
}




