const Communication = {
  endpoint: 'http://localhost:5000',

  init: () => {
    const evtSrc = new EventSource(Communication.endpoint + "/subscribe");

    evtSrc.onmessage = (e) => {
      console.log(e.data);

      if (e.data.startsWith('mode: ')) {
        let mode = e.data.replace('mode: ', '');
        let modes = $('#mode-list');
        modes.find('.button').removeClass('is-active').addClass('is-outlined');
        modes.find('#mode-' + mode).addClass('is-active').removeClass('is-outlined');
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
