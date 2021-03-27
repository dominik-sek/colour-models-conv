const {ipcRenderer} = require('electron')
const ipc = ipcRenderer


closeBtn.addEventListener('click',()=>{
  ipc.send('closeApp')
})
minBtn.addEventListener('click',()=>{
  ipc.send('minApp')
})
maxBtn.addEventListener('click',()=>{
  ipc.send('maxApp')
})