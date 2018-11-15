/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2017-03-07 17:10:29
 * @version $Id$
 */
!function(){
    $.infoData=function(){
        var info={
            'companyInfo':companyInfo?JSON.parse(companyInfo.replace(/\n/g,"${n}")):{},
            'siteInfo':siteInfo?JSON.parse(siteInfo.replace(/\n/g,"${n}")):{}
        }
        var obj={};
        $.each(info,function (k,v) {
            if (/^(companyInfo)|(siteInfo)$/.test(k)){
                $.each(v, function (k,v) {
                    obj[k]=(v===null?"":v);
                });
            }
        });
        return obj;
    }();
    if($.isEmptyObject($.infoData)) return ;
    $(".wqdelementEdit[data-elementtype='info']").each(function (){
        var $t=$(this),$txt=$t.find(".wqd-infoTxt em"),
            param=$t.attr("data-param"),
            $img=$t.find("img"),
            newTxt;
        newTxt=$.infoData[param];
        if (param=="registerArea") newTxt=$.infoData["registerProvince"]+" "+$.infoData["registerCity"]+" "+$.infoData["registerArea"];
        if(param=="companyArea")  newTxt=$.infoData['province']+" "+$.infoData['city']+" "+$.infoData['area']+($.trim($.infoData['detailAddress'])&&(" "+$.trim($.infoData['detailAddress'])));
        if(param=="businessModel"&&$.infoData['businessModel']=="其他") newTxt=$.infoData['businessModelText'];
        if(param=="registerFund"&&$.infoData['registerFund']) newTxt=$.infoData['registerFund']+"万元";
        //图片
        if (/honorQualification|brandLogo|businessLicense/.test(param)){
            var imgPra=param.replace(/[\d]+$/,"");
            var imIdx=parseInt(param.replace(/^[\D]+/,""),10)-1;
        }
        var uri=imgPra?$.infoData[imgPra].split(",")[!imIdx?0:imIdx]:'';
        if ($txt.length&&newTxt!=$txt.text()){
            $txt.text(newTxt.replace(/\$\{n\}/g,"\n"));
            $txt.parents(".wqdelementEdit").height($txt.height());
        }else if ($img.length){
            var isDel=true;
            $.each($.infoData[imgPra].split(","),function (i,v) {
                var src=$img.attr("src");
                var str=/wqdian.net\//g.test(src)?"wqdian.net/":"wqdian.com/"
                if (v==src.split(str)[1]){
                    isDel=false;
                }
            });
            isDel&&$t.remove();
        };
    });
}();
