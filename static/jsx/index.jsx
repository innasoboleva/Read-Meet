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
          {meetings.length === 0 ? (
        <tbody><tr><td>No meetings to display.</td></tr></tbody>
      ) : (
          <tbody>
            { meetings.map((meeting) => (
              <MeetingRow key={meeting.id} meeting={meeting} user={user} />
            ))}
          </tbody>
      )}
        </table>
      </React.Fragment>
    );
  }

// each row of a meeting table
function MeetingRow(props) {
    const { meeting, user } = props;
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
    });

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
      }
      };
      
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
        }
        };

    const localDateString = convertDate(meeting.date);

    return (<React.Fragment>
      <tr>
        <td>{meeting.book_title}, <br></br>by {meeting.book_authors}</td>
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
      </React.Fragment>
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
    {groupBooks.length === 0 ? (
        <span>No books to display.</span>
      ) : (
      <div className="carousel-inner">
          { groupBooks.map((books, index) => (
              <CarouselItems user={user} key={index} books={books} isActive={index===1}/> // if index is 1, it will set block to active for carousel
          ))}
      </div>
      )}
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
      {books.length === 0 ? (
        <span>No books to display.</span>
      ) : (
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
      )}
       </div>
    </React.Fragment>
  )
}


function UsersHostDataContainer(props) {
  const { user } = props;
  const modalRef = React.useRef(null);
  const [showModal, setShowModal] = React.useState(false);
  const [meetings, setMeetings] = React.useState([]);


  React.useEffect(() => {
    // showing/hiding modal alert for cancelling meeting
    const modalElement = modalRef.current;

    if (modalElement) {
      const modal = new bootstrap.Modal(modalElement);

      if (showModal) {
        modal.show();
      }
      // hide() doesn't do anything here, closing modal using html button attr
    }
  }, [showModal]);


  const showAlertModal = (meeting, meetingDate) => {
    document.querySelector('#modal-body-alert-text').innerHTML = `<p>${meeting.book_title} by ${meeting.book_authors}</p><p>on ${meetingDate}</p>`
    setShowModal(true);
    
  };

  const deleteMeeting = () => {
    console.log("Deleting meeting...")
    setShowModal(false);
  };

  const cancelDelete = () => {
    console.log("Canceled deleting meeting...")
    setShowModal(false);
  };

  React.useEffect(() => {
    fetch('/api/get_hosted_meetings_for_user')
      .then(response => response.json())
      .then(data => {
        console.log("Hosting: ", data);
          if (data.status == "success" && data.meetings.length > 0) {
              setMeetings(data.meetings);
            }
          })
      .catch(error => console.error('Error fetching meetings:', error));
    }, [user]);

  return (
    <React.Fragment>
      <h2>Your Hosted Meetings</h2>
       <ModalAlert deleteMeeting={deleteMeeting} cancelDelete={cancelDelete} modalRef={modalRef}/>
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
        {meetings.length === 0 ? (
        <tbody><tr><td>No meetings to display.</td></tr></tbody>
      ) : (
        <tbody>
          { meetings.map((meeting) => (
            <UserHostMeetingRow key={meeting.id} meeting={meeting} showAlertModal={showAlertModal}/>
          ))}
        </tbody>
      )}
      </table>
    </React.Fragment>
  );
}


function UserHostMeetingRow(props) {
  const { meeting, showAlertModal } = props;

  const meetingDate = convertDate(meeting.date);

  return (<React.Fragment>
    <tr>
      <td>{meeting.book_title}, <br></br>by {meeting.book_authors}</td>
      <td>{meetingDate}</td>
      <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
      <td>{meeting.guests_count}/{meeting.max_guests}</td>
      <td>
          <button id="button-delete" className="btn btn-secondary" onClick={() => showAlertModal(meeting, meetingDate)}>Cancel</button>
      </td>
    </tr>
    </React.Fragment>
  );
}


function UsersGuestDataContainer(props) {
  const { user } = props;
  const [meetings, setMeetings] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/get_guest_meetings_for_user')
      .then(response => response.json())
      .then(data => {
        console.log("Guest:", data)
          if (data.status == "success" && data.meetings.length > 0) {
              setMeetings(data.meetings);
            }
          })
      .catch(error => console.error('Error fetching meetings:', error));
    }, [user]);

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
        
        {meetings.length === 0 ? (<tbody><tr><td>No meetings to display.</td></tr></tbody>
          ) : (
            <tbody>
          { meetings.map((meeting) => (
            <UserGuestMeetingRow key={meeting.id} meeting={meeting} />
          ))}
          </tbody>
        )}
      </table>
    </React.Fragment>
  );
}

function UserGuestMeetingRow(props) {
  const { meeting } = props;
  const meetingDate = convertDate(meeting.date);

  const dropMeeting = () => {
    console.log("Dropping meeting...")
  };

  return (<React.Fragment>
    <tr>
      <td>{meeting.book_title}, <br></br>by {meeting.book_authors}</td>
      <td>{meetingDate}</td>
      <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
      <td>{meeting.guests_count}/{meeting.max_guests}</td>
      <td>
          <button id="button-drop" className="btn btn-success" onClick={dropMeeting}>Drop</button>
      </td>
    </tr>
    </React.Fragment>
  );
}


function ModalAlert(props) {
  const { deleteMeeting, cancelDelete, modalRef } = props;

  return (<React.Fragment>
      <div className="modal" id="modal-alert" tablindex="-1" role="dialog" aria-labelledby="modalAlert"
      aria-hidden="true" ref={modalRef}>
      <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content">
              <button type="button" className="close" data-bs-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
              </button>
            <div className="modal-body" id="modal-body-alert">
              <div className="modal-title">
              <h3>Confirmation</h3></div>
                <h5>Do you really want to delete this meeting?</h5><br></br>
                <div id="modal-body-alert-text"></div>
            </div>
            
            <div className="modal-footer modal-footer-alert">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" aria-label="Close" onClick={cancelDelete}>
                No
              </button>
              <button type="button" className="btn btn-danger" data-bs-dismiss="modal" aria-label="Close" onClick={deleteMeeting}>
                Yes
              </button>
            </div>
          </div>
        </div>
      </div>

    </React.Fragment>
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