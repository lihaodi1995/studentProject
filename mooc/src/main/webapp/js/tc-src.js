/**
 * Created by lynn on 2017/7/1.
 */
$(function () {

    var url = {
        tmapp: "/api/tc-getG",
        tminfo: "/api/tc-getAcc",
        tmdel: "/api/tc-delG",
        uploadsrc: "/mooc/api/tc-up-src"
    };

    $('.src-del').click(function () {
        $("[name='checkbox']").each(function () {
            if ($(this).prop('checked')) {
                $(this).parents('li').css('display', 'none');
            }
        });
    });

    $('.downloasrc').on('click', function () {
        Materialize.toast('成功下载', 4000);
    })
    $('.src-publicdg').click(function () {
        var header = $('#srcheadlinedg').val();
        var content = $('#srccontentdg').val();
        var params={
            name:header,
            content:content,
            files:fd
        };


        if (header && content) {

            // xhr = new XMLHttpRequest();
            // xhr.open("post", url.uploadsrc, true);
            // xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            // xhr.send(fd);
            fd.append('header',header);
            fd.append('content',content);
            $.ajax({
                url: url.uploadsrc,
                type: "POST",
                data: fd,
                /**
                 *必须false才会自动加上正确的Content-Type
                 */
                contentType: false,
                /**
                 * 必须false才会避开jQuery对 formdata 的默认处理
                 * XMLHttpRequest会对 formdata 进行正确的处理
                 */
                processData: false,
                success: function (data) {
                    if (data.status == "true") {
                        Materialize.toast('上传成功', 4000);
                    }
                    if (data.status == "error") {
                        alert(data.msg);
                    }
                    //$("#imgWait").hide();
                    fd = new FormData();
                    var headerhtml = '<li> <div class="collapsible-header"> <div class="col s1 m1 selectDown"> <form> <p> <input type="checkbox" name="checkbox" class="filled-in" id="src4"> <label for="src4"></label> </p> </form> </div> <i class="material-icons">filter_drama</i>';
                    var middlehtml = '<i class="material-icons text-black right">play_for_work</i> </div> <div class="collapsible-body"> <span>';
                    var footerhtml = '</span> </div> </li>';

                    $('.show-src').append(headerhtml + header + middlehtml + content + footerhtml);
                },
                error: function () {
                    Materialize.toast('上传失败', 4000);
                    //$("#imgWait").hide();
                }

            });
        }
        else {
            Materialize.toast('请输入完整的标题和说明文字', 4000);
        }
        fd=new FormData();
    })


//拖拽上传
    $(document).on({
        dragleave: function (e) { //拖离
            e.preventDefault();
            $('.drag-box').removeClass('over');
        },
        drop: function (e) { //拖后放
            e.preventDefault();
        },
        dragenter: function (e) { //拖进
            e.preventDefault();
            $('.drag-box').addClass('over');
        },
        dragover: function (e) { //拖来拖去
            e.preventDefault();
            $('.drag-box').addClass('over');
        }
    });

    var box = document.getElementById('drag-box');

    var fd = new FormData();

    box.addEventListener("drop", function (e) {
        e.preventDefault(); //取消默认浏览器拖拽效果

        var fileList = e.dataTransfer.files; //获取文件对象
        //fileList.length 用来获取文件的长度（其实是获得文件数量）
        //检测是否是拖拽文件到页面的操作
        if (fileList.length == 0) {
            $('.drag-box').removeClass('over');
            return;
        }


        for (var i = 0; i < fileList.length; i++) {
            fd.append('files', fileList[i]);
        }

    }, false);


})