var bg1 = $('#background-stats-1');
var bg2 = $('#background-stats-2');
var valueA = $('#a'); 
var valueB = $('#b'); 
var total = $('#result'); 

function animateStats (a,b){
    if(a + b > 0){
        var percentA = a/(a+b)*100;
        var percentB = 100-percentA;
        bg1.width((percentA-0.3)+"%");
        bg2.width(percentB+"%");
    }
}

function updateScores (){
    $.get("https://kmti6g8um6.execute-api.eu-central-1.amazonaws.com/my-vote", null, function(result,status){
        if ("success" == status) {
            console.log(result);

            data = JSON.parse(result);
            var a = parseInt(data.a || 0);
            var b = parseInt(data.b || 0);
            
            animateStats(a, b);
        
            if(a + b > 0){
                valueA.text(Math.round((a/(a+b) * 100) * 10) / 10 + "%");
                valueB.text(Math.round((b/(a+b) * 100) * 10) / 10 + "%");
                total.text("Всего голосов: " + (a + b))
            }
        } else {
            console.log(result);
        }
    });
}

$.ajaxSetup({
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});
document.body.style.opacity=1;
updateScores();

setInterval(function() {
    updateScores();
}, 3000);
