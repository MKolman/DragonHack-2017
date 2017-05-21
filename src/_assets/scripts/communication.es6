const Communication = {
  endpoint: 'http://193.2.179.248:5000',
  global_id: -1,

  init: () => {
    const evtSrc = new EventSource(Communication.endpoint + "/subscribe");

    evtSrc.onmessage = (e) => {
      console.log(e.data);

      if (e.data.startsWith('global_id: ')) {
        Communication.global_id =  e.data.replace('global_id: ', '');
      } else if (e.data.startsWith('mode: ')) {
        let mode = e.data.replace('mode: ', '');
        let pretty_mode = mode.charAt(0).toUpperCase() + mode.slice(1);
        let modes = $('#mode-list');
        modes.find('.button').removeClass('is-active').addClass('is-outlined');
        modes.find('#mode-' + mode).addClass('is-active').removeClass('is-outlined');
        $('#current-mode').text('mode: ' + pretty_mode);

        if (GlobalName == "GOD") {
          $('#joystick-placeholder').hide();
          $('#joystick-container').show();
        } else {
          if (mode == 'single') {
            $('#joystick-placeholder').show();
            $('#joystick-container').hide();
          } else {
            $('#joystick-placeholder').hide();
            $('#joystick-container').show();
          }
        }
      } else if (e.data.startsWith('subscriptions: ')) {
        let subscriptions = Number(e.data.replace('subscriptions: ', ''));
        $('#current-spectators').text('subscriptions: ' + subscriptions);
      }  else if (e.data.startsWith('movement: ')) {
        let movement = JSON.parse(e.data.replace('movement: ', ''));
        $('#current-speed').text('current speed: ' + movement.speed);
        $('#current-angle').text('current direction: ' + movement.angle);
      }
    };
  }
};
