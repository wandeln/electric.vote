function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function ajax_error(request,error){
    console.log(request)
    console.log(error)
}

function ajax_ok(data){
    console.log(data)
}

function send_ajax(url,data,response_handler){
    $.ajaxSetup({
        headers:{
            'X-CSRFToken':getCookie("_xsrf")
        }});
    let r = {
        url: url,
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'html',
        success: response_handler,
        error: ajax_error
        }
    $.ajax(r)
}

function redirect_handler(data){
    window.location.href = data
}

function update_users_handler(data){
    document.getElementById('users').innerHTML = data
}

function update_polls_handler(data){
    document.getElementById('polls').innerHTML = data
}

function update_slider(id){
    slider_label = document.getElementById('slider_label_'+id)
    slider = document.getElementById('slider_'+id)
    send_ajax('/choice_vote_ajax',{choiceId:id,vote:slider.value},update_choices_handler)
    label = "direct vote: "+Math.round(slider.value*1000)/1000;
    if(slider.value<-1/3){
        label += " (CONTRA)"
    }else if(slider.value<1/3){
        label += " (NEUTRAL)"
    }else{
        label += " (PRO)"
    }
    slider_label.innerHTML = label;
}

function update_choices_handler(data){
	if(data=="error"){
		location.reload()
	}
    //document.getElementById('choices').innerHTML = data
}
