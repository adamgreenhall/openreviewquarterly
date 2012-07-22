function getTops(){
    console.log('getting tops');
    sections = $(".pieceheader");  // all content sections
    totoplink = $('.current-piece a');  // all nav sections
    topsArray = sections.map(function() {
        return $(this).position().top - 300;  // make array of the tops of content
    }).get();                                 //   sections, with some padding to
                                              //   change the class a little sooner   
    len = topsArray.length;  // quantity of total sections
    
    dir = window.location.pathname;
    //console.log(dir.indexOf('.'))
    if (dir.indexOf('.')!=-1){dir = dir.substring(0, dir.lastIndexOf('.'))}
    //console.log(dir)
    //$("div#header").css("border","3px solid green");
    //console.log(sections)
    //console.log(topsArray)       
}

$(document).ready( function(){ 
    if (typeof sections=="undefined"){
        getTops();
        currentIndex=0;
        }
})


//    // on scroll,  call the getCurrent() function above, and see if we are in the
//    //    current displayed section. If not, add the "selected" class to the
//    //    current nav, and remove it from the previous "selected" nav
// 

$(document).scroll(function(e) {
    if (typeof sections=="undefined"){
        getTops();
        currentIndex=0;
        }
    getCurrent = function( top ) {   // take the current top position, and see which
        for( var i = 0; i < len; i++ ) {   // index should be displayed
            if( top > topsArray[i] && topsArray[i+1] && top < topsArray[i+1] ) {
                return i;
            }
        }
        if (top>topsArray[len-1]){return len-1;} //its the last section
    };    
    
    var scrollTop = $(this).scrollTop();
    var checkIndex = getCurrent( scrollTop );
    console.log(checkIndex,currentIndex)
    if (currentIndex==undefined){
      totoplink.attr('style','visibility:hidden');
    }
    if( checkIndex !== currentIndex ) {
        currentIndex = checkIndex;
        if (checkIndex==undefined){ totoplink.attr('style','visibility:hidden') }
        else {
            totoplink.attr({
                'href':(dir+'/'+sections.eq(checkIndex).attr('id')),
                'style':'visibility:visible'
                });
            }
        
    }
});