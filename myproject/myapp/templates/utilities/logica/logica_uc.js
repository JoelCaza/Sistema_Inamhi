const usuarioInput = document.getElementById('usuarioInput');
const contrasenaInput = document.getElementById('contrasenaInput');
const contrasenaLabel = document.getElementById('contrasenaLabel');
const usuarioLabel=document.getElementById('usuarioLabel');

usuarioInput.addEventListener('input',() => ){
    if(usuarioInput.value !==''){
        usuarioLabel.classList.add('active');
    }else{
        usuarioLabel.classList.remove('active');
    }

}