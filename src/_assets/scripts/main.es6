//= require communication
//= require actions
//= require joystick

$(document).ready(() => {
  if (GlobalName != "USER") {
    $('#select-mode').show();
  }

  Communication.init();
  Actions.init();
  Joystick.init();
});
