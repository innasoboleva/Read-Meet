function MeetingDataContainer() {
    const [meetings, setMeetings] = React.useState([]);
  
    React.useEffect(() => {
      fetch('/api/get_all_meetings')
        .then(response => response.json())
        .then(data => setMeetings(data))
        .catch(error => console.error('Error fetching meetings:', error));
    }, []);
  
    return (
      <React.Fragment>
        <h2>Upcoming Book Discussions</h2>
        <table className="table table-hover">
          <thead>
            <tr>
              <th scope="col">Book</th>
              <th scope="col">Day</th>
              <th scope="col">Place</th>
              <th scope="col">Offline</th>
              <th scope="col">Few words</th>
              <th scope="col">Video note</th>
              <th scope="col">Language (English, if not specified)</th>
              <th scope="col">Host</th>
              <th scope="col"> Guests (max specified)</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            { meetings.map((meeting) => (
              <MeetingRow key={meeting.id} meeting={meeting} />
            ))}
          </tbody>
        </table>
      </React.Fragment>
    );
  }

function MeetingRow({ meeting }) {
    const [host, setHost] = React.useState({});
    const [book, setBook] = React.useState({});
  
    React.useEffect(() => {
      fetch('/api/get_user_by_id', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "host_id": meeting.host_id }),
      })
        .then(response => response.json())
        .then(data => setHost(data))
        .catch(error => console.error('Error fetching host:', error));
  
      fetch('/api/get_book_by_id', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "book_id": meeting.book_id }),
      })
        .then(response => response.json())
        .then(data => setBook(data))
        .catch(error => console.error('Error fetching book:', error));
    }, [meeting]);
  
    return (
      <tr>
        <td>{book.title}</td>
        <td>{meeting.date}</td>
        <td>{meeting.place}</td>
        <td>{meeting.offline}</td>
        <td>{meeting.overview}</td>
        <td>{meeting.video}</td>
        <td>{meeting.language}</td>
        <td>{host.name}</td>
        <td>{meeting.guests}/12</td>
      </tr>
    );
  }

ReactDOM.render(<MeetingDataContainer />, document.getElementById('container'));