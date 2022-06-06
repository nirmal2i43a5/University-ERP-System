$(document).ready(function() {
 
    $('#notification').on("click",function(){
      $("#notification_count").hide();
      console.log('clicked');
      $.ajax({
              type: "GET",
              url: "{% url 'notifications:update_notification' %}",
              dataType: 'json',
              success: function(response){
                console.log(response)
                $("#notification_count").html("");
              },error:function(response){
                  return false;
              }
          });
  });   
  });
