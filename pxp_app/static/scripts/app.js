function clearFormFields(){
    let formElement = this.parentElement;
    let inputElements = ['input', 'select', 'textarea'];
    for(i in inputElements){
        let childElements = formElement.getElementsByTagName(inputElements[i]);

        for(j in childElements){
            if (childElements[j].className != "ignore-discard") {
              childElements[j].value = '';
            }
            
        }
    }
}


let discardButton = document.getElementById("form-discard");
discardButton.addEventListener('click', clearFormFields);


setTimeout(function () {
  document.getElementById("message-card").className = "hide-card";
}, 3000);