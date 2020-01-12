
function validPassword(str){
    return str.length>=8 && hasLowerCase(str) && hasUpperCase(str) && hasDigit(str);
}
function validUsername(str){
    return (/^[a-zA-Z0-9._]{4,}$/.test(str));
}
function validEmail(str){
	if(str=="") return true;
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(str).toLowerCase());
}
function hasLowerCase(str) {
    return (/[a-z]/.test(str));
}
function hasUpperCase(str) {
    return (/[A-Z]/.test(str));
}
function hasDigit(str) {
    return (/[0-9]/.test(str));
}
function trim(str){
    return ltrim(rtrim(str));
}
function ltrim(str){
    if(str==null)return str;
    return str.replace(/^\s+/g,'');
}
function rtrim(str){
    if(str==null)return str;
    return str.replace(/\s+$/g,'');
} 

function hasClass(element,className){
    return (' '+element.className+' ').indexOf(' '+className+' ')>-1;
}

function disable_inputs(){
	var inputs = document.getElementsByTagName("INPUT");
	for (var i=0;i<inputs.length;i++){
		inputs[i].disabled=true;
	}
}
