var isDark = true;
function switchTheme(){
    if(isDark){
        toggleLight();
    }else{
        toggleDark();
    }
    isDark = !isDark;
}

function toggleDark(){
    addClass('body', 'body-light', 'body-dark');

    addClass('navbar', 'navbar-light', 'navbar-dark');
    addClass('navbar', 'bg-light', 'bg-dark');

    addClass('class-choose-btn', 'btn-outline-dark', 'btn-outline-light');
}

function toggleLight(){
    addClass('body', 'body-dark', 'body-light');
    
    addClass('navbar', 'navbar-dark', 'navbar-light');
    addClass('navbar', 'bg-dark', 'bg-light');

    addClass('class-choose-btn', 'btn-outline-light', 'btn-outline-dark');
}

function addClass(id, remove, add){
    document.getElementById(id).classList.remove(remove);
    document.getElementById(id).classList.add(add);   
}

switchTheme();