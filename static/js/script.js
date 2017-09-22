var apiUrl = location.protocol + '//' + location.host + location.pathname + "api/";

//update interface with portfolios and risk factors

$(document).ready(function() {
  //$('.tab-bead').width($('.tab-title:nth-child(1)').width() + 24);
  $("#section_two").hide();
  $("#section_three").hide();
});

$('#home').click(function() {
  //$('.sandboxtwo').toggleClass('analysis');
  location.reload();
});

function loadPortfolio() {
    $("#section_one").hide();
    $("#section_two").show();
    $("#loader_section").hide();
    $("#portfolio_data").hide();
    $.get(apiUrl + 'brokeragenames', function(data) {
        //console.log("data in get brokeragenames");
        //console.log(data)
        $('#select_brokerage').append('<option value="" selected="selected">[pick brokerage]</option>');
        for (var i = 0; i < data.length; i++) {
          for (var key in data[i]) {
                $('#select_brokerage').append('<option value=' + key + '> ' + data[i][key] + '</option>');
            }
        }
    });
};

function loadAccern() {
  $("#section_one").hide();
  $("#section_two").hide();
  $("#section_three").show();
}

function loadPortfolioData(){
    //retrieve user input
    var brokerage= $('#select_brokerage option:selected').val();
    var brokerageUsername=$('#brokerage_username').val();
    var brokeragePassword=$('#brokerage_password').val();
    var quovoUsername=$('#quovo_username').val();
    var quovoPassword=$('#quovo_password').val();
    if(brokerage===""){
      alert("Choose a broker first");
      return;
    }
    else if (brokerageUsername === "") {
      alert("Enter brokerage username");
      return;
    } else if (brokeragePassword === "") {
      alert("Enter brokerage password");
      return;
    } else if (quovoUsername === "") {
      alert("Enter Quovo username");
      return;
    } else if (quovoPassword === "") {
      alert("Enter Quovo password");
      return;
    } else {
      //console.log("process")
      //$('.sandboxtwo').toggleClass('loading');
      Process(brokerage, brokerageUsername, brokeragePassword, quovoUsername, quovoPassword);
    }
}

function Process(formBrokerageID, formBrokerageUsername, formBrokeragePassword, formQuovoUsername, formQuovoPassword) {
  //create json data
  $("#loader_section").show();
  var run_data = '{' + '"brokerageID" : ' + formBrokerageID + ', ' + '"brokerageUsername" : "' + formBrokerageUsername + '", ' + '"brokeragePassword" : "' + formBrokeragePassword + '", ' + '"quovoUsername" : "' + formQuovoUsername + '", ' + '"quovoPassword" : "' + formQuovoPassword +'"}';
  console.log("run data: " + run_data);
  //make ajax call to run services and populate table
  $.ajax({
      type: 'POST',
      url: apiUrl + 'analyze',
      data: run_data,
      dataType: 'json',
      contentType: 'application/json',
      success: function(data) {
          //$("#portfolio_data").show();
          console.log("Data received");
          console.log(data);
          //check for error in data

          $('#portfolio_data > tr').remove();
          if ('error' in data) {
            alert("Error: " + data.error);
            return;
          }
          //update header
          var holdings_title = '<caption>Portfolio name: ' + data.portfolio_name+'<caption>';
          $('#portfolio_data').append(holdings_title);
          //display holdings data
          console.log(holdings_title);
          var holdings_data = data.holdings;
          holdings_data = sortByKey(holdings_data, 'companyName');
          for (var i = 0; i < holdings_data.length; i++) {
              $('<tr>').html("<td>" + holdings_data[i].asset + "</td><td>" + holdings_data[i].companyName + "</td><td>" +  holdings_data[i].quantity + "</td>").appendTo('#portfolio_data');
          }
          $("#loader_section").hide();
          $("#portfolio_data").show();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $("#loader_section").hide();
            alert("Error: Try again")
            console.log(errorThrown);
            console.log(textStatus);
            console.log(jqXHR);

        }});
}


//sort the objects on key
function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}
