"use strict";
const inputs = document.querySelectorAll('.inpError');
const btnEnviarFormulario = document.querySelector('.btn_crearCuenta');

btnEnviarFormulario.addEventListener('click', (e) => {


    for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value == '') {
            inputs[i].classList.add('inputError');
            inputs[i].style.boxShadow = '0px -1px 5px 1px var(--colorSecundario)';
        } else {
            inputs[i].classList.remove('inputError');
            inputs[i].style.boxShadow = '0px -1px 5px 1px var(--colorPrimario)';
        }
    }

})