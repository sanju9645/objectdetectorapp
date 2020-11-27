window.selectedClassList=[]  //global variable

function resetClass(){
    let classes=document.getElementsByClassName('classSelect')
    classes = Array.from(classes);
    classes.forEach(element => {
        element.checked=false
    });
    window.selectedClassList = []
}

function updateSelectedClass(element){
    if(element.checked){
        if(!window.selectedClassList.includes(element.name)){
            window.selectedClassList.push(element.name)
        }
    }else{
        let index = window.selectedClassList.indexOf(element.name)
        window.selectedClassList.splice(index,1)
    }

    let imgtag=document.getElementById('stream')
    let ampIndex=imgtag.src.indexOf('&')
    let q_string='&classes='+window.selectedClassList.join(',')
    if(ampIndex==-1){
        imgtag.src+=q_string
    }else{
        let spliced_src=imgtag.src.slice(0,ampIndex)
        imgtag.src=spliced_src+q_string
    }
    //.src=window.selectedClassList.join(',')

    

}

// Array.from(document.getElementsByClassName('classSelect')).forEach(el=>{
//     updateSelectedClass(el);
// })