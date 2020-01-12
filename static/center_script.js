function getElementHeight(element){
    return element.offsetHeight+
    parseInt(window.getComputedStyle(element).marginTop)+
    parseInt(window.getComputedStyle(element).marginBottom)
}


function recenter(){
    
    if(window.innerHeight > getElementHeight(document.getElementById("card"))){
        document.getElementById("center").style.setProperty('align-items','center');
    }else{
        document.getElementById("center").style.setProperty('align-items','flex-start');
    }
    /*
    if(window.innerWidth > 750){
        document.getElementById("center").style.setProperty('flex-direction','row');
    }else{
        document.getElementById("center").style.setProperty('flex-direction','column');
        document.getElementById("center").style.setProperty('align-items','center');
    }*/
}

window.onload=recenter
window.onresize=recenter
