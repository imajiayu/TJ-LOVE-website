/*
* jquery.counterup.js 1.0
*
* Copyright 2013, Benjamin Intal http://gambit.ph @bfintal
* Released under the GPL v2 License
*
* Date: Nov 26, 2013
*/
(function(a){a.fn.counterUp=function(b){var c=a.extend({time:400,delay:10},b);return this.each(function(){var e=a(this);var d=c;var f=function(){var q=[];var h=d.time/d.delay;var p=e.text();var l=/[0-9]+,[0-9]+/.test(p);p=p.replace(/,/g,"");var n=/^[0-9]+$/.test(p);var m=/^[0-9]+\.[0-9]+$/.test(p);var g=m?(p.split(".")[1]||[]).length:0;for(var k=h;k>=1;k--){var o=parseInt(p/h*k);if(m){o=parseFloat(p/h*k).toFixed(g)}if(l){while(/(\d+)(\d{3})/.test(o.toString())){o=o.toString().replace(/(\d+)(\d{3})/,"$1,$2")}}q.unshift(o)}e.data("counterup-nums",q);e.text("0");var j=function(){e.text(e.data("counterup-nums").shift());if(e.data("counterup-nums").length){setTimeout(e.data("counterup-func"),d.delay)}else{delete e.data("counterup-nums");e.data("counterup-nums",null);e.data("counterup-func",null)}};e.data("counterup-func",j);setTimeout(e.data("counterup-func"),d.delay)};e.waypoint(f,{offset:"100%",triggerOnce:true})})}})(jQuery);