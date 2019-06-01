const { dialog } = require("electron").remote;
const child = require('child_process').execFile;
const path = require("path");
const dir_sys_python = path.join(__dirname, '/src/dist/sysReading/sysReading.exe');
const progress = document.getElementById("progress-bar");

let dir_pdfs = null;

function select_directory(e) {
    let options = { properties: ["openDirectory"] };

    dialog.showOpenDialog(null, options, (dir) => { 
        if(dir == undefined) return;

        dir_pdfs = dir;              
        e.value = dir;
    });
}

function convert(){
    child(dir_sys_python, [1, dir_pdfs], function(err, results) {
        if(err){
            alert(err);
            return;
        }
        
        progress.style.width = "0%";
        progress.textContent = "0%";
        document.getElementById("out-convert").value = "";

        results = results.replace(/'|\[|\]|\s|\n|\t/gi, '');
        results = results.replace(/\\\\/gi, '\\');

        let list_files = results.split(',');

        const porcent_increment = 100 / list_files.length;
        let porcent = 0;

        for (let i = 0; i < list_files.length; i++) {
            child(dir_sys_python, [2, list_files[i]], function(errC, resultsC) {
                if(errC){
                    alert(errC)
                    return;
                }
                porcent += porcent_increment;
                progress.style.width = porcent + "%";
                progress.textContent = porcent + "%";
                document.getElementById("out-convert").value = document.getElementById("out-convert").value + resultsC;
            });
        }
    });
}