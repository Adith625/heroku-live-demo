function submit(){
 document.getElementById("date-picker").submit();
}

$( function() {
 document.getElementById("datepicker").value=date
 $( "#datepicker" ).datepicker({
   showAnim: "slideDown",
   changeMonth: true,
   changeYear: true,
   minDate: -365,
   maxDate: 0
 } );
 

 if (stat!=-1) {
   stat=JSON.parse(stat);
   var g;
   var a;
   for (i = 0; i <4; i++) {
     g=i.toString();          
     if (stat["user_"+g]==true) {
       document.getElementById("usr"+g).getElementsByClassName("td")[1].innerHTML="&#x2713";
     }
     else{
      document.getElementById("usr"+g).getElementsByClassName("td")[1].innerHTML="&#x292B";
    }
  }
}
else{
 document.getElementById('table').style.display="none";}
}); 