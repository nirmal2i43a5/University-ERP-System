  $("#div_id_course_category input:radio").click(function(){
    var course_category_id = $(this).val();
    
    $.ajax({
        url:" {% url 'attendance_app:fill_semester_select' %}",
        data:{'course_category':course_category_id},
        success:function(data){
            $("#id_semester").html(data);
        }
    })
})


$("#id_semester").change(function(){
  var semester_id = $(this).val();
  
  
  $.ajax({
      url:" {% url 'attendance_app:fill_section_select' %}",
      data:{'semester':semester_id},
      success:function(data){
          $("#id_section").html(data);
      }
  })
})


$("#id_semester").change(function(){
  var semester_id = $(this).val();
  var course_category_id = $('#id_course_category').val();
  
  
  $.ajax({
      url:" {% url 'attendance_app:fill_subject_select' %}",
      data:{'semester':semester_id,'course_category':course_category_id},
      success:function(data){
          $("#id_Subject").html(data);
      }
  })
})