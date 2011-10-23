$(document).ready(function(){
  $("#startwizard").click(function(){
    $("#app").load('/startwizard', null,function(){
        // Smart Wizard     
        $('#wizard').smartWizard();
      });
  });
});
