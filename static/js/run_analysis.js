apiUrl = location.protocol + '//' + location.host + location.pathname + "api/";

//check user input and process, generate result in tables
$('.integrate.Button').click(function(){

        console.log("Integrate");
        //$('.sandboxtwo').addClass('analysis');

        //retrieve user input
        var formBrokerage = $('.enter-brokerage select').find(":selected").text();
        var formBrokerageID = $('.enter-brokerage select').find(":selected").attr('brokerage-id');
        var formBrokerageUsername = $('.brokerage_username input').val();
        var formBrokeragePassword = $('.brokerage_password input').val();

        var formQuovoUsername = $('.quovo_username input').val();
        var formQuovoPassword = $('.quovo_password input').val();

        console.log("formBrokerage: " + formBrokerageID);
        console.log("formBrokerageUsername: " + formBrokerageUsername);
        console.log("formBrokeragePassword: " + formBrokeragePassword);
        console.log("formQuovoUsername: " + formQuovoUsername);
        console.log("formQuovoPassword: " + formQuovoPassword);

        //verify input otherwise display an informative message
        if(formBrokerage.includes('Loading...')) {
          alert("Choose a broker first");
          return;
        } else if(formBrokerage.includes('[pick brokerage]')) {
          alert("Select a brokerage");
          return;
        } else if (formBrokerageUsername === "") {
          alert("Enter brokerage username");
          return;
        } else if (formBrokerageUsername === "") {
          alert("Enter brokerage password");
          return;
        } else {
          console.log("process")
          $('.sandboxtwo').toggleClass('loading');
          Process(formBrokerageID, formBrokerageUsername, formBrokeragePassword, formQuovoUsername, formQuovoPassword, function(){
          });
        }
});

function Process(formBrokerageID, formBrokerageUsername, formBrokeragePassword, formQuovoUsername, formQuovoPassword) {
      //process input into server to create output json
      $('.loader').addClass('active');

      //create json data
      var run_data = '{' + '"brokerageID" : ' + formBrokerageID + ', ' + '"brokerageUsername" : "' + formBrokerageUsername + '", ' + '"brokeragePassword" : "' + formBrokeragePassword + '", ' + '"quovoUsername" : "' + formQuovoUsername + '", ' + '"quovoPassword" : "' + formQuovoPassword +'"}';

      console.log("run data: ");
      console.log(run_data)

      //make ajax call to run services and populate table
      $.ajax({
      type: 'POST',
      url: apiUrl + 'analyze',
      data: run_data,
      dataType: 'json',
      contentType: 'application/json',
      beforeSend: function() {
          //alert('Fetching....');
      },
      success: function(data) {
          console.log(data);
          $('.sandboxtwo').removeClass('loading');

          //check for error in data
          if ('error' in data) {
            alert("Error: " + data.error);
            return;
          }
          $('.table').show();

          //update header
          var holdings_title = 'Portfolio name: ' + data.portfolio_name;
          $('.title1 h3').text(holdings_title);

          //display holdings data
          var holdings_data = data.holdings;
          holdings_data = sortByKey(holdings_data, 'companyName');
          var holdingsDataLength = holdings_data.length;
          console.log("Number of objects: " + holdingsDataLength);
          var tr = "";

          for (var i = 0; i < holdingsDataLength; i++) {
              var Name = holdings_data[i].asset;
              var Company = holdings_data[i].companyName;
              var Quantiy = holdings_data[i].quantity;

              tr += "<tr tabindex='0' aria-label=" + Name + "><td>" + Name + "</td><td>" + Company + "</td><td>" + Quantiy + "</td></tr>";
          }
          $('.port-table tbody').html(tr);

        },
    error: function(jqXHR, textStatus, errorThrown) {
        //reload on error
        $('.sandboxtwo').removeClass('loading');

        alert("Error: Try again")
        console.log(errorThrown);
        console.log(textStatus);
        console.log(jqXHR);

        //location.reload();
    },
    complete: function() {
        //alert('Complete')
    }
  });
}


//sort the objects on key
function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
}
