//= require communication
//= require actions
//= require joystick

$(document).ready(() => {
  Communication.init();
  Actions.init();
  Joystick.init();
});
