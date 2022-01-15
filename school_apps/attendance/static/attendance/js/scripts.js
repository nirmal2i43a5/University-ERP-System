
      //--------------------------------------------------For auto select form fill-------------------------------

      $("#id_course_category").change(function(){
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
              $("#id_subject").html(data);
          }
      })
    })

//get search form based on course category

$('#id_course_category').change(function(){
  var course_category = $('#id_course_category option:selected').text()
  if(course_category ==  'A-Level'){
   $('#id_semester').removeAttr("hidden");
   $('#id_group').removeAttr("hidden");
   $('#id_subject').attr("hidden",true);
   $('#id_section').attr("hidden",true);
  }
  if(course_category ==  'Bachelor' || course_category ==  'Master'){
   $('#id_semester').removeAttr("hidden");
   $('#id_subject').removeAttr("hidden");
   $('#id_section').removeAttr("hidden");
   $('#id_group').attr("hidden",true);
  }
})