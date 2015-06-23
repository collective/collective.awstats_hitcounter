$(document).ready(function(){
  function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
  }
  $("#awstats_hitcounter").hide();
  var pathname = window.location.pathname;

  if (window.location.pathname == '/'){ var pathname = "";}
  if (endsWith(pathname,'/view')){
       pathname = pathname.substring(0, pathname.length - 5);
   }  
    //console.log(pathname+"/awstats_hitcounter_view");
  $.getJSON( pathname+"/awstats_hitcounter_view", function( data ) {

   if (data.success == 'true'){
 
    $( "<span/>", {
      "class": "creation-date",
      html: data.creation_date
    }).appendTo( "#awstats_hitcounter .date-created" );
       
    $( "<span/>", {
      "class": "modification-date",
      html: data.modification_date
    }).appendTo( "#awstats_hitcounter .date-modified" );

    // code for generating commas came from http://stackoverflow.com/a/29026196/642276
    $( "<span/>", {
      "class": "hits-count-for-pages",
      html: data.hits.toString().replace(/\B(?=(\d{3})+\b)/g, ",")
    }).appendTo( "#awstats_hitcounter .page-hits" );
       
    $( "<span/>", {
      "class": "views-count-for-pages",
      html: data.page_views.toString().replace(/\B(?=(\d{3})+\b)/g, ",")
    }).appendTo( "#awstats_hitcounter .page-views" );
    if ( data.hasOwnProperty('downloads') ) {
        $( "<span/>", {
          "class": "views-count-for-downloads",
          html: data.downloads.toString().replace(/\B(?=(\d{3})+\b)/g, ",")
        }).appendTo( "#awstats_hitcounter .attachment-downloads" );
        $(".page-info.awstats-downloads").show();

    }
    $("#awstats_hitcounter").show();

   }

  });
});
