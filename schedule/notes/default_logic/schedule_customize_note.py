I am using calendar_base_test.html for ohter fields like yearly, tri month.so include this base to the .html tag which is not fully customisze but that u only want to test

EXTRA IDEAS:
--------------
https: // gitter.im / llazzaro / django - scheduler


1) ADD AND CUSTOMIZE BUTTON FOR DIFFERENT DAYS VIEWS
- ----------------------------------------------

    header: {
            left: 'prev,next today',
            center: 'title',
            # similarly i can add other button for this view
            right: 'month,agendaWeek,agendaDay,agendaThreeDay,listWeek'
        },
    
    
    
       views: {#in this way i can give button name for various button name
           
        agendaThreeDay: {#this should same as it is decalared above
          type: 'agenda',
          duration: { days: 3 },#change this according to days u want to populate
          buttonText: 'Three Days'
        },
        defaultView: 'agendaThreeDay'
      },

2)https://fullcalendar.io/docs  #use this to customize calendar design
3)try this for list button agenda https://fullcalendar.io/docs/v3/listDayAltFormat
4)TRY THIS https://www.youtube.com/watch?v=NiTLuPqvt58
5)WHEN I SELECT THEN I WILL SHOW ADD EVENT FORM IN THE FUTURE AS IN 4 VIDEOS
6)this timeline does not work https://jsfiddle.net/jvddrift/8jndrp7m/2/ and also https://codepen.io/acerix/pen/ejQRea?editors=1010
7)datepicker in top center https://github.com/fullcalendar/fullcalendar/issues/

8)EVENT CLICK LOGIC

  eventClick: function(event) {
          
            if (event.title) {
                alert(event.title);
            }
        }
  
  
  check this for day and event js click
  
-----------------------------------
https://stackoverflow.com/questions/29072645/fullcalendar-open-bootstrap-modal-on-dayclick