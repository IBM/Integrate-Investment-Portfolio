var apiUrl = location.protocol + '//' + location.host + location.pathname + "api/";

//update interface with portfolios and risk factors
function updateText() {
  $('.table').hide();

    console.log("apiUrl: " + apiUrl)
    //update portfolio lists
    var brokerageLists;
    $.get(apiUrl + 'brokeragenames', function(data) {
        $('.enter-brokerage select').html(function() {
            var str = '<option value="" disabled="" selected="">[pick brokerage]</option>';
            //var parsed = JSON.parse(data)
            console.log("data in get brokeragenames");
            console.log(data)
            for (var i = 0; i < data.length; i++) {
              for (var key in data[i]) {
                    str = str + '<option brokerage-id=' + key + '> ' + data[i][key] + '</option>';
                }
            }
            //brokerageLists = parsed;
            console.log("str: " + str)
            return str;
        });
    });
}
