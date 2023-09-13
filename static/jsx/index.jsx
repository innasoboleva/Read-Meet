// creates a table displaying upcoming meetings
function IndexPageContainer() {
  const [user, setUser] = React.useState();

  // nav bar built in JS updates user info
  window.updateUser = (newUser) => {
    setUser(newUser);
  }

  React.useEffect(() => {
      fetch('/api/get_current_user')
        .then(response => response.json())
        .then(data => {
          setUser(data)
          if ((data.user_id != "") && (data.user_id != null)) {
              console.log("User logged in")
              window.userIsLoggedIn();
          }
          else {
              console.log("No user")
              window.userIsLoggedOut();
          }
        })
        .catch(error => console.error('Error fetching current user:', error));
    }, []);

  return (<React.Fragment>
            <CarouselDataContainer user={user}/>
            <UsersHostDataContainer user={user} />
            <UsersGuestDataContainer user={user} />
            <MeetingDataContainer user={user}/>
          </React.Fragment>);
}


function MeetingDataContainer(props) {
  const { user } = props;
    const [meetings, setMeetings] = React.useState([]);
    // const [user, setUser] = React.useState();

    React.useEffect(() => {
      console.log("User got updated, re-rendering..")
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
              <th scope="col">Few words</th>
              <th scope="col">Video note</th>
              <th scope="col">Language</th>
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
function MeetingRow(props) {
    const { meeting, user } = props;
    const [book, setBook] = React.useState({});
    // for correct displaying join meeting button and drop meeting button
    const [hideJoinButton, setHideJoinButton] = React.useState(true);
    const [hideDropButton, setHideDropButton] = React.useState(true);

    const [guestsCount, setGuestsCount] = React.useState(meeting.guests_count);

    React.useEffect(() => {
      if (guestsCount >= meeting.max_guests) {
        setHideJoinButton(true);
      }
    }, [guestsCount])
    
    React.useEffect(() => {
      console.log("User", user.user_id)
      if ((user.user_id == null) || (user.user_id == "") || (user.user_id == meeting.host_id) || (guestsCount >= meeting.max_guests)) {
        // user is a host, disable buttons
        setHideJoinButton(true);
        setHideDropButton(true);
      } else if (user.user_id && meeting.guests.includes(user.user_id)) {
        // user is a guest, disable join
        setHideJoinButton(true);
        setHideDropButton(false);
      } else {
        setHideJoinButton(false);
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
      console.log(`${meeting.id}`)
      if (user.user_id && (user.user_id != meeting.host_id)) {
        fetch('/api/join_meeting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                  setHideJoinButton(true);
                  setHideDropButton(false);
                  setGuestsCount(prevGuestsCount => prevGuestsCount + 1);
              }
          })
          .catch(error => console.error('Error joining meeting:', error));
      };
      }
      
      const dropMeeting = () => {
        if (user.user_id && (user.user_id != meeting.host_id)) {
          fetch('/api/drop_meeting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
          })
            .then(response => response.json())
            .then(data => {
                if (data && data.status == "success") {
                    setHideDropButton(true);
                    setHideJoinButton(false);
                    setGuestsCount(prevGuestsCount => prevGuestsCount - 1);
                }
            })
            .catch(error => console.error('Error dropping meeting:', error));
        };
        }


    // converting date of meeting from UTC to local user's time
    // const date = new Date(meeting.date);
    // the user's local timezone
    // const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    // const options = { timeZone: userTimeZone, year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' };
    // const localDateString = date.toLocaleDateString('en-US', options);
    const localDateString = convertDate(meeting.date);

    return (
      <tr>
        <td>{book.title}, <br></br>by {book.authors}</td>
        <td>{localDateString}</td>
        <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
        <td>{meeting.overview}</td>
        <td>{meeting.video}</td>
        <td>{meeting.language}</td>
        <td>{meeting.host_name}</td>
        <td>{guestsCount}/{meeting.max_guests}</td>
        <td>
            <button id="button-join" className="btn btn-success" disabled={hideJoinButton} onClick={joinMeeting}>Join</button>
        </td>
        <td>
            <button id="button-drop" className="btn btn-warning" disabled={hideDropButton} onClick={dropMeeting}>Drop</button>
        </td>
      </tr>
    );
  }


function CarouselDataContainer(props) {
  const { user } = props;
  // fetching popular books for carousel
  const [popularBooks, setPopularBooks] = React.useState([]);

  React.useEffect(() => {
    // getting popular books for past month from the server
    fetch('/api/get_popular_books')
      .then(response => response.json())
      .then(data => setPopularBooks(data))
      .catch(error => console.error('Error fetching popular book:', error)
      );
    }, []);
  
  const filteredBooks = popularBooks.filter(book => !book.image_url.startsWith("/static/img"));
  const groupBooks = [];
  for (let i = 0; i < filteredBooks.length; i += 3) {
    groupBooks.push(filteredBooks.slice(i, i + 3));
  }

  return (
    <React.Fragment>
    <div id="carouselExampleControls" className="carousel slide" data-bs-ride="carousel">
      <div className="carousel-inner">
          { groupBooks.map((books, index) => (
              <CarouselItems user={user} key={index} books={books} isActive={index===1}/> // if index is 1, it will set block to active for carousel
          ))}
      </div>
      <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
    </React.Fragment> 
    )
}


function CarouselItems(props) {
  const { books, user, isActive } = props;
  return (
    <React.Fragment>
      <div className={`carousel-item ${isActive ? 'active' : ''}`}>
        <div className="carousel-img-block d-flex justify-content-between">
          { books.map((book) => (
            
            <div key={book.book_id} className="carousel-image">
              <ReactRouterDOM.Link key={book.book_id} pathname={`{/books/${book.book_id}}`} to={{
            pathname: `/books/${book.book_id}`,
            state: { user, book }
            }}>
                <img src={book.image_url} className="img-fluid" alt={book.title} />
              </ReactRouterDOM.Link>
            </div>
          ))}
          
          </div>
       </div>
    </React.Fragment>
  )
}


function UsersHostDataContainer(props) {
  const { user } = props;
  const [meetings, setMeetings] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/get_hosted_meetings_for_user')
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
      <h2>Your Hosted Meetings</h2>
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Book</th>
            <th scope="col">Day</th>
            <th scope="col">Place</th>
            <th scope="col"> Guests (max specified)</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          { meetings.map((meeting) => (
            <UserHostMeetingRow key={meeting.id} meeting={meeting} user={user} />
          ))}
        </tbody>
      </table>
    </React.Fragment>
  );
}


function UserHostMeetingRow(props) {

  const { meeting, user } = props;

  const meeting_date = convertDate(meeting.date);

  const deleteMeeting = () => {
    console.log("Deleting meeting...")
  };

  return (
    <tr>
      {/* <td>{book.title}, <br></br>by {book.authors}</td> */}
      <td>{meeting_date}</td>
      <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
      <td>{guestsCount}/{meeting.max_guests}</td>
      <td>
          <button id="button-delete" className="btn btn-success" onClick={deleteMeeting}>Cancel</button>
      </td>
    </tr>
  );
}


function UsersGuestDataContainer(props) {
  const { user } = props;
  const [meetings, setMeetings] = React.useState([]);

  // React.useEffect(() => {
  //   fetch('/api/get_guest_meetings_for_user')
  //     .then(response => response.json())
  //     .then(data => {
  //         if (data) {
  //             setMeetings(data);
  //           }
  //         })
  //     .catch(error => console.error('Error fetching meetings:', error));
  //   }, [user]);

  return (
    <React.Fragment>
      <h2>Your Guest Meetings</h2>
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Book</th>
            <th scope="col">Day</th>
            <th scope="col">Place</th>
            <th scope="col"> Guests (max specified)</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          { meetings.map((meeting) => (
            <UserGuestMeetingRow key={meeting.id} meeting={meeting} user={user} />
          ))}
        </tbody>
      </table>
    </React.Fragment>
  );
}

function UserGuestMeetingRow(props) {
  const { meeting, user } = props;

  const meeting_date = convertDate(meeting.date);

  const dropMeeting = () => {
    console.log("Dropping meeting...")
  };

  return (
    <tr>
      {/* <td>{book.title}, <br></br>by {book.authors}</td> */}
      <td>{meeting_date}</td>
      <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
      <td>{guestsCount}/{meeting.max_guests}</td>
      <td>
          <button id="button-drop" className="btn btn-success" onClick={dropMeeting}>Drop</button>
      </td>
    </tr>
  );
}


function convertDate(day) {
  if (day != null) {
    // converting date of meeting from UTC to local user's time
    const date = new Date(day);
    // the user's local timezone
    const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const options = { timeZone: userTimeZone, year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' };
    const localDateString = date.toLocaleDateString('en-US', options);
    return localDateString
  }
  return ""
}