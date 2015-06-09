$(document).ready(function(){
 var pathname = window.location.pathname;
  if (window.location.pathname == '/'){ var pathname = "";}
$("#awstats_hitcounter")
     .load(pathname + "/@@awstats_hitcounter_view",
        function(response, status, xhr){
             if ( status == "error" ) { /// 
                                 } else {
                              $("#awstats_hitcounter").prepend("<span class='awstats_hitcounter_text'>Hits: </span>");
                    }
           });

});
