code = """/* Disabled External File Drag */
window.addEventListener("dragover",function(e){
  if (e.target.type != "file") {
    e.preventDefault();
    e.dataTransfer.effectAllowed = "none";
    e.dataTransfer.dropEffect = "none";
  }
},false);
window.addEventListener("dragenter",function(e){
  if (e.target.type != "file") {
    e.preventDefault();
    e.dataTransfer.effectAllowed = "none";
    e.dataTransfer.dropEffect = "none";
  }
},false);
window.addEventListener("drop",function(e){
  if (e.target.type != "file") { // e.target.tagName == "INPUT" 
    e.preventDefault();
    e.dataTransfer.effectAllowed = "none";
    e.dataTransfer.dropEffect = "none";
  }
},false);
"""
