$(document).ready(function(){
var url = "http://127.0.0.1:8000/api/"
var endpoints = { myaccount:"myaccount/?format=json",
                  myspp:
                }
$.ajax({
url:url+endpoints.myaccount,
cache:false,
success:function (data){
$('#info_username').html(data.data.username)
$('#status_role').html(data.data.role)
}
})

})
