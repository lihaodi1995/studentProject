$(document).ready(function () {

    $("#btn_delete").click(function () {
        var $table = $('#table');
        alert('getSelections: ' + JSON.stringify($table.bootstrapTable('getSelections')));
    })

    $("#close-modal-temp").click(function () {

        $("#templates-table").empty();
        $("#CreateVMModal").modal("hide");
    })

    $("#vm-create-submit").click(function () {
        var radionum = document.getElementsByName("MO_ID")
        var checkedradio;
        for (var i = 0; i < radionum.length; i++) {
            if (radionum[i].checked) {
                checkedradio = radionum[i];
                break;
            }
        }
        var name = ["MO_ID", "MO_NAME", "DiskByGB",
                "MemoryByMb", "CPUByNum", "OS", "Remark", "VM_NAME"];

        var j = 0;
        var tr = checkedradio.parentNode.parentNode;
        var tds = tr.cells;
        var temdata = new Array(tds.length - 1);
        for (var i = 1 ; i < tds.length - 1 ; i++) {
            //  alert(tds[i].innerHTML);
            //  var tem = tds[i].value;
            temdata[j++] = tds[i].innerHTML;
        }
        //  alert(temdata[2]);
        // alert($("#vm-create-name").val());
        // alert($("#vm-create-remark").val());
        var data = {
            "VM_NAME": $("#vm-create-name").val(),
            "MO_ID": temdata[0],
            "MO_NAME": temdata[1],
            "DiskByGB": temdata[2],
            "MemoryByMb": temdata[3],
            "CPUByNum": temdata[4],
            "OS": temdata[5],
            "Remark": $("#vm-create-remark").val()
        }
        $.post("/VirtualMachine/DoCreate", data, function (data, status) {
            if (data == true) {
                alert("创建完成");
            }
        });
    });

    $("#btn_add").click(function () {
        $.get("/VirtualMachine/Create", null, function (data, status) {
            console.log(data);
            var myData = JSON.parse(data);
            var length = myData.length;
            //alert(length);
            var mytable = document.getElementById("templates-table");
            var myFirstTr = document.createElement("tr");
            //加上table的列
            var myFirstTh = ["选择", "模板ID", "模板名称", "磁盘(GB)",
                "内存(MB)", "CPU个数", "操作系统名称", "备注"];

            for (var i = 0 ; i < 8; i++) {
                var td = document.createElement("td");
                td.innerHTML = myFirstTh[i];
                myFirstTr.appendChild(td);
            }
            mytable.appendChild(myFirstTr);


            for (var i = 0; i < length; i++) {
                var tr = document.createElement("tr");
                var firsttd = document.createElement("td");
                var input = document.createElement("input");
                input.type = "radio";
                input.name = "MO_ID";
                firsttd.appendChild(input);
                tr.appendChild(firsttd);
                // alert(myData[i]);
                for (var item in myData[i]) {
                    if (item != "__type") {
                        var td = document.createElement("td");
                        td.innerHTML = myData[i][item];
                        tr.appendChild(td);
                    }
                }

                mytable.appendChild(tr);
            }
        })

        $("#CreateVMModal").modal('show');
    })

})