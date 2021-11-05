var userName = document.getElementById('name')
var email = document.getElementById('email')
var dbStatus = document.getElementById('status')

function add(){
    if(userName.vaue=='' || email.value==''){
        dbStatus.innerText = "Can't submit empty data!"
        dbStatus.style.cssText = 'border-color:yellow;'
        return
    }
    window.execPy(window.database, `add('${userName.value}', '${email.value}')`)
    .then((r)=>{
        if(r){
            dbStatus.innerText = "Successfuly added!"
            dbStatus.style.cssText = 'border-color:green;'
        }
        else{
            dbStatus.innerText = "Name or Email exists, try again!"
            dbStatus.style.cssText = 'border-color:red;'
        }
    })
        
}
    