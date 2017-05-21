//= require communication
//= require actions
//= require joystick
//= require plot

$(document).ready(() => {
  if (GlobalName != "USER") {
    $('#select-mode').show();
  } else {
    $('#joystick-video').remove();
  }

  Communication.init();
  Actions.init();
  Joystick.init();

  Plot.stats();
});
