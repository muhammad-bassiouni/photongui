var loader = document.querySelector(".loader")
var faceDetection = document.querySelector("#faceDetection")
var eyeDetection = document.querySelector("#eyeDetection")
let liveImage = document.getElementById('bg');

function py_video(self) {
    if (self.getAttribute('elem-data') == "start"){
        self.setAttribute("elem-data", "stop")
        self.style.background = "#dc3545"
        self.textContent = "Stop"
        loader.style.display = "block"
        var optionsSelected = JSON.stringify(selectedOption())
        window.execPy(window.faceEyeDetection, `startVideo(${optionsSelected})`)
        console.log("Start")
    }
    else {
        window.execPy(window.faceEyeDetection, `stopVideo()`)
        resetGui(self)
        console.log("Stop")
    }
   
}

function resetGui(self){
    self.setAttribute("elem-data", "start")
    self.style.background = "#28a745"
    self.textContent = "Start"
    liveImage.src = "images/facial-recognition.svg"
    loader.style.display = "none"
}

function selectedOption(){
    return [Number(faceDetection.checked), Number(eyeDetection.checked)]
}


function updateImageSrc(imageBase64) {
    loader.style.display = "none"
    liveImage.src = "data:image/jpg;base64," + imageBase64
}


