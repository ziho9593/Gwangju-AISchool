$(document).ready(function(){
    var num = 0;
    
    setInterval(function(){
        if(num<2){
            $("#slide ul").animate({top:"-="+400},"slow");
            num++;
        }else{
            $("#slide ul").animate({top:0},"slow");
            num = 0;
        }
    },3000);
});