
if (!!window.EventSource) {
  var source = new EventSource("/drone_num");
  source.onmessage = function (e) {
    var jbSplit = e.data.split(",");
    var total_dnum = 0;
    var time = new Date();
    var D = 'Date: ' + time.getFullYear() + '-' + (time.getMonth()+1)+ '-' + time.getDate() + ' ' + time.getHours() + ':' + time.getMinutes() + ':' + time.getSeconds();
    $("#timedate").text(D)
    for (var i in jbSplit) {
      $("#cam" + i).text(jbSplit[i]);
      var j = jbSplit[i].split(":");
      var k = parseInt(j[1]);
      if (k != 0) {
        total_dnum += k;
        var img = document.getElementById("video" + i);
        img.style.borderColor = "#ffff00";
      } else {
        var img = document.getElementById("video" + i);
        img.style.borderColor = "#ffffff";
      }  
    }
    // if(total_dnum != 0)
    // {
    //   var audio = new Audio("../alert_sound.mp3");
    //   audio.play();    
    // }

    //if(total_dnum == 0){
    //     Warning.pause();
    //     Warning.loop = true;
    // }
    // else
    //     Warning.play();
      
  };
}

window.onload=function(){
    $("#video0").attr('src', '/video_feed/1');
    $("#video1").attr('src', '/video_feed/2');
    $("#video2").attr('src', '/video_feed/3');
    $("#video3").attr('src', '/video_feed/4');
  }


$(document).ready(function (e){
  $(document).on("click",".cam_video",function(){
          var scrollTop = $(window).scrollTop();
          //$('html').scrollTop(1200);      // 스크롤 위로
          $(".bigPictureWrapper").css('top', scrollTop);
          //$('html').animate({scrollTop : offset.top}, 2400);
          $("body").css("overflow", "hidden");  // 스크롤 숨기기
          var path = $(this).attr('src');
          var c = $(this).attr('class');
          var cam = c.split(' ')[1];
          showImage(path, cam);

          
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
      $(".bigPicture").html("<img src='"+fileCallPath+"' >");
      var radar= '/Radar_map'
      $("#radar").html("<img src='"+radar+"' >");
    }
      
  $(".bigPicture").on("click", function(e){
      //$('#radar').removeAttr('src');
      //$("#radar").empty();
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
