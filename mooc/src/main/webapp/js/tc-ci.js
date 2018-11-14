/**
 * Created by lynn on 2017/7/1.
 */

$(function () {

    var url = {
        getAbsent: "/mooc/getAbsent",
        	cistatus:"/mooc/getAb",
            postci:"/mooc/postAb"
    };

    //TODO

    function loadAbsent() {
        $.get(url.getAbsent, function (json) {
            var tbody = $('table').find('tbody');
            //var jsonParsed = json;
            var jsonParsed = eval('(' + json + ')');
            for (var i = 0; i < jsonParsed.length; i++) {
                var tr = $("<tr></tr>");
                var stuID = jsonParsed[i].stuID;
                var stuName = jsonParsed[i].stuName;
                var stuTeam = jsonParsed[i].stuTeam;
                var record=jsonParsed[i].date;
                
                var IDtd = $("<td>" + stuID + "</td>");
                IDtd.appendTo(tr);
                var nametd = $("<td>" + stuName + "</td>");
                nametd.appendTo(tr);
                var teamtd = $("<td>" + stuTeam + "</td>");
                teamtd.appendTo(tr);
                var recordtd = $("<td class='red-text'>" + record + "</td>");
                recordtd.appendTo(tr);

                tr.appendTo(tbody);
            }


        });
    }
    function checkinStatus() {
        $.get(url.cistatus,function (json) {
            var jsonP=eval('(' + json + ')');
            if(!jsonP.status){
                $('.beginci').css('display','block');
                $('.stopci').css('display','none');
            }else{
                $('.stopci').css('display','block');
                $('.beginci').css('display','none');
            }
        })
    }
    loadAbsent();
    checkinStatus();

    $('.beginci').click(function () {
        var params={
            status:1
        };
        $.get(url.postci,params,function () {
            $('.stopci').css('display','block');
            $('.beginci').css('display','none');
            Materialize.toast('开始签到！', 4000);
        })
    });

    $('.stopci').click(function () {
        var params={
            status:0
        };
        $.get(url.postci,params,function () {
        	loadAbsent();
            $('.beginci').css('display','block');
            $('.stopci').css('display','none');
            Materialize.toast('结束签到！', 4000);
        })
    });

})
