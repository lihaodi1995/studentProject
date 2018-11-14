$(document).ready(function () {
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
});
$(function () {
    setTeamValue();
    getStuStatus();
})
$(function(){
	

$('.modal-content').on('click','.teamlist',function () {
    var _this = this;
//        $(_this).find('.hwContent').toggle('normal');
    if ($(_this).css('margin-bottom') == '8px') {
        $(_this).closest('.row').next().find('.teamContent').slideDown('normal');
        $(_this).css('margin-bottom', '0px');
        $(_this).next().css('margin-bottom', '0px');
    } else {
        $(_this).closest('.row').next().find('.teamContent').slideUp('normal');
        setTimeout(function () {
            $(_this).css('margin-bottom', '8px');
            $(_this).next().css('margin-bottom', '8px');
        }, 300);
    }
});
$('div').on('click','.find-team-apply',function () {
    var _this=this;
    var _teamName = $(_this).parent().parent().prev().find('.find-team-name').text();
    teamQuery.stuTA.data.teamName=_teamName;
    setStuTeamApply();
    if(0==teamRet.stuTA){
        getStuInfo();
        revealTeamCheck();
    }else{
        alert('请刷新页面然后重新提交申请');
    }
});
})
/*
$('.teamlist').click(function () {
    var _this = this;
//        $(_this).find('.hwContent').toggle('normal');
    if ($(_this).css('margin-bottom') == '8px') {
        $(_this).closest('.row').next().find('.teamContent').slideDown('normal');
        $(_this).css('margin-bottom', '0px');
        $(_this).next().css('margin-bottom', '0px');
    } else {
        $(_this).closest('.row').next().find('.teamContent').slideUp('normal');
        setTimeout(function () {
            $(_this).css('margin-bottom', '8px');
            $(_this).next().css('margin-bottom', '8px');
        }, 300);
    }
});*/

function revealTeamMng() {
    $('#create-team').modal('close');
    $('#team-choose').css('display', 'none');
    $('#team-manage').css('display', 'block');
}

function revealTeamCheck() {
    $('#find-team').modal('close');
    $('#team-choose').css('display', 'none');
    $('#team-check').css('display', 'block');
}

function revealTeamScore() {
    getTeamScore();
    $('#team-score').modal('open');
}

$('#team-manage-app').on('click','.agree',function () {
    var _this = this;
    var _li = $(_this).parent().parent();
    teamQuery.stuTMA.data.appStuID = $(_this).parent().find('.appStuID').text();
    teamQuery.stuTMA.data.approve = 0;
    teamManageApproval();
    if (0 == teamRet.stuTMA) {
        $(_this).parent().parent().slideUp('normal');
        setTimeout(function () {
            $(_li).find('div a').css('display', 'none');
            $('#team-manage-mem').append(_li);
            $(_li).slideDown('normal');
        }, 300);
    } else {
        alert('队员审批失败请重新申请');
    }
});
/*
$('.agree').click(function () {
    var _this = this;
    var _li = $(_this).parent().parent();
    teamQuery.stuTMA.data.appStuID = $(_this).parent().find('.appStuID').text();
    teamQuery.stuTMA.data.approve = 0;
    teamManageApproval();
    if (0 == teamRet.stuTMA) {
        $(_this).parent().parent().slideUp('normal');
        setTimeout(function () {
            $(_li).find('div a').css('display', 'none');
            $('#team-manage-mem').append(_li);
            $(_li).slideDown('normal');
        }, 300);
    } else {
        alert('队员审批失败请重新申请');
    }
});
*/
$('#team-manage-app').on('click','.disagree',function () {
    var _this = this;
    var _li = $(_this).parent().parent();
    teamQuery.stuTMA.data.appStuID = $(_this).parent().find('.appStuID').text();
    teamQuery.stuTMA.data.approve = 1;
    teamManageApproval();
    if (0 == teamRet.stuTMA) {
        $(_this).parent().parent().slideUp('normal');
    } else {
        alert('队员审批失败请重新申请');
    }
})
/*
$('.disagree').click(function () {
    var _this = this;
    var _li = $(_this).parent().parent();
    teamQuery.stuTMA.data.appStuID = $(_this).parent().find('.appStuID').text();
    teamQuery.stuTMA.data.approve = 1;
    teamManageApproval();
    if (0 == teamRet.stuTMA) {
        $(_this).parent().parent().slideUp('normal');
    } else {
        alert('队员审批失败请重新申请');
    }

});
*/
$('#find-team-confirm').click(function () {
    getStuTeamList();
});

/*
$('.find-team-apply').click(function () {
    var _this=this;
    var _teamName = $(_this).parent().parent().prev().find('.find-team-name').text();
    teamQuery.stuTA.data.teamName=_teamName;
    setStuTeamApply();
    if(0==teamRet.stuTA){
        getStuInfo();
        revealTeamCheck();
    }else{
        alert('请刷新页面然后重新提交申请');
    }

});
*/
function disableTeamApply() {
    $('#submit-team-apply').addClass('disabled').html('团队申请已提交');
}

var teamQuery = {
    stuTS: {
        url: 'stu-team-status',
        data: {
            stuID: ''
        }
    },
    stuTC: {
        url: 'stu-team-create',
        data: {
            teamName: '',
            teamInfo: '',
            stuID: ''
        }
    },
    stuTM: {
        url: 'stu-team-manage',
        data: {
            stuID: ''
        }
    },
    stuTI: {
        url: 'stu-team-info',
        data: {
            stuID: ''
        }
    },
    stuTL: {
        url: 'stu-team-list',
    },
    stuTA: {
        url: 'stu-team-apply',
        data: {
            stuID: '',
            teamName: '',
        }
    },
    stuTMA: {
        url: 'stu-team-manage-approval',
        data: {
            stuID: '',
            appStuID: '',
            approve: 0
        }
    },
    stuTMS: {
        url: 'stu-team-manage-submit',
        data: {
            stuID: '',
        }
    },
    stuTMC: {
        url: 'stu-team-manage-check',
        data: {
            stuID: '',
        }
    },
    stuTSL:{
        url:'stu-team-score-list',
        data: {
            stuID:'',
        }
    },
    stuTSS:{
        url:'stu-team-mem-score',
        data:{
            stuID:'',
            count:0,
            memList:[]
        }
    }
};
var teamRet = {
    stuTS: '',
    stuTC: '',
    stuTM: '',
    stuTI: '',
    stuTL: '',
    stuTA: '',
    stuTMA: '',
    stuTMS: '',
    stuTMC: '',
    stuTSL:'',
    stuTSL:'',
}

function setTeamValue() {
    var Id = $('#stuID').text();
    teamQuery.stuTA.data.stuID = Id;
    teamQuery.stuTC.data.stuID = Id;
    teamQuery.stuTS.data.stuID = Id;
    teamQuery.stuTM.data.stuID = Id;
    teamQuery.stuTI.data.stuID = Id;
    teamQuery.stuTMA.data.stuID = Id;
    teamQuery.stuTMC.data.stuID = Id;
    teamQuery.stuTMS.data.stuID = Id;
    teamQuery.stuTSL.data.stuID = Id;
    teamQuery.stuTSS.data.stuID = Id;

}

function getStuStatus() {//获取学生状态检查是否已经成为组长或组员
    $.get(teamQuery.stuTS.url, teamQuery.stuTS.data, function (json) {
        teamRet.stuTS = eval('(' + json + ')').status;
        if (1 == teamRet.stuTS) {
            getStuMng();
            revealTeamMng();
        } else if (2 == teamRet.stuTS) {
            getStuInfo();
            revealTeamCheck();
        }
    })
}

function getStuMng() {//组长管理界面信息获取
    $.get(teamQuery.stuTM.url, teamQuery.stuTM.data, function (json) {
        teamRet.stuTM = eval('(' + json + ')');
        $('#team-manage-name').text(teamRet.stuTM.teamName);
        $('#team-manage-info').text(teamRet.stuTM.teamInfo);
        var _AppCounter = teamRet.stuTM.appCounter;
        var _AppArr = teamRet.stuTM.memApp.arr;
        var _ListCounter = teamRet.stuTM.memCounter;
        var _ListArr = teamRet.stuTM.memList.arr;
        for (var p=0;p<_AppCounter;p++) {
            $('#team-manage-app').append(' <li class="collection-item"><div><span class="appStuName">' + _AppArr[p].name + '</span><span class="appStuID">' + _AppArr[p].appStuID + '</span><a class="secondary-content waves-effect waves-light red z-depth-1 disagree">不同意</a><a class="secondary-content waves-effect waves-light cyan z-depth-1 agree">同意</a></div></li>');
        }
        for (var p=0;p<_ListCounter;p++) {
            $('#team-manage-mem').append('<li class="collection-item"><span class="memName">' + _ListArr[p].name + '</span><span class="memStuID">' + _ListArr[p].memStuID + '</span></li>');
        }
    });
}

function getStuInfo() {//学生团队界面信息获取
    $.get(teamQuery.stuTI.url, teamQuery.stuTI.data, function (json) {
        teamRet.stuTI = eval('(' + json + ')');
        $('#team-check-name').text(teamRet.stuTI.teamName);
        $('#team-check-info').text(teamRet.stuTI.teamInfo);
        var _counter = teamRet.stuTI.memCounter;
        var _ListArr = teamRet.stuTI.memList.arr;
        for (var p =0;p<_counter;p++) {
            $('#team-check-mem').append('<li class="collection-item"><span class="memName">' + _ListArr[p].name + '</span><span class="memStuID">' + _ListArr[p].memStuID + '</span></li>');
        }
    });
    /*$.each(teamRet.stuTM.memList,function (i,item) {
        $('#team-check-mem').append('<li class="collection-item">'+item.name+'</li>')
    })*/
}


function getStuTeamList() {//组员报名团队时组信息获取
    $.get(teamQuery.stuTL.url,teamQuery.stuTL.data,function (json) {
        teamRet.stuTL=eval('('+json+')');
        var _TeamCounter = teamRet.stuTL.TeamCounter;
        var _TeamListArr = teamRet.stuTL.TeamListArr;
        var _prefixMemList = '                    <li class="collection-item">'
        var _suffixMemList = '</li>\n'
        var _tmpMemList = ''
        for (var p=0;p < _TeamCounter;p++){
            _tmpMemList = '';
            var memCounter = _TeamListArr[p].teamMemCounter;
            for(var i = 0; i<memCounter;i++){
                _tmpMemList =  _tmpMemList+_prefixMemList+_TeamListArr[p].teamMemArr[i].name+_suffixMemList;
            }
            $('#find-team .modal-content').append('        <div class="row find-team-list-div">\n' +
                '            <div class="col m12 valign-wrapper teamlist opacity z-depth-2">\n' +
                '                <span class="find-team-name">'+_TeamListArr[p].teamName+'</span><span>——'+_TeamListArr[p].teamCrter+'的团队</span>\n' +
                '            </div>\n' +
                '        </div>\n' +
                '        <div class="row">\n' +
                '            <div class="col m12 opacity teamContent z-depth-1 find-team-div">\n' +
                '                <h4>团队信息</h4>\n' +
                '                <p>'+_TeamListArr[p].teamInfo+'</p>\n' +
                '                <h4>队员信息</h4>\n' +
                '                <ul class="collection">\n' +
                                _tmpMemList +
                '                </ul>\n' +
                '                <a href="#" type="submit" class="find-team-apply cyan waves-effect waves-light btn">申请加入</a>\n' +
                '            </div>\n' +
                '        </div>');
        }
    });
}
function setStuTeamApply() {//提交学生加入团队申请
    $.post(teamQuery.stuTA.url, teamQuery.stuTA.data, function (json) {
        teamRet.stuTA = eval('(' + json + ')').status;
        //alert(teamRet.stuTA);

        /*if (0 == teamRet.stuTA) {
            getStuInfo();
            revealTeamCheck();
        } else {
            alert('请刷新页面然后重新提交申请');
        }*/
    });
}

function teamCreate() {//成立团队
    var _teamName = $('#teamname').val();
    var _teamInfo = $('#teaminfo').val();
    teamQuery.stuTC.data.teamName = _teamName;
    teamQuery.stuTC.data.teamInfo = _teamInfo;
    $.post(teamQuery.stuTC.url, teamQuery.stuTC.data, function (json) {
        teamRet.stuTC = eval('(' + json + ')').status;
        if (0 != status) {
            alert('团队建立失败 请重新创建团队');
        } else {
            $('#team-manage-name').text(_teamName);
            $('#team-manage-info').text(_teamInfo);
            revealTeamMng();
        }
    })
    /*
    TODO:下面那行需要删除
     */
    // revealTeamMng();
}

function teamManageApproval() {//管理学生加入团队申请
    $.post(teamQuery.stuTMA.url, teamQuery.stuTMA.data, function (json) {
        teamRet.stuTMA = eval('(' + json + ')').status;
    })
}

function teamManageSubmit() {//团队确认提交到老师
    $.post(teamQuery.stuTMS.url, teamQuery.stuTMS.data, function (json) {
        teamRet.stuTMS = eval('(' + json + ')').status;
        if (0 != teamRet.stuTMS) {
            alert('申请失败,请刷新后重新提交申请');
        } else {
            disableTeamApply();
        }
    });
}

function teamManegeCheck() {//待实现 查看团队是否已经提交申请
    $.get(teamQuery.stuTMC.url, teamQuery.stuTMC.data, function (json) {
        teamRet.stuTMC = eval('(' + json + ')');
        // if(1==)
    })
}

function getTeamScore() {
    $.get(teamQuery.stuTSL.url, teamQuery.stuTSL.data, function (json) {
        teamRet.stuTSL = eval('('+json+')');
        var _counter = teamRet.stuTSL.counter;
        var _arr = teamRet.stuTSL.Arr;
        for( var p = 0;p<_counter;p++){
            $('#team-score-list').append('<li class="collection-item row"><span class="teamScoreName col m2">'+_arr[p].Name+'</span><span class="teamScoreID col m2">'+_arr[p].memID+'</span> <input class="teamScoreScore col m3" type="range" min="0.4" max="1.2" step="0.2" value="1"><div class="blankspace col m5"></div></li>');
        }

    })
}

function setTeamScore(){
    var sum=0;
    var counter=0;
    $('#team-score-list').find('input').each(function () {
        sum+=parseFloat($(this).val());
        counter++;
    });
    teamQuery.stuTSS.data.count=counter;
    // $('#team-score-list').css('background-color','#6cf');
    // $('#team-score-list').find('input').css('background-color','red');
    // alert($('#team-score-list').find('input').val());
    // alert(sum);
    if(sum!=counter){
        alert('分数之和不符合要求,请重新打分');
    }else{
        $('#team-score-list').find('input').each(function () {
            //TODO:FIX
            teamQuery.stuTSS.data.memList.push({"memID":$(this).prev().text(),"Score":$(this).val()});
        });
        $.get(teamQuery.stuTSS.url,teamQuery.stuTSS.data,function (json) {
            teamRet.stuTSS = eval('('+json+')').status;
            if(0==teamRet.stuTSS){
                alert("打分成功！")
                getTeamScore();
                $('#team-score').modal('close');
            }else{
                alert("提交失败,请重新提交");
            }
        })

    }
}
/*
$('#set-team-score-btn').click(function () {
    var _this=this;
    $(_this).parent().addClass("a");
    $(_this).parent().find('#team-score-list').addClass("a");
    $(_this).parent().find('#team-score-list').find('input').addClass('b');
    $(_this).parent().find('#team-score-list').find('input').each(function () {
        alert(1);
    })
})
*/