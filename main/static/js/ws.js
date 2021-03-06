var public_ws, token, ws_address, ws_public, ws_score;

token = this.token;

ws_address = this.ws_address;

public_ws = this.public_ws;

this.webscokets = true;

if ("WebSocket" in window) {
    //console.log("ws://" + ws_address + "/private/" + token + "/")
  ws_score = new WebSocket("wss://" + ws_address + "/private/" + token + "/");
  ws_score.onopen = function() {
    //return console.log("private connection is opened...");
  };
  ws_score.onclose = function() {
    //return console.log("private connection is closed...");
  };
  ws_score.onmessage = function(event) {
    var message, quick_panel_element, rendered, template;
    message = JSON.parse(event.data);
    if (message.action === 'notify') {
      //console.log(message);
      quick_panel_element = $('#quick_panel').find("a[href='" + message.data.url + "']");
      if (quick_panel_element.length > 0) {
        if (quick_panel_element.find('.quick_panel_new').length === 0) {
          return quick_panel_element.append($('<span class="quick_panel_new"></span>'));
        }
      } else {
        template = $('#order_notification').html();
        rendered = $('<div>');
        rendered.append(Mustache.render(template, message.data));
        return $('#quick_panel').append(rendered);
      }
    }
  };
  if (public_ws) {
    ws_public = new WebSocket("wss://" + ws_address + "/");
    ws_public.onopen = function() {
      //return console.log("public websocket connection is opened...");
    };
    ws_public.onclose = function() {
      //return console.log("public websocket connection is closed...");
    };
    ws_public.onmessage = function(event) {
      var counter, int_counter, jq_order_counter, message, rendered, template;
      message = JSON.parse(event.data);
      if (message.action === 'order') {
        jq_order_counter = $('.jq_order_counter');
        if (jq_order_counter.length > 0) {
          counter = jq_order_counter.text();
          int_counter = parseInt(counter, 10);
          if (isNaN(int_counter)) {
            int_counter = 0;
          }
          $('.jq_order_counter').text("+" + (++int_counter));
          //console.log(message);
        }
        template = $('#order_certified').html();
        rendered = $('<div>');
        rendered.append(Mustache.render(template, message.data));
        //$('.order_notifications').prepend(rendered);
        //return rendered.delay(5000).hide('slow');
      }
    };
  }
} else {
  alert("Your browser doesn't support websockets\n Please try another browser.");
  this.webscokets = false;
}

// ---
// generated by coffee-script 1.9.2
