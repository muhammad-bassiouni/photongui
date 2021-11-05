`
BSD 3-Clause License

Copyright (c) 2021, Muhammed Bassiouni
All rights reserved.
`



class Media {
    constructor(id){
        this.media = document.getElementById(id)
    }
    get_cur_time() { 
        var timenow = this.media.currentTime
        var currenttime
      if (parseInt(timenow)/60>=1) {
            var h = Math.floor(timenow / 3600);
            timenow = timenow - h * 3600;               
            var m = Math.floor(timenow / 60);
            var s = Math.floor(timenow % 60);
            if(h.toString().length<2){h='0'+h;}
            if(m.toString().length<2){m='0'+m;}
            if(s.toString().length<2){s='0'+s;}
            currenttime = h+':'+m+':'+s      
        } else {
            var m = Math.floor(timenow / 60);
            var s = Math.floor(timenow % 60);
            if(m.toString().length<2){m='0'+m;}
            if(s.toString().length<2){s='0'+s;}
            currenttime = '00:'+m+':'+s
        }
        return currenttime
    }

    show_current_time(){
        console.log(this.get_cur_time())
    }
    
    highlight_text(){
        this.media.addEventListener("timeupdate", ()=>{
            var time = this.get_cur_time()
            try{
                let text = document.querySelector(`[time_start='${time}']`)
                text.parentNode.querySelectorAll('.sub_text').forEach(e => e.classList.remove("sub_text"))
                text.scrollIntoView({behavior: "smooth", block: "center"})
                text.classList.add("sub_text")
                }
            catch(error){
                //
            }
        })
    }
     
    
}

async function create_subtitle(){
    subtitle = await window.execPy(window.textHighlight, 'generateText()')
    var subtitle_box = document.getElementById('subtitle_box')
    for(var item of subtitle){
        var time_start = item[0][0][0]
        var time_end = item[0][0][1]
        var subtitle_content = item[1].join(' ')
        subtitle_box.innerHTML += `<span time_start='${time_start}' time_end='${time_end}'>${subtitle_content} </span>`;
    }
}



var audio = new Media("myAudio")

document.getElementById("subtitle_btn").addEventListener("click", create_subtitle)
audio.highlight_text()


