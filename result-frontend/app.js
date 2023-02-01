var bg1 = $('#background-stats-1');
var bg2 = $('#background-stats-2');
var valueA = $('#a'); 
var valueB = $('#b'); 
var total = $('#result'); 

function animateStats (a,b){
    console.log('**************animateStats inside******************');          
    if(a + b > 0){
        console.log('******* a+b>0*************');          
        var percentA = a/(a+b)*100;
        var percentB = 100-percentA;
        bg1.width((percentA-0.3)+"%");
        bg2.width(percentB+"%");
    }
}




var backend_url = "${backend_api_gateway}" + "results"

console.log('-----------------backend url--------------------')
console.log(backend_url)


function updateScores (){
    console.log('------------UPDATE SCORES FUNCTION--------------------')
    $.get(backend_url, null, function(result,status){
        if ("success" == status) {
            console.log('****************success***************************');          
            console.log(result);

            data = JSON.parse(result);
            var a = parseInt(data.a || 0);
            var b = parseInt(data.b || 0);
            
            console.log('*************ANIMATE STATS*************');
            animateStats(a, b);
        
            if(a + b > 0){
                valueA.text(Math.round((a/(a+b) * 100) * 10) / 10 + "%");
                valueB.text(Math.round((b/(a+b) * 100) * 10) / 10 + "%");
                total.text("total votes: " + (a + b))
            }
        } else {
            console.log(result);
        }
    });
}

$.ajaxSetup({
    headers: {
        'Content-Type': 'text/plain',
        'Accept': 'application/json'
    }
});

document.body.style.opacity=1;
console.log('------------main html inside--------------------')

updateScores();

setInterval(function() {
    console.log('------------set interval inside--------------------')
    updateScores();
}, 3000);
