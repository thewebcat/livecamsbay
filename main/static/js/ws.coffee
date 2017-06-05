# get local var from globals
token=this.token
ws_address=this.ws_address
public_ws=this.public_ws

#поддержка сокетов браузером
this.webscokets = true


# Проверяем поддержку websocketoв браузера
if "WebSocket" of window
    # созадем сокет на получение очков
    ws_score = new WebSocket "wss://#{ws_address}/private/#{token}/"
    ws_score.onopen = ()-> console.log "private connection is opened..."
    ws_score.onclose = () -> console.log "private connection is closed..."
    ws_score.onmessage = (event) ->
        message = JSON.parse(event.data)
        if message.action == 'notify'
            console.log message
            quick_panel_element = $('#quick_panel').find("a[href='#{message.data.url}']")
            # такой элемент уже есть
            if quick_panel_element.length > 0
                # если нет значка о новых уведомлениях, то он добавляется
                if quick_panel_element.find('.quick_panel_new').length == 0
                    quick_panel_element.append($('<span class="quick_panel_new"></span>'))
            # такого элемента нет, рендеринг из mustache
            else
                template = $('#order_notification').html();
                rendered = $('<div>')
                rendered.append(Mustache.render(template, message.data));
                $('#quick_panel').append(rendered)

    if public_ws
        ws_public = new WebSocket "wss://#{ws_address}/"
        ws_public.onopen = ()-> console.log "public websocket connection is opened..."
        ws_public.onclose = () -> console.log "public websocket connection is closed..."
        ws_public.onmessage = (event) ->
            message = JSON.parse(event.data)
            if message.action == 'order'
                jq_order_counter = $('.jq_order_counter')
                if jq_order_counter.length > 0
                    counter = jq_order_counter.text()
                    int_counter = parseInt(counter, 10)
                    if isNaN(int_counter)
                        int_counter = 0
                    $('.jq_order_counter').text("+#{++int_counter}")
                    console.log message

                template = $('#order_certified').html();
                rendered = $('<div>')
                rendered.append(Mustache.render(template, message.data));
                $('.order_notifications').prepend(rendered)
                rendered.delay(5000).hide('slow')


else
    alert("Your browser doesn't support websockets\n Please try another browser.")
    this.webscokets = false

