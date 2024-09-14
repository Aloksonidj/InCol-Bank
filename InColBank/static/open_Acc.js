
if (document.querySelector("#special").innerHTML){
        
    let msg = document.querySelector("#special").innerHTML
    const some = document.querySelector("#Some").innerHTML

    if( msg ^ some){
        alert(`${some} : ${msg}`)
        window.location.href = "\login"
    }
    
}
