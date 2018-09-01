/*
* 展示所有留言及回复
* ykbpro@whut.edu.cn
* 2018-8-22 21:17:23
* */
;(function ($, window, document, undefined) {
    const Message = function (ele, opt) {
        this.$element = ele;
        this.defaults = {
            parentNode : $('#show-all-messages'), //评论区容器
            commentList : [] //所有评论封装的json数组
        };
        this.options = $.extend({}, this.defaults, opt);
    };
    const fn = Message.prototype;
    fn.init = function () {
        this.initNode(); //初始化评论区DOM节点
        this.options.parentNode.html(this.body); //节点放入容器中
        this.showList(this.options.commentList); //显示评论
    };
    fn.initNode = function () {
        //初始化动作
        this.body = (function () {
           let html = '<div class="m-comment">' +
                          '<div class="cmt-content">' +
                              '<div class="no-cmt">暂时没有评论</div>' +
                              '<ul class="cmt-list"></ul>' +
                          '</div>' +
                      '</div>';
           return $(html)
        })();
        this.commentListUl = this.body.find(".cmt-list").eq(0); //评论列表容器
        this.noCommentAreaDiv = this.body.find(".no-cmt").eq(0); //无评论时容器
    };
    fn.initEvent = function () {
        this.commentListUl.on('click', this.reply.bind(this));
        this.commentListUl.find(".reply-button").on("mouseenter", function () {
           $(this).css({"background-color":"#16ac3a","color":"#fff"});
        });
        this.commentListUl.find(".reply-button").on("mouseleave", function () {
           $(this).css({"background-color":"#fff","color":"#16ac3a"});
        });
    };
    fn.reply = function (event) {
        //点击回复触发的函数
        let element = $(event.target);
        if(element.hasClass("reply-button")){
            //点击回复
            let showOrder = element.attr("show-order");
            $('.cmt-list-reply-all').eq(showOrder).toggle(500);
        }else if(element.hasClass("submit-reply-btn")){
            //点击提交回复
            let messageId = element.attr("message-id"); // 评论Id
            let replyUser = element.prev().find("input").val();
            let replyContent = element.siblings("textarea").val();
            if(replyUser === "" || replyContent === ""){
                alert("内容或姓名不能为空。");
            }else{
                //存储回复
                $.post("/saveReply",
                {
                    user_name: replyUser,
                    reply_content : replyContent,
                    message_id : messageId
                }, function (data, status) {
                    alert(data.message);
                    element.prev().find("input").val("");
                    element.siblings("textarea").val("");
                    //刷新评论
                    $('#show-all-messages').showMessages({
                    });
                });
            }
        }
    };
    fn.showList = function () {
        let self = this;
        let commentHtml = "";
        //构造异步请求
        $.ajax({
            type : 'post',
            url : 'getMessage',
            dataType : 'json',
            cache : false,
            success : function(result){
                //alert(result.data);
                let commentList = result;
                for(let i=0;i<commentList.length;i++){
                    //处理每条评论
                    let comment = commentList[i];
                    self.options.commentList.push(comment);
                    let replyHtml = "";
                    $.each(comment.replies, function (index, value) {
                        replyHtml+='<div class="cmt-list-reply-father">' +
                                        '<div class="cmt-list-reply-child">' +
                                            '<span class="comment-name">'+value.user_name+'</span> ' +
                                            '<span class="comment-time">'+value.reply_time+'</span>' +
                                            '<div class="reply-content">' +
                                                '<span>'+value.reply_content+'</span>'+
                                            '</div>'+
                                        '</div>' +
                                    '</div>';
                    });
                    replyHtml +=
                            '<div class="comment-textarea" style="float: left">'+
                              '<textarea placeholder="想回复什么？" maxlength="200" message-id="'+comment.id+'"></textarea>'+
                                '<div class="input-group">'+
                                  '<span class="input-group-addon" id="basic-addon1"><i class="far fa-user"></i></span>'+
                                  '<input type="text" class="form-control" placeholder="昵称" ' +
                                        'aria-describedby="basic-addon1" style="width: 20%" message-id="'+comment.id+'">'+
                                '</div>'+
                                '<a class="submit-reply-btn" message-id="'+comment.id+'">提交回复</a>'+
                            '</div> '
                    ;
                    commentHtml+='<li class="cmt-list-li">'+
                                    '<div class="head-img g-col-1">' +
                                        '<img src="../static/images/photo.png"/>' +
                                    '</div>' +
                                    '<div class="content g-col-18">' +
                                        '<div class="f-clear">' +
                                            '<span class="comment-name">'+comment.user_name+'</span>' +
                                            '<span class="comment-time">'+comment.msg_time+'</span>' +
                                        '</div>' +
                                        '<div class="parent-comment">'+
                                            '<span>'+comment.msg_content+'</span>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="g-col-1 f-float-right">'+
                                        '<span class="reply-button" message-id="'+comment.id+'" show-order="'+i+'">回复</span>' +
                                    '</div>' +
                                    '</li>' + '<div class="cmt-list-reply-all">'+replyHtml+'</div>';
                }
                self.noCommentAreaDiv.css("display","none");
                self.commentListUl.append(commentHtml);
                //注册事件
                self.initEvent();
            }
        });
    };
    //插件接口
    $.fn.extend({
        showMessages : function(options, callbacks) {
            let message = new Message(this, options);
            message.init();
        },
    });
})(jQuery, window, document);