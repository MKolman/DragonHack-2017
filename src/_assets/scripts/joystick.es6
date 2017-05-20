const Joystick = {
  init: () => {
    let w = 200;
    let h = 200;
    let ratio = window.devicePixelRatio;
    let canvas = document.getElementById("joystick");
    canvas.width = 200 * ratio;
    canvas.height = 200 * ratio;
    canvas.style.width = 200 + "px";
    canvas.style.height = 200 + "px";

    var xCenter = 100 * ratio;
    var yCenter = 100 * ratio;
    var stage = new createjs.Stage(canvas);

    var psp = new createjs.Shape();
    psp.graphics.beginFill('#333333').drawCircle(xCenter, yCenter, 25 * ratio);

    psp.alpha = 0.25;

    var vertical = new createjs.Shape();
    var horizontal = new createjs.Shape();
    vertical.graphics.beginFill('#3273dc').drawRect(100 * ratio, 0, 2 * ratio, 200 * ratio);
    horizontal.graphics.beginFill('#3273dc').drawRect(0, 100 * ratio, 200 * ratio, 2 * ratio);

    stage.addChild(psp);
    stage.addChild(vertical);
    stage.addChild(horizontal);
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener('tick', stage);
    stage.update();

    var myElement = $('#joystick')[0];

    // create a simple instance
    // by default, it only adds horizontal recognizers
    var mc = new Hammer(myElement);

    mc.on("panstart", function(ev) {
      var pos = $('#joystick').position();
      xCenter = psp.x;
      yCenter = psp.y;
      psp.alpha = 0.5;

      stage.update();
    });

    // listen to events...
    mc.on("panmove", function(ev) {
      var coords = Joystick.calculateCoords(ev.angle, ev.distance);

      psp.x = coords.x * ratio;
      psp.y = coords.y * ratio;

      $('#valSpeed').text('speed: ' + Math.round(coords.speed));
      $('#valAngle').text('direction: ' + Math.round(coords.angle));

      psp.alpha = 0.5;

      stage.update();
    });

    mc.on("panend", function(ev) {
      psp.alpha = 0.25;
      createjs.Tween.get(psp).to({
        x: xCenter,
        y: yCenter
      }, 750, createjs.Ease.elasticOut);
    });
  },

  calculateCoords: (angle, distance) => {
    var coords = {};
    distance = Math.min(distance, 100);
    var rads = (angle * Math.PI) / 180.0;

    coords.x = distance * Math.cos(rads);
    coords.y = distance * Math.sin(rads);
    coords.speed = distance;
    coords.angle = angle;

    return coords;
  }
};
