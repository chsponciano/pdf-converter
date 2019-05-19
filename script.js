const {dialog} = require("electron").remote;
const child = require('child_process').execFile;
const path = require("path");

function select_directory(){
    let options = {properties:["openDirectory"]};
    let dir_sys_python = path.join(__dirname, '/src/dist/sysReading/sysReading.exe');
    let progress = document.getElementById("progress-bar");

    dialog.showOpenDialog(null, options, (dir) => { 
        if(dir == undefined) return;

        child(dir_sys_python, [1, dir], function(err, results) {
            if(err){
                console.log(err);
                return;
            } 

            const porcent_increment = 100 / results.length;
            let porcent = 0;

            progress.style.width = "0px";
            process.value = "0%";
            progress.classList.add("progress-bar-animated");

            for (var i = 0; i < results.length; i++) {
                
                child(dir_sys_python, [2, results[i]], function(err, returnConvert) {
                    if(err){
                        console.log(err);
                        return;
                    } 

                    porcent += porcent_increment;

                    progress.style.width = porcent + "px";
                    process.value = porcent + "%";
                    document.getElementById('out-convert').value = document.getElementById('out-convert').value + '\n' + returnConvert;
                });
            }
            
            progress.classList.remove("progress-bar-animated");
        });        
    });
}