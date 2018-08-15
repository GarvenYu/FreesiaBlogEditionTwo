/**
* 留言板js
*/
$(function(){
	$("i.fa-angle-double-down").click(function(){
		if($(this).hasClass("fa-angle-double-down")){
          $(this).removeClass("fa-angle-double-down")
          .addClass("fa-angle-double-up")
          .next()
          .text("收起");          
		}else{
		  $(this).removeClass("fa-angle-double-up")
		  .addClass("fa-angle-double-down")
		  .next()
		  .text("展开");
		}
		$("#div2").toggle(800);
    });
    $(".message-block-button").hover(
    	function(){
    		$(this).css({"background-color":"#00B38F","color":"white"});
    	},
    	function(){
    		$(this).css({"background-color":"white","color":"#00B38F"});
    	}
    );
    $(".verify-btn").hover(
      function(){
        $(this).css({"background-color":"#00B38F","color":"white"});
      },
      function(){
        $(this).css({"background-color":"white","color":"#00B38F"});
      }
    );  
    $("i.fa-comment").click(function(){
    	
    });
    $('#mpanel1').codeVerify({
    //常规验证码type=1， 运算验证码type=2
    type : 1,
    //验证码宽度
    width : '400px',
    //验证码高度
    height : '50px',
    codeLength : 4,
    //提交按钮的id名称
    btnId : 'check-btn',
    //验证成功以后的回调
    success : function() {
        let values = {};
        values["user_name"] = $("#user_name_input").val();
        values["message_content"] = $("#message_content").val();
        let data = JSON.stringify(values);
        $.ajax({
            type : 'post',
            url : 'saveMessage',
            dataType : 'json',
            data : data,
            cache : false,
            success : function(data){
                alert(data.msg);
            }
        });
    },
    //验证错误以后的回调
    error : function(){
      alert('验证码错误！');
    },
    });
});