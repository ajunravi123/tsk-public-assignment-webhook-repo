function load_data(){
    $.ajax({
        type: 'GET',
        url: "/fetch_history",
        success:function(data){
            html = "";
            data.forEach(function(value, index) {
                console.log(value["author"]);
                switch(value["action"]){
                    case "PUSH":
                        html += `<div class="msgBox"> <label class="auth">"${value["author"]}"</label> pushed to <label class="branch">"${value["to_branch"]}"</label> on ${value["timestamp"]} </div>`;
                        break;
                    case "PULL_REQUEST":
                        html += `<div class="msgBox"> <label class="auth">"${value["author"]}"</label> submitted a pull request from <label class="branch">"${value["from_branch"]}"</label> to <label class="branch">"${value["to_branch"]}"</label> on ${value["timestamp"]} </div>`;
                        break;
                    case "MERGE":
                        html += `<div class="msgBox"> <label class="auth">"${value["author"]}"</label> merged branch "${value["from_branch"]}" to <label class="branch">"${value["to_branch"]}"</label> on ${value["timestamp"]} </div>`;
                        break;
                }
            });
            if(html == ""){
                $("#dataBox").empty().append('<div class="msgBox"> No Documents Found !! </div>')
            }else{
                $("#dataBox").empty().append(html)
            }
        }
    });
}

load_data();
setInterval(function(){ 
    load_data();
    var x = document.getElementById("toast");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 2000);
}, 15000);