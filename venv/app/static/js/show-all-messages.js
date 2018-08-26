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
        if(this.options.commentList.length>0){
            this.showList(this.options.commentList); //显示评论
        }
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
    fn.showList = function (commentList) {
        let commentHtml = "";
        for(let i=0;i<commentList.length;i++){
            //处理每条评论
            let comment = commentList[i];
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
                                '<sapn class="reply-button">回复</span>' +
                            '</div>' +
                            '</li>'
        }
        this.noCommentAreaDiv.css("display","none");
        this.commentListUl.html(commentHtml);
    };
    //插件接口
    $.fn.showMessages = function(options, callbacks) {
        let message = new Message(this, options);
        message.init();
    };
})(jQuery, window, document);