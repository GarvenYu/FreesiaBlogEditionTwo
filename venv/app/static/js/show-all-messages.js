/*
* 展示所有留言及回复
* ykbpro@whut.edu.cn
* 2018-8-22 21:17:23
* */
;(function ($, window, document, undefined) {
    const Message = function (ele, opt) {
        this.$element = ele;
        this.defaults = {
            parentNode : $('#show-all-messages')
        };
        this.options = $.extend({}, this.defaults, opt);
        this.init(this.options);
    };
    const fn = Message.prototype;
    fn.init = function (options) {
        //初始化动作

    };
    //插件接口
    $.fn.showMessages = function(options, callbacks) {
        let message = new Message(this, options);
    };
})(jQuery, window, document);