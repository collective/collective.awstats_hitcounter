$(document).ready(function(){
  $("#awstats_hitcounter").hide();
  var pathname = window.location.pathname;

  if (window.location.pathname == '/'){ var pathname = "";}
  $.getJSON( "awstats_hitcounter_view", function( data ) {

   if (data.success == 'true'){
 
    $( "<span/>", {
      "class": "creation-date",
      html: data.creation_date
    }).appendTo( "#awstats_hitcounter .date-created" );
    $( "<span/>", {
      "class": "modification-date",
      html: data.modification_date
    }).appendTo( "#awstats_hitcounter .date-modified" );
    $( "<span/>", {
      "class": "views-count-for-pages",
      html: data.page_views
    }).appendTo( "#awstats_hitcounter .page-views" );
    $("#awstats_hitcounter").show();

   }

  });
});
