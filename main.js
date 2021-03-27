const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const ipc = ipcMain

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation:false,
        devTools:true
    },
    maximizable: true,
    minimizable: true,
    closable: true,
  })

  win.loadFile('index.html')

  ipc.on('closeApp', ()=>{
      win.close()
  })

  ipc.on('maxApp',()=>{
    if(win.isMaximized()){
        win.restore()
    }else{
        win.maximize()
    }
  })

  ipc.on('minApp',()=>{
    win.minimize()
  })


}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
      win.webContents.openDevTools()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})