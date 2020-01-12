
min_left_column_width = 300;//250
left_relative_width = '25%'
min_center_column_width = 400
min_right_column_width = 300;//250
right_relative_width = '25%'

left_column_toggle = true
right_column_toggle = true

function getElementWidth(element){
    return element.offsetWidth+
    parseInt(window.getComputedStyle(element).marginLeft)+
    parseInt(window.getComputedStyle(element).marginRight)
}

function updateColumnWidth(){
    width = window.innerWidth
    
    document.getElementById("left_toggle").textContent=left_column_toggle?"<":">"//"x":"="
    document.getElementById("right_toggle").textContent=right_column_toggle?">":"<"//"x":"="
    
    if(left_column_toggle == false){
        document.documentElement.style.setProperty('--left-width','0px')
    }else if(width<4*min_left_column_width){
        document.documentElement.style.setProperty('--left-width',''+min_left_column_width+'px')
    }else{
        document.documentElement.style.setProperty('--left-width',left_relative_width)
    }
    
    if(right_column_toggle == false){
        document.documentElement.style.setProperty('--right-width','0px')
    }else if(width<4*min_right_column_width){
        document.documentElement.style.setProperty('--right-width',''+min_right_column_width+'px')
    }else{
        document.documentElement.style.setProperty('--right-width',right_relative_width)
    }
    
    if(width<min_left_column_width+min_center_column_width&&left_column_toggle||
        width<min_center_column_width+min_right_column_width&&right_column_toggle
    ){
        document.documentElement.style.setProperty('--center-width',''+width+'px')
    }else{
        document.documentElement.style.setProperty('--center-width','calc(100% - var(--left-width) - var(--right-width))')
    }
    
    if(!left_column_toggle&&right_column_toggle&&width<min_center_column_width+min_right_column_width){
        document.documentElement.style.setProperty('--left-origin',''+(-getElementWidth(document.getElementById("column_right")))+'px')
    }else{
        document.documentElement.style.setProperty('--left-origin','0px')
    }
}

function onStart(){
    width = window.innerWidth
    if(width<min_left_column_width+min_center_column_width+min_right_column_width){
        right_column_toggle=false
    }
    if(width<min_left_column_width+min_center_column_width){
        left_column_toggle=false
    }
    updateColumnWidth()
    //window.scrollTo(0,1);
}
//window.onload=onStart

function onResize(){
    width = window.innerWidth
    if(width<min_left_column_width+min_center_column_width+min_right_column_width&&left_column_toggle){
        right_column_toggle=false
    }
    updateColumnWidth()
}
window.onresize=onResize

function toggle_left_column(column){
    left_column_toggle = !left_column_toggle
    if(width<min_left_column_width+min_center_column_width+min_right_column_width&&left_column_toggle){
        right_column_toggle=false
    }
    updateColumnWidth()
}

function toggle_right_column(column){
    right_column_toggle = !right_column_toggle
    if(width<min_left_column_width+min_center_column_width+min_right_column_width&&right_column_toggle){
        left_column_toggle=false
    }
    updateColumnWidth()
}


function toggle_chart_line(element,index){
	hidden = !lineChart.data.datasets[index].hidden;
	lineChart.data.datasets[index].hidden = hidden;
	lineChart.update();
	if(hidden){
		element.childNodes[7].style.textDecoration = "line-through";
	}else{
		element.childNodes[7].style.textDecoration = "none";
	}
}
