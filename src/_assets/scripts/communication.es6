const Communicaton = {
  init: () => {
    const evtSrc = new EventSource("http://localhost:5000/subscribe");

    evtSrc.onmessage = (e) => {
        console.log(e.data);
    };
  }
};
