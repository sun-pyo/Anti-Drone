
if (!!window.EventSource) {
  var source = new EventSource("/drone_num");
  source.onmessage = function (e) {
    var jbSplit = e.data.split(",");
    for (var i in jbSplit) {
      $("#cam" + i).text(jbSplit[i]);
      var time = new Date();
      var D = 'Date: ' + time.getFullYear() + '-' + (time.getMonth()+1)+ '-' + time.getDate() + ' ' + time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds();
      $("#timedate").text(D)
      var j = jbSplit[i].split(":");
      parseInt(j[1]);
      if (j[1] != 0) {
        var img = document.getElementById("video" + i);
        img.style.borderColor = "#ffff00";
      } else {
        var img = document.getElementById("video" + i);
        img.style.borderColor = "#ffffff";
      }
    }
  };
}


$(document).ready(function (e){

  $(document).on("click",".cam_video",function(){
          var scrollTop = $(window).scrollTop();
          //$('html').scrollTop(1200);      // 스크롤 위로
          $(".bigPictureWrapper").css('top', scrollTop);
          //$('html').animate({scrollTop : offset.top}, 2400);
          $("body").css("overflow", "hidden");  // 스크롤 숨기기
          var path = $(this).attr('src')
          var c = $(this).attr('class')
          var cam = c.split(' ')[1]
          showImage(path, cam)

          
          window.onkeydown = function(){
            if(event.keyCode == 13){           //엔터키
              $.ajax({
                url:'/send_img'
              });
            }
            else if(event.keyCode == 37){      //좌
              $.ajax({
                url:'/L/'+ cam
              });
            }
            else if(event.keyCode == 38){      //상
              $.ajax({
                url:'/U/'+ cam
              });
            }
            else if(event.keyCode == 39){      //우
              $.ajax({
                url:'/R/'+ cam
              });
            }
            else if(event.keyCode == 40){      //하
              $.ajax({
                url:'/D/'+ cam
              });
            }
            else if(event.keyCode == 32){      //스페이스바
              $.ajax({
                url:'/C/'+ cam
              });
            }
          }
          window.onkeyup = function(){
            event.keyCode = 9;
          }
          
    });//end click event
      
  function showImage(fileCallPath, cam){
      $(".bigPictureWrapper").css("display","flex").show();
      $(".bigPicture")
      .html("<img src='"+fileCallPath+"' >");
  }
      
  $(".bigPicture").on("click", function(e){
      $("body").css("overflow", "scroll");
      setTimeout(function(){
      $('.bigPictureWrapper').hide();
      }, 0);
  });//end bigWrapperClick event

  var check = $("input[type='checkbox']");
  check.click(function(){
    $.ajax({
      url: "/mode_change",
      //async: true
    });
    $(".Auto_text").toggle();
  });
  
});
