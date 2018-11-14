/**
 * Created by lynn on 2017/7/1.
 */

$(function () {
    var url = {
        getGrade: "/mooc/getGradeG",
        postGrade: "/mooc/postGradeG",
        	getTemp:"/mooc/exportGradeTemplate",
            getGradexls:"/mooc/exportGrade",

    };
    var grade = [{
        ID: "2",
        name: "RUA",
        grade: -1
    }, {
        ID: "1",
        name: "RUA",
        grade: 100
    }];

    function loadGrade() {
        $.get(url.getGrade, function (json) {
            //var jsonParsed = json;
            var jsonParsed = eval('(' + json + ')');

            var tbodydom = $('.stu-tbl').find('tbody');

            for (var i = 0; i < jsonParsed.length; i++) {
                var tr = $("<tr></tr>");

                var teamID = jsonParsed[i].ID;
                var teamName = jsonParsed[i].name;
                var teamGrade = jsonParsed[i].grade;

                if (teamGrade != -1) {
                    var IDtd = $("<td>" + teamID + "</td>");
                    IDtd.appendTo(tr);
                    var nametd = $("<td>" + teamName + "</td>");
                    nametd.appendTo(tr);
                    var gradetd = $("<td>" + teamGrade + "</td>");
                    gradetd.appendTo(tr);
                    var newGrade = $('<td class="input-field col s2"> <input type="text" class="validate"> </td>');
                    newGrade.appendTo(tr);

                    var send = $("<td><i class='material-icons publishGrade waves-effect waves-teal'>publish</i></td>");
                    send.appendTo(tr);
                    tr.appendTo(tbodydom);
                } else {
                    var IDtd = $("<td>" + teamID + "</td>");
                    IDtd.appendTo(tr);
                    var nametd = $("<td>" + teamName + "</td>");
                    nametd.appendTo(tr);
                    var gradetd = $("<td>无</td>");
                    gradetd.appendTo(tr);

                    var newGrade = $('<td class="input-field col s2"> <input type="text" class="validate"> </td>');
                    newGrade.appendTo(tr);
                    var send = $("<td><i class='material-icons publishGrade waves-effect waves-teal'>publish</i></td>");
                    send.appendTo(tr);

                    tr.appendTo(tbodydom);
                }

            }

        })

    }

    loadGrade();

    $('.stu-tbl').on('click', '.publishGrade', function () {
        var _this = this;
        var newgrade = $(_this).parent().prev();
        var grade = $(newgrade).prev();

        var gradeNum = $(newgrade).find('input').val();

        var ID = $($(grade).prev()).prev();
        var idcontent=$(ID).html();
        
        var params = {
            ID: idcontent,
            grade: gradeNum
        };
        if (gradeNum >= 0 && gradeNum <= 100) {
            /*$.post(url.postGrade, params, function () {
                Materialize.toast('打分成功', 4000);
                $(grade).html(gradeNum);
            })*/
            $.ajax({
            	type:"POST",
            	url:url.postGrade,
            	data:params,
            	trditional:true,
            	success:function(){
            		Materialize.toast('打分成功', 4000);
                    $(grade).html(gradeNum);
            	},
            	error:function(){
            		Materialize.toast('打分失败', 4000);
                  
            	}
            })
        }else{
            Materialize.toast('请输入0~100之间的数字', 4000);

        }
    })

    /*$('.down-temp').click(function () {
        $.get(url.getTemp,function () {
            Materialize.toast('模板下载成功', 4000);
        })
        $.ajax({
            	type:"GET",
            	url:url.getTemp,
            
            	success:function(){
            		Materialize.toast('打分成功', 4000);
                  
            	},
            	error:function(){
            		Materialize.toast('打分失败', 4000);
                  
            	}
            })
    });
    $('.down-grade').click(function () {
        $.get(url.getGradexls,function () {
            Materialize.toast('成绩单下载成功', 4000);
        })
    });*/
    
})