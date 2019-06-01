const { app, BrowserWindow, dialog } = require('electron')

function createWindow () {
  	let win = new BrowserWindow({ width: 900, height: 600, minWidth: 900, minHeight: 600, maxWidth: 900, maxHeight: 600 });
  	win.loadFile('index.html')
}

app.on('window-all-closed', function() {
  if (process.platform != 'darwin') {
    app.quit();
  }
});

app.on('ready', createWindow)
