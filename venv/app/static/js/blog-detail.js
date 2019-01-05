/**
* 留言板js
*/
$(function(){
	$("div.wb-btn").click(function(){
        var _shareUrl = 'http://v.t.sina.com.cn/share/share.php?&appkey=331103139';     //真实的appkey，必选参数
        _shareUrl += '&url='+ encodeURIComponent(document.location);     //参数url设置分享的内容链接|默认当前页location，可选参数
        _shareUrl += '&title=' + encodeURIComponent(document.title+" by @FreesiaAABBCC");    //参数title设置分享的标题|默认当前页标题，可选参数
        _shareUrl += '&source=' + encodeURIComponent('');
        _shareUrl += '&sourceUrl=' + encodeURIComponent('');
        _shareUrl += '&content=' + 'utf-8';   //参数content设置页面编码gb2312|utf-8，可选参数
        _shareUrl += '&pic=' + encodeURIComponent('');  //参数pic设置图片链接|默认为空，可选参数
        window.open(_shareUrl,'_blank');
    });
});