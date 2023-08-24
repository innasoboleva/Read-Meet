function MeetingDataContainer() {

    const [meeting, setMeeting] = React.useState([]);
  
    React.useEffect(() => {
      fetch('/api/get_all_meetings')
      .then(response => response.json())
      .then(response => setMeeting(response))
    }, []);

    const [host, setHost] = React.useState([]);
    const [book, setBook] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/get_all_meetings', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "name": name, "skill": skill }),
    
        })
        .then(response => response.json())
        .then(response => setMeeting(response))
      }, []);
    
    React.useEffect(() => {
        fetch('/api/get_all_meetings')
        .then(response => response.json())
        .then(response => setMeeting(response))
      }, []);
    
    return (
      <React.Fragment>
        <h2>Upcoming Bok Discussions</h2>
        <table class="table table-hover">
        <thead>
            <tr>
              <th scope="col">Book</th>
              <th scope="col">Day</th>
              <th scope="col">Place</th>
              <th scope="col">Online</th>
              <th scope="col">Few words</th>
              <th scope="col">Video note</th>
              <th scope="col">Language (English, if not specified)</th>
              <th scope="col"> Guests (max specified)</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            {   books.map((meeting) => (
                <tr>
                    <td>{meeting.title}</td>
                    <td>{meeting.title}</td>
                </tr>
                ))}
          </tbody>
          </table>
      </React.Fragment>
    );
  
  }


ReactDOM.render(<MeetingDataContainer />, document.getElementById('container'));