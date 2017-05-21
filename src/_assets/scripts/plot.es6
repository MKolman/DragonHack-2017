const Plot = {
  stats: (participants) => {
    participants = participants ? participants : [];

    var rlist = [];
    var tlist = [];
    for (var i = 0; i < participants.length; i++) {
      rlist.push(participants[i].speed);
      tlist.push(participants[i].angle);
    }

    while (rlist.length < 4) {
      rlist.push(1000);
      tlist.push(0);
    }

    var trace1 = {
      r: rlist,
      t: tlist,
      mode: 'markers',
      marker: {
        color: '#2A2F5C',
        size: 110,
        line: {color: 'white'},
        opacity: 0.7
      },
      type: 'scatter'
    };

    var data = [trace1];

    var layout = {
      font: {size: 15},
      plot_bgcolor: '#80d5ff',
      paper_bgcolor: 'transparent',
      angularaxis: {tickcolor: '#3273dc', range: [0, 360] },
      radialaxis: {tickcolor: '#3273dc', range: [0, 100] },
      showlegend: false,
      width: 400,
      height: 400
    };

    Plotly.plot('plot', data, layout);
  }
};
