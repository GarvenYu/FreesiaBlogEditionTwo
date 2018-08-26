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
    $(".submit-btn").hover(
      function(){
        $(this).css({"background-color":"#00962b","color":"#fff"});
      },
      function(){
        $(this).css({"background-color":"#16ac3a","color":"#fff"});
      }
    );
    $("textarea").focus(function(){
      $(this).css({"border":"1px solid #87CEFF"});
    });
    $("textarea").blur(function(){
      $(this).css("border","1px solid #d9d9d9");
    });
    $('#show-all-messages').showMessages({
        commentList: [{'user_name':"qwer",'msg_content':"dddd",'msg_time':"2018-08-19 22:28:35"}
        ,{'user_name':"qwer",'msg_content':"dddd",'msg_time':"2018-08-19 22:28:35"}]
    });
});