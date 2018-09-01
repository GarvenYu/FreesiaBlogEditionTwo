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
	let submitBtn = $('#submit-btn');
	let commentText = $("#comment-content");
	let commentUser = $("#comment-name");
    submitBtn.hover(
      function(){
        $(this).css({"background-color":"#00962b","color":"#fff"});
      },
      function(){
        $(this).css({"background-color":"#16ac3a","color":"#fff"});
      }
    );
    submitBtn.on("click", function () {
        //点击提交评论按钮
        let content = $.trim(commentText.val());
        let name = $.trim(commentUser.val());
        if(content === "" || name === ""){
            alert("内容或姓名不能为空。");
        }else{
            $.post("/saveMessage",
                {
                    user_name: name,
                    message_content : content
                }, function (data, status) {
                    alert(data);
                    commentText.val("");
                    commentUser.val("");
                    //刷新评论
                    $('#show-all-messages').showMessages({
                    });
                });
        }
    });
    commentText.focus(function(){
      $(this).css({"border":"1px solid #87CEFF"});
    });
    commentText.blur(function(){
      $(this).css("border","1px solid #d9d9d9");
    });
    $('#show-all-messages').showMessages({
    });
});