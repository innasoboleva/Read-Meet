// creates a table displaying upcoming meetings
function MeetingDataContainer() {
    const [meetings, setMeetings] = React.useState([]);
    const [user, setUser] = React.useState();
  
    React.useEffect(() => {
        fetch('/api/get_current_user')
          .then(response => response.json())
          .then(data => setUser(data))
          .catch(error => console.error('Error fetching current user:', error));
      }, []);

    React.useEffect(() => {
      fetch('/api/get_all_meetings')
        .then(response => response.json())
        .then(data => {
            if (data) {
                setMeetings(data);
            }
            })
        .catch(error => console.error('Error fetching meetings:', error));
    }, [user]);


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
              <MeetingRow key={meeting.id} meeting={meeting} user={user} />
            ))}
          </tbody>
        </table>
      </React.Fragment>
    );
  }
// each row of a meeting table
function MeetingRow({ meeting, user }) {
    const [host, setHost] = React.useState({});
    const [book, setBook] = React.useState({});
    // for correct displaying join meeting button and drop meeting button
    const [hideJoinButton, setHideJoinButton] = React.useState(false);
    const [hideDropButton, setHideDropButton] = React.useState(false);

    if (meeting.guests.includes(user.user_id)) {
        setHideJoinButton(true);
        setHideDropButton(false);
    };
  
    React.useEffect(() => {
      if (meeting.guests.includes(user.user_id)) {
        setHideJoinButton(true);
        setHideDropButton(false);
      };

      if (user && user.user_id && meeting.host_id && user.user_id != meeting.host_id) { // check that user exists, has id and he is not a host
          fetch('/api/get_user_by_id', {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ "host_id": meeting.host_id }),
            })
              .then(response => response.json())
              .then(data => setHost(data))
              .catch(error => console.error('Error fetching host:', error));
      } else {
          setHideJoinButton(true);
          setHideDropButton(true);
      };
      
      fetch('/api/get_book_by_id', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "book_id": meeting.book_id }),
      })
        .then(response => response.json())
        .then(data => setBook(data))
        .catch(error => console.error('Error fetching book:', error));
    }, [meeting]);

    const joinMeeting = () => {
      fetch('/api/join_meeting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "meeting_id": meeting.meeting_id, "user_id": user.user_id }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                  setHideJoinButton(true);
                  setHideDropButton(false);
              }
          })
          .catch(error => console.error('Error joining meeting:', error));
      };
  
      const dropMeeting = () => {
      fetch('/api/drop_meeting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "meeting_id": meeting.meeting_id, "user_id": user.user_id }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                  setHideDropButton(true);
                  setHideJoinButton(false);
              }
          })
          .catch(error => console.error('Error joining meeting:', error));
      };

    return (
      <tr>
        <td>{book.title}, <br></br>by {book.authors}</td>
        <td>{meeting.date}</td>
        <td>{meeting.place}</td>
        <td>{meeting.offline}</td>
        <td>{meeting.overview}</td>
        <td>{meeting.video}</td>
        <td>{meeting.language}</td>
        <td>{host.name}</td>
        <td>{meeting.guests_count}/12</td>
        <td>
            <button id="button-join" className="btn btn-success" disabled={hideJoinButton} onClick={() => joinMeeting(meeting.id, user.user_id)}>Join</button>
        </td>
        <td>
            <button id="button-drop" className="btn btn-warning" disabled={hideDropButton} onClick={() => dropMeeting(meeting.id, user.user_id)}>Drop</button>
        </td>
      </tr>
    );
  }



ReactDOM.render(<MeetingDataContainer />, document.getElementById('container'));