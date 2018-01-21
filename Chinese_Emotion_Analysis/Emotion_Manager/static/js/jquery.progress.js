/* jQuery Progress Bar Plugin - v1.0.0
 * Copyright (c) 2015 Zeyu Feng; Licensed MIT
 * https://github.com/clarkfbar/jquery.progress
 * */

$.fn.extend({
  Progress: function(options){
    var settings = {
      width: 90, // 进度条宽度
      height: 20, // 进度条高度
      percent: 0, // 当前占比
      backgroundColor: '#60AEFD', // 进度条背景颜色
      barColor: '#FD6B27', // 进度条颜色
      fontColor: '#fff', // 百分比字体颜色
      radius: 4, // 边角圆度
      fontSize: 12, // 字体大小
      increaseTime: 1000.00/60.00, // 每一次调整进度条的时间, 默认最佳时间(可以调大，不要调小)；只有在animate为true的情况下有效
      increaseSpeed: 1, // 每次调整，增长速度；只有在animate为true的情况下有效
      animate: true // 调整的时候，是否使用动画增长，默认为true
    };
    $.extend(settings, options);

    var $svg = $(this), $background, $bar, $g, $text, timeout;

    function progressPercent(p){
      if(!$.isNumeric(p) || p < 0) {
        return 0;
      } else if(p > 100) {
        return 100;
      } else {
        return p;
      }
    }

    // 动画相关方法
    var Animate = {
      getWidth: function(){
        // 获取当前的宽度，根据总宽度和percent
        return settings.width * settings.percent / 100.00;
      },
      getPercent: function(currentWidth){
        // 根据当前的宽度，计算当前的percent
        return parseInt((100 * currentWidth / settings.width).toFixed(2));
      },
      animateWidth: function(currentWidth, targetWidth){
        // 动画增长
        timeout = setTimeout(function(){
          if(currentWidth > targetWidth) {
            if(currentWidth - settings.increaseSpeed <= targetWidth) {
              currentWidth = targetWidth;
            } else {
              currentWidth = currentWidth - settings.increaseSpeed;
            }
          } else if(currentWidth < targetWidth) {
            if(currentWidth + settings.increaseSpeed >= targetWidth) {
              currentWidth = targetWidth;
            } else {
              currentWidth = currentWidth + settings.increaseSpeed;
            }
          }

          $bar.attr("width", currentWidth);
          $text.empty().append(Animate.getPercent(currentWidth) + "%");

          if(currentWidth != targetWidth) {
            Animate.animateWidth(currentWidth, targetWidth);
          }
        }, settings.increaseTime);
      }
    }

    function svg(tag){
      return document.createElementNS("http://www.w3.org/2000/svg", tag);
    }

    // 初始化条件
    !!function(){
      settings.percent = progressPercent(settings.percent);

      $svg.attr({'width': settings.width, 'height': settings.height * 4});

      $background = $(svg("rect")).appendTo($svg)
                      .attr({x: 0, rx: settings.radius, width: settings.width, height: settings.height, fill: settings.backgroundColor});

      $bar = $(svg("rect")).appendTo($svg)
                .attr({x: 0, rx: settings.radius, height: settings.height, fill: settings.barColor});

      $g = $(svg("g")).appendTo($svg)
                .attr({"fill": "#fff", "text-anchor": "middle", "font-family": "DejaVu Sans,Verdana,Geneva,sans-serif", "font-size": settings.fontSize});

      $text = $(svg("text")).appendTo($g)
                .attr({"x": settings.width/2.0, "y": settings.height * 1.8 + settings.fontSize/3.0, fill: settings.fontColor});

      draw();
    }();

    // 绘制进度条
    function draw() {
      var targetWidth = Animate.getWidth();

      // 是否使用动画增长
      if(settings.animate) {
        if(timeout) {
          clearTimeout(timeout);
        }
        var currentWidth = parseFloat($bar.attr("width"));
        if(!currentWidth) currentWidth = 0;

        Animate.animateWidth(currentWidth, targetWidth);
      } else {
        $bar.attr("width", targetWidth);
        $text.empty().append(settings.percent + "%");
      }
    }

    this.percent = function (p) {
      if(p) {
        p = progressPercent(p);

        settings.percent = p;
        draw();
      }
      return settings.percent;
    }

    return this;
  }
});
