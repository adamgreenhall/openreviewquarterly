$(document).ready(function() {
 var iphone = screen.width <= 320 
 if (iphone) { return; }

 //if not an iphone

  function filterPath(string) {
    return string
      .replace(/^\//,'')
      .replace(/(index|default).[a-zA-Z]{3,4}$/,'')
      .replace(/\/$/,'');
  }
  
  var sections = $(".pieceheader");  // all content sections
  var toPiecelink = $('#to-piece-link');  
  var issue_title = $('.pieces').attr('id');
  // make array of the tops of content sections, with some padding 
  var topsArray = sections.map(function() { return $(this).position().top - 300; }).get();
  var currentIndex=0;                              
  
  var locationPath = filterPath(location.pathname);
  var padding = -20;
  var speed = 1000;

  $('.toc-hash-link').each(function() {
    var target = this.hash;
    $(this).click(function(event) {
      event.preventDefault();
      $.scrollTo( $(target), speed, {offset:padding});
    });
  });
    
  $(document).scroll(function(e) {

      var getCurrent = function( top ) {   // take the current top position, and see which
          for( var i = 0; i < topsArray.length; i++ ) {   // index should be displayed
              if( top > topsArray[i] && topsArray[i+1] && top < topsArray[i+1] ) { return i; }
          }
          if (top>topsArray[topsArray.length-1]){return topsArray.length-1;} //its the last section
      };    
    
      var scrollTop = $(this).scrollTop();
      var checkIndex = getCurrent( scrollTop );
      console.log(checkIndex,currentIndex)
      if (currentIndex==undefined){ toPiecelink.attr('style','visibility:hidden'); }
      if( checkIndex !== currentIndex ) {
          currentIndex = checkIndex;
          console.log('change',currentIndex,toPiecelink)
          if (checkIndex==undefined){ toPiecelink.attr('style','visibility:hidden') }
          else {
              toPiecelink.attr({
                  'href':( issue_title.concat('/').concat(sections.eq(checkIndex).attr('id')) ),
                  'style':'visibility:visible'
                  });
          }
      }
  });
});