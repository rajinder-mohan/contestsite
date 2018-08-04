// function display() {
//   if(document.action.cpass.value=="")
//   {
//     alert("Enter Confirm Password");
//   }
//   if(document.action.pass.value!=document.action.cpass.value)
//   {
//     alert("Enter Valid Password");
//   }
// }
function validatepass() {
  var pass = $('#password').val();
  var cpass = $('#confrmpassword').val();
  if (pass != cpass) {
    console.log("Password not matched.");
  }
  else{
    console.log("Password matched.");
  }
}
function addFriend(id,elmnt){
  var url = $("#postaction").val();
  var token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
            url: url,
            type:"POST",
            data: {
               'id':id,'csrfmiddlewaretoken': token,
            },
            success: function(response) {
                alert(JSON.stringify(response));
                $(elmnt).attr("disabled","true");
            }
        });
}

function acceptFried(id,elmnt){
  var url = $("#postaction").val();
  var token = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
            url: url,
            type:"POST",
            data: {
               'id':id,'csrfmiddlewaretoken': token,
            },
            success: function(response) {
                alert(JSON.stringify(response));
                $(elmnt).attr("disabled","true");
            }
        });
}
