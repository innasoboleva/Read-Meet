// parent component keeping track of all children
function IndexPageContainer() {
  const [user, setUser] = React.useState();
  const [meetingToAdd, setMeetingToAdd] = React.useState(null);
  const [meetingToDrop, setMeetingToDrop] = React.useState(null);

  const [meetingToDropFromGuest, setMeetingToDropFromGuest] = React.useState(null);
  const [meetingToDelete, setMeetingToDelete] = React.useState(null);
  const [messages, setMessages] = React.useState([]);
  // for referencing timer, for clean up
  const timersRef = React.useRef({});
  
   //  to add a message with a timer
   const addMessageWithTimer = (message) => {
    const uniqueKey = `${message}_${Date.now()}`;

     setMessages((prevMessages) => [...prevMessages, { message, key: uniqueKey }]);
      // to clear this specific message after 20 seconds
      const timer = setTimeout(() => {
        setMessages((prevMessages) => prevMessages.filter((prevMessage) => prevMessage.key !== uniqueKey));
        clearTimeout(timersRef.current[uniqueKey]);
        delete timersRef.current[uniqueKey];
        }, 15000);
        timersRef.current[uniqueKey] = timer;
  };

  // nav bar built in JS updates user info
  window.updateUser = (newUser) => {
    setUser(newUser);
    if (newUser != null && newUser.name != "") {
      addMessageWithTimer(`You logged in as ${newUser.name}`);
    } else if (newUser != null && newUser.name == "") {
      addMessageWithTimer(`You logged out`);
    }
  }

  // setting up AWS
  const AWS = window.AWS;

  React.useEffect(() => {
    if (meetingToAdd) {
      addMessageWithTimer(`You joined a meeting for "${meetingToAdd.book_title}" on ${convertDate(meetingToAdd.date)}`);
    }
  }, [meetingToAdd]);

  React.useEffect(() => {
    if (meetingToDrop) {
      addMessageWithTimer(`You dropped from a meeting for "${meetingToDrop.book_title}" on ${convertDate(meetingToDrop.date)}`);
    }
  }, [meetingToDrop]);


  React.useEffect(() => {
    const controller1 = new AbortController();
    const controller2 = new AbortController();

      fetch('/api/get_current_user', {signal: controller1.signal })
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

      fetch('/api/get_aws_keys', {signal: controller2.signal })
        .then(response => response.json())
        .then(data => {
          if (data.status == 'success') {
            
            AWS.config.update({
              region: 'us-east-2',
              accessKeyId: data.data[0], // 'your-access-key-id',
              secretAccessKey: data.data[1] //'your-secret-access-key',
            });
            window.s3 = new AWS.S3();
            console.log("S3 was succesfully set", window.s3)
          }
        })
        .catch(error => console.error('Error fetching AWS keys:', error));

        return () => {
          // cancel the request before component unmounts
          controller1.abort();
          controller2.abort();
          // Clean up timers and messages when the component unmounts
          Object.values(timersRef.current).forEach((timer) => {
            clearTimeout(timer);
          });
          timersRef.current = {};
          setMessages([]);
      };
    }, []);

  const dropMeetingFromGuest = (meeting) => {
    setMeetingToDropFromGuest(meeting);
  }

  const deleteMeetingFromMeetingTable = (meeting) => {
    setMeetingToDelete(meeting);
    addMessageWithTimer(`You canceled a meeting for "${meeting.book_title}"`);
  }

  return (<React.Fragment>
           <Messages messages={messages}/>
            <div id="background-img">
              <img src="/static/img/house_on_the_hill.png" alt="Background picture with house on the hill"></img>
            </div>
            <CarouselDataContainer user={user}/>
            <div id="index-container-tables">
            <div className="column" id="meeting-table-container">
                <MeetingDataContainer user={user} meetingToDelete={meetingToDelete} meetingToAdd={meetingToAdd} meetingToDrop={meetingToDrop} setMeetingToAdd={setMeetingToAdd} setMeetingToDrop={setMeetingToDrop} meetingToDropFromGuest={meetingToDropFromGuest}/>
              </div>
              { (user && user.user_id != "" && user.user_id != null) ? (
                <React.Fragment>
                  <div className="column">
                    <div id="host-table-container">
                      <UsersHostDataContainer user={user} deleteMeetingFromMeetingTable={deleteMeetingFromMeetingTable}/> 
                    </div>
                    <div id="guest-table-container">
                      <UsersGuestDataContainer user={user} meetingToAdd={meetingToAdd} meetingToDrop={meetingToDrop} dropMeetingFromGuest={dropMeetingFromGuest}/>
                    </div>
                  </div>
                </React.Fragment>
              ) : (
                  <div>You will see your personal meetings here if you log in </div>
              )}
            </div>
            <footer>
                <div className="footer-content">
                    <p>&copy; 2023, Inna Soboleva. All rights reserved.</p>
                </div>
              </footer>
          </React.Fragment>);
}

function Messages(props) {
  const { messages } = props;
  
  return (
    <React.Fragment>
     <div id="flash-messages">
     {messages && messages.map((messageObject) => (
            <li key={messageObject.key}>{messageObject.message}</li>
          ))}
      </div>
    </React.Fragment>
  );
}


// table for all upcoming meeting for everyone
function MeetingDataContainer(props) {
  const { user, meetingToDelete, meetingToAdd, meetingToDrop, setMeetingToAdd, setMeetingToDrop, meetingToDropFromGuest } = props;
    const [meetings, setMeetings] = React.useState([]);


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

    React.useEffect(() => {
      const updatedMeetings = meetings.filter(meeting => meeting.id !== meetingToDelete.id);
      setMeetings(updatedMeetings);
    }, [meetingToDelete])
      
    return (
      <React.Fragment>
        <h3 id="h2-meeting-table">Upcoming Book Discussions</h3>
        <div id="meeting-table">
          <table className="table table-hover" >
            <thead>
              <tr>
                <th scope="col">Book</th>
                <th scope="col">Day</th>
                <th scope="col">Place</th>
                <th scope="col">Few words</th>
                <th scope="col">Video note</th>
                <th scope="col">Lg.</th>
                <th scope="col">Host</th>
                <th scope="col"> Guests</th>
                <th scope="col"></th>
              </tr>
            </thead>
            {meetings.length === 0 ? (
          <tbody><tr><td>No meetings to display.</td></tr></tbody>
        ) : (
            <tbody>
              { meetings
              .sort((a, b) => new Date(a.date) - new Date(b.date)) // Sort meetings by date
              .map((meeting) => (
                <MeetingRow key={meeting.id} meeting={meeting} user={user} meetingToAdd={meetingToAdd} meetingToDrop={meetingToDrop} setMeetingToAdd={setMeetingToAdd} setMeetingToDrop={setMeetingToDrop} meetingToDropFromGuest={meetingToDropFromGuest}/>
              ))}
            </tbody>
        )}
          </table>
        </div>
      </React.Fragment>
    );
  }

// each row of a meeting table
function MeetingRow(props) {
    const { meeting, user, meetingToAdd, meetingToDrop, setMeetingToAdd, setMeetingToDrop, meetingToDropFromGuest } = props;
    // for correct displaying join meeting button and drop meeting button
    const [hideJoinButton, setHideJoinButton] = React.useState(false);
    const [hideDropButton, setHideDropButton] = React.useState(false);
    const [guestsCount, setGuestsCount] = React.useState(meeting.guests_count);

    React.useEffect(() => {
      if (guestsCount >= meeting.max_guests) {
        setHideJoinButton(true);
      }
    }, [guestsCount]);

    React.useEffect(() => {
      if (meetingToDropFromGuest != null && meetingToDropFromGuest.id === meeting.id) {
        dropMeeting();
      }
    }, [meetingToDropFromGuest]);
    
    React.useEffect(() => {
      // check for initial render with no updates made yet
      if (meetingToDropFromGuest == null && meetingToDrop == null & meetingToAdd == null) {
        if ((user.user_id == null) || (user.user_id == "") || (user.user_id == meeting.host_id) || (meeting.guests_count >= meeting.max_guests) && !(meeting.guests.includes(user.user_id))) {
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
      }
    });

    React.useEffect(() => {
      if (meeting.video) {
        fetchVideoBlob(meeting.id, meeting.video);
      }
    }, [meeting]);

    const joinMeeting = () => {
      if (user.user_id && (user.user_id != meeting.host_id)) {
        fetch('/api/join_meeting', {
          method: 'UPDATE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                if (meetingToAdd == meeting) {
                  setMeetingToAdd(null);
                }
                  meeting.guests.push(user.user_id) // add user_id
                  meeting.guests_count = meeting.guests_count + 1;
                  setHideJoinButton(true);
                  setHideDropButton(false);
                  setGuestsCount(prevGuestsCount => prevGuestsCount + 1);
                  setMeetingToAdd(meeting);
              }
          })
          .catch(error => console.error('Error joining meeting:', error));
      }
    };
      
      const dropMeeting = () => {
        if (user.user_id && (user.user_id != meeting.host_id) && meeting.guests.includes(user.user_id)) {
          fetch('/api/drop_meeting', {
            method: 'UPDATE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
          })
            .then(response => response.json())
            .then(data => {
                if (data && data.status == "success") {
                  if (meetingToDrop == meeting) {
                    setMeetingToDrop(null);
                  }
                  meeting.guests = meeting.guests.filter(item => item != user.user_id) // remove user_id
                  meeting.guests_count = meeting.guests_count - 1;
                  setHideJoinButton(false);
                  setHideDropButton(true);
                  setGuestsCount(prevGuestsCount => prevGuestsCount - 1);
                  setMeetingToDrop(meeting);
                }
            })
            .catch(error => console.error('Error dropping meeting:', error));
        }
      };

    const localDateString = convertDate(meeting.date);

    return (<React.Fragment>
      <tr>
        <td className="book-title">{meeting.book_title}, <br></br>by {meeting.book_authors}</td>
        <td>{localDateString}</td>
        <td>{meeting.offline ? meeting.place : 'Zoom'}</td>
        <td>{meeting.overview}</td>
        <td>
        { meeting.video ? (<video className="video-note" id={`video-${meeting.id}`} controls controlsList="nodownload"/>) : ('-')}</td>
        <td>{meeting.language}</td>
        <td>{meeting.host_name}</td>
        <td>{meeting.guests_count}/{meeting.max_guests}</td>
        <td>
            <button id={`button-join-${meeting.id}`} className="btn btn-success join" disabled={hideJoinButton} onClick={joinMeeting}>Join</button>
            <button id={`button-drop-${meeting.id}`} className="btn btn-warning drop" disabled={hideDropButton} onClick={dropMeeting}>Drop</button>
        </td>
      </tr>
      </React.Fragment>
    );
  }

// component for showing books
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
  const groupedBooks = [];
  for (let i = 0; i < filteredBooks.length; i += 3) {
    groupedBooks.push(filteredBooks.slice(i, i + 3));
  }

  const phrases = [ 'Did you read these popular books?', 'Try these popular books!', 'Could this be the next book for you?', 'Judge a book by more than its cover. Try it out.', 'Why not see if one of these books is right for you?']
  const randomIndex = Math.floor(Math.random() * phrases.length);
  const popular_book_phrase = phrases[randomIndex];

  return (
    <React.Fragment>
    <div id="carouselExampleControls" className="carousel slide" data-bs-ride="carousel">
    <h2 id="popular-book-title">{popular_book_phrase}</h2>
    {groupedBooks.length === 0 ? (
        <span>No books to display.</span>
      ) : (
      <div className="carousel-inner">
          { groupedBooks.map((books, index) => (
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

// child component of carousel, showing three books at the same time
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

// table for all upcoming meeting for user if user is a host
function UsersHostDataContainer(props) {
  const { user, deleteMeetingFromMeetingTable } = props;
  const modalRef = React.useRef(null);
  const [showModal, setShowModal] = React.useState(false);
  const [meetings, setMeetings] = React.useState([]);

  const [meetingToDelete, setMeetingToDelete] = React.useState();

  React.useEffect(() => {
    // showing/hiding modal alert for cancelling meeting
    const modalElement = modalRef.current;

    if (modalElement) {
      const modal = new bootstrap.Modal(modalElement);

      if (showModal) {
        modal.show();
      } else {
        modal.hide();
      }
    }
  }, [showModal]);


  const showAlertModal = (meeting, meetingDate) => { // showing modal alert with provided meeting info
    document.querySelector('#modal-body-alert-text').innerHTML = `<p>${meeting.book_title} by ${meeting.book_authors}</p><p>on ${meetingDate}</p>`
    setShowModal(true);
    setMeetingToDelete(meeting);
  };

  const deleteMeeting = () => {
    setShowModal(false);

    fetch('/api/delete_meeting', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "meeting_id": meetingToDelete.id, "user_id": user.user_id }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status == "success") {
            console.log("Meeting was deleted");
            const updatedMeetings = meetings.filter(meeting => meeting.id != meetingToDelete.id);
            deleteMeetingFromMeetingTable(meetingToDelete);
            setMeetings(updatedMeetings);
            setMeetingToDelete(null);
          }
        })
      .catch(error => console.error('Error fetching meetings:', error));
  };

  const cancelDelete = () => {
    setShowModal(false);
  };

  React.useEffect(() => {
      console.log("Meetings were updated.");
  }, [meetings]);

  React.useEffect(() => {
    fetch('/api/get_hosted_meetings_for_user')
      .then(response => response.json())
      .then(data => {
          if (data.status == "success" && data.meetings.length > 0) {
              setMeetings(data.meetings);
            }
          })
      .catch(error => console.error('Error fetching meetings:', error));
    }, [user]);

  return (
    <React.Fragment>
      <h3>Your Hosted Meetings</h3>
       <ModalAlert deleteMeeting={deleteMeeting} cancelDelete={cancelDelete} modalRef={modalRef}/>
       <div id="host-table">
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Book</th>
            <th scope="col">Day</th>
            <th scope="col">Place</th>
            <th scope="col"> Guests</th>
            <th scope="col"></th>
          </tr>
        </thead>
        {meetings.length === 0 ? (
        <tbody><tr><td>No meetings to display.</td></tr></tbody>
      ) : (
        <tbody>
          { meetings
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .map((meeting) => (
            <UserHostMeetingRow key={meeting.id} meeting={meeting} showAlertModal={showAlertModal}/>
          ))}
        </tbody>
      )}
      </table>
      </div>
    </React.Fragment>
  );
}

// row of a hosting table meetings
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

// table for all upcoming meeting for user if user has joined as a guest
function UsersGuestDataContainer(props) {
  const { user, meetingToAdd, meetingToDrop, dropMeetingFromGuest } = props;
  const [meetings, setMeetings] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/get_guest_meetings_for_user')
      .then(response => response.json())
      .then(data => {
          if (data.status == "success" && data.meetings.length > 0) {
              setMeetings(data.meetings);
            }
          })
      .catch(error => console.error('Error fetching meetings:', error));
    }, [user]);

    React.useEffect(() => {
      if (meetingToAdd != null) {
          setMeetings(prevMeetings => [...prevMeetings, meetingToAdd]);
      }
      }, [meetingToAdd]);

      React.useEffect(() => {
        if (meetingToDrop != null) {
          const updatedMeetings = meetings.filter(meeting => meeting.id !== meetingToDrop.id);
          setMeetings(updatedMeetings);
        }
        }, [meetingToDrop]);


  return (
    <React.Fragment>
      <h3>Your Guest Meetings</h3>
      <div id="guest-table">
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Book</th>
            <th scope="col">Where</th>
            <th scope="col">Host</th>
            <th scope="col"> Guests</th>
            <th scope="col"></th>
          </tr>
        </thead>
        
        {meetings.length === 0 ? (<tbody><tr><td>No meetings to display.</td></tr></tbody>
          ) : (
            <tbody>
          { meetings
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .map((meeting) => (
            <UserGuestMeetingRow key={meeting.id} meeting={meeting} dropMeetingFromGuest={dropMeetingFromGuest}/>
          ))}
          </tbody>
        )}
      </table>
      </div>
    </React.Fragment>
  );
}

// row of a guest table
function UserGuestMeetingRow(props) {
  const { meeting, dropMeetingFromGuest } = props;
  const meetingDate = convertDate(meeting.date);

  return (<React.Fragment>
    <tr>
      <td>{meeting.book_title}, <br></br>by {meeting.book_authors}</td>
      <td>{meeting.offline ? meeting.place : 'Zoom'} on {meetingDate}</td>
      <td>{meeting.host_name}</td>
      <td>{meeting.guests_count}/{meeting.max_guests}</td>
      <td>
          <button id={`button--guest-drop-${meeting.id}`} className="btn btn-warning" onClick={() => dropMeetingFromGuest(meeting)}>Drop</button>
      </td>
    </tr>
    </React.Fragment>
  );
}

// confirmation alert for deleting meeting in Host table
function ModalAlert(props) {
  const { deleteMeeting, cancelDelete, modalRef } = props;

  return (<React.Fragment>
      <div className="modal" id="modal-alert" tablindex="-1" role="dialog" aria-labelledby="modalAlert"
      aria-hidden="true" ref={modalRef}>
      <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content">
              <button type="button" className="close" data-bs-dismiss="modal" aria-label="Close" onClick={cancelDelete}>
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

// getting local user TZ and returning localized date
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

// function for showing video from AWS S3
function fetchVideoBlob(meeting_id, path) {
 
  if (!path) {
    console.error(`No file found for meeting_id ${meeting_id}`);
    return;
  }

  window.s3.getObject({ Bucket: 'readmeet-video', Key: path }, (err, data) => {
    if (err) {
      console.error(`Error fetching object for meeting_id ${meeting_id}:`, err);
      return;
    }
    console.log("Video", path, "ID", meeting_id)
    const blob = new Blob([data.Body], { type: 'video/mp4' });
    const videoElement = document.getElementById(`video-${meeting_id}`);
    videoElement.src = URL.createObjectURL(blob);

  });
}