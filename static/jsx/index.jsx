// creates a table displaying upcoming meetings
function MeetingDataContainer() {
    const [meetings, setMeetings] = React.useState([]);
    const [user, setUser] = React.useState();

    window.updateUser = (newUser) => {
      setUser(newUser);
    }
  
    React.useEffect(() => {
        fetch('/api/get_current_user')
          .then(response => response.json())
          .then(data => {
            setUser(data)
            if ((data.user_id != "") && (data.user_id != null)) {
                console.log("No user")
                window.userIsLoggedIn();
            }
            else {
                console.log("User loged in")
                window.userIsLoggedOut();
            }
          })
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
function MeetingRow(props) {
    const { meeting, user } = props;
    const [host, setHost] = React.useState({});
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
      
      if ((user.user_id == meeting.host_id) || (guestsCount >= meeting.max_guests)) {
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

      // if (user.user_id && (user.user_id != meeting.host_id)) { // check that user exists, has id and he is not a host
      //     fetch('/api/get_user_by_id', {
      //         method: "POST",
      //         headers: { "Content-Type": "application/json" },
      //         body: JSON.stringify({ "host_id": meeting.host_id }),
      //       })
      //         .then(response => response.json())
      //         .then(data => setHost(data))
      //         .catch(error => console.error('Error fetching host:', error));
      // } else {
      //     setHideJoinButton(true);
      //     setHideDropButton(true);
      // };
      
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

    return (
      <tr>
        <td>{book.title}, <br></br>by {book.authors}</td>
        <td>{meeting.date}</td>
        <td>{meeting.place}</td>
        <td>{meeting.offline}</td>
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


function CarouselDataContainer() {
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
              <CarouselItems key={index} books={books} isActive={index===1}/> // if index is 1, it will set block to active for carousel
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
  const { books, isActive } = props;
  return (
    <React.Fragment>
      <div className={`carousel-item ${isActive ? 'active' : ''}`}>
        <div className="carousel-img-block d-flex justify-content-between">
          { books.map((book) => (
            
            <div key={book.ISBN} className="carousel-image">
              <ReactRouterDOM.Link key={book.ISBN} pathname={`{/books/${book.ISBN}}`} to={{
            pathname: `/books/${book.ISBN}`,
            state: { book }
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