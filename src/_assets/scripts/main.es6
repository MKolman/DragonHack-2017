//= require communication
//= require actions
//= require joystick
//= require plot

$(document).ready(() => {
  if (GlobalName != "USER") {
    $('#select-mode').show();
  }

  Communication.init();
  Actions.init();
  Joystick.init();

  Plot.stats();
});
