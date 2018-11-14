$(function () {
    $('.edit').css('display','none');
    $('.edit-button').css('display','none');
    $('#course-date-start-edit').pickadate({
        selectMonths: true,
        selectYears:1
    })
    $('#course-date-end-edit').pickadate({
        selectMonths: true,
        selectYears:1
    })
})
$('#course-edit').click(function () {

    /*修改表单预设值*/
    $('#course-name-edit').attr('placeholder',$('#course-name').text());
    $('#course-info-edit').attr('placeholder',$('#course-info').text());
    $('#course-teacher-edit').attr('placeholder',$('#course-teacher').text());
    $('#course-place-edit').attr('placeholder',$('#course-place').text());
    $('#course-score-edit').attr('placeholder',$('#course-score').text());

    $('.edit').css('display','block');
    $('.edit-button').css('display','inline');
    $('.origin-info').css('display','none');
});
$('#course-cancel').click(function () {
    $('.edit').css('display','none');
    $('.edit-button').css('display','none');
    $('.origin-info').css('display','inline');
})
$('#course-save').click(function () {
    $('.edit').css('display','none');
    $('.edit-button').css('display','none');
    $('.origin-info').css('display','inline');
    var data= {
        name: $('#course-name-edit').val(),
        info: $('#course-info-edit').val(),
        teacher: $('#course-teacher-edit').val(),
        place: $('#course-place-edit').val(),
        score: $('#course-score-edit').val(),
        dateSt: $('#course-date-start-edit').val(),
        dateEd: $('#course-date-end-edit').val(),
    };
    var _url='dn-course-save';
    /*$.post(_url,data,function (json) {
        var ret = eval('('+json+')').status;
        if(0==ret){
            window.location.reload();
        }else{
            alert(保存失败,请重新保存);
        }
    })*/
})

$('#course-save').click(function (){
	
	var name = $('#course-name').html();
	var info = $('#course-info').html(); 
	var teacher = $('#course-teacher').html(); 
	var place = $('#course-place').html();
	var score = $('#course-score').html();
	var people = $('#course-people').html();
	var start = $('#course-date-start').html();
	var end = $('#course-date-end').html();
	
	if($('#course-name-edit').val() != "")
		name = $('#course-name-edit').val();
	if($('#course-info-edit').val() != "")
		info = $('#course-info-edit').val();
	if($('#course-teacher-edit').val() != "")
		teacher = $('#course-teacher-edit').val();
	if($('#course-place-edit').val() != "")
		place = $('#course-place-edit').val();
	if($('#course-score-edit').val() != "")
		score = $('#course-score-edit').val();
	if($('#course-date-start-edit').val() != "")
		start = $('#course-date-start-edit').val();
	if($('#course-date-end-edit').val() != "")
		end = $('#course-date-end-edit').val();
	if($('#course-people-edit').val() != "")
		people = $('#course-people-edit').val();
		
	$('#course-name').html(name);
	$('#course-info').html(info); 
	$('#course-teacher').html(teacher); 
	$('#course-place').html(place);
	$('#course-score').html(score);
	$('#course-people').html(people);
	$('#course-date-start').html(start);
	$('#course-date-end').html(end);
	
	var course = {'name': name, 'info': info, 'teacher': teacher, 'place': place, 'score': score, 'people': people, 'start': start, 'end': end};
	
	$.ajax({
	
		type:'POST',
		
		data:JSON.stringify(course),
		
		contentType: "application/json; charset=utf-8", 
		dataType:'json',
		
		url :'/mooc/courseInfo',
			
		success :function(data) {
			
			//alert("OK");
		
		}		
	});
	
	alert("课程信息修改成功！");
});
