const Actions = {
  init: () => {
    $('#mode-list').find('.button').click(Actions.selectMode);
  },

  selectMode: (event) => {
    let item = $(event.currentTarget);
    $('#mode-list').find('.button').removeClass('is-active').addClass('is-outlined');
    item.addClass('is-active').removeClass('is-outlined');
    $.get(Communication.endpoint + '/mode', { set: item.attr('id').replace('mode-', '') });
  },

  updateMovementLast: -1,
  updateMovement: (speed, angle, force) => {
    let old = Actions.updateMovementLast;
    let now = new Date().getTime();
    if (!force && now - old < 250)
      return;

    Actions.updateMovementLast = now;

    $.get(Communication.endpoint + '/movement', { speed: speed, angle: angle, global_id: Communication.global_id });
  }
};
