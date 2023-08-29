function BooksSearchContainer() {
  const [page, setPage] = React.useState(0);
  const [books, setBooks] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);


  let isScrolling = false;
  // slowing down scroll calls, debounce implementation (found on StackOverflow)
  const debounce = (func, delay) => {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => {
        func.apply(this, args);
      }, delay);
    };
  };

  const scrollDown = () => {
    if (!isScrolling) {
      isScrolling = true;
      setTimeout(() => {
        if (
          window.innerHeight + window.scrollY >= document.body.offsetHeight - 600
        ) {
          console.log("Scrolled ONCE");
          setPage(prevPage => prevPage + 1);
          setIsLoading(true);
        }
        isScrolling = false;
      }, 300); // 300ms delay
    }
  };

  const debouncedScrollDown = debounce(scrollDown, 300);

  React.useEffect(() => {
    window.addEventListener('scroll', debouncedScrollDown);
    return () => window.removeEventListener('scroll', debouncedScrollDown);
  }, [debouncedScrollDown]);


  React.useEffect(() => {
    // Getting url that is already rendered with search parameters
    const queryParamsString = window.location.search;

    // constructing fetch request with current params and page, starting is 0
    const newUrl = `/api/get_books${queryParamsString}&page=${page}`

    fetch(newUrl)
      .then(response => response.json())
      .then(data => {
        if (data["status"] === "success") {
          setIsLoading(false);
          setBooks(prevBooks => [...prevBooks, ...data["books"]]); // Append new books to existing list
        }
      })
      .catch(error => console.error('Error fetching books with search query:', error));
  }, [page]);
  
  return (
    <React.Fragment>
      <h4>Results</h4>
      <div className="search-all-books d-flex">
        {books.map((book, index) => (
          <Book key={index} book={book} />
        ))}
        {isLoading && <p>Loading...</p>}
      </div>
    </React.Fragment>
  );
  }


  function Book(props) {
    const { book } = props;
    const [showDetails, setShowDetails] = React.useState(false);
    
    function generateRandomHue() {
      return Math.floor(Math.random() * 361); // Generates random hue between 0 and 360
    }
  
    return (
      <React.Fragment>
        <ReactRouterDOM.Link
            to={{
              pathname: `/books/${book.ISBN}`,
              state: { book }
            }}>
        {/* <ReactRouterDOM.Link to={`/books/${book.ISBN}`}> */}
        <div className="search-book-div">
          <div className="book-image-background" style={{ backgroundColor: `hsl(${generateRandomHue()}, 40%, 95%)`}}></div>
          <div className="image-block">
            <img src={book.image} className="img-fluid" alt={`Picture cover for ${book.title}`} />
          </div>
          <div className="book-contents">
            <div className="title">{book.ISBN}</div>
            {/* render subtitle only if present in the book */}
            {/* { book.subtitle ? <span className="subtitle"><br></br>{book.subtitle}</span> : null } */}
            <div className="authors">{book.title}</div>
          </div>
        </div>
        {/* { showDetails && <BookDetails key={book.ISBN} book={book} /> } */}
        </ReactRouterDOM.Link>
      </React.Fragment>
    );
  }


function BookDetailsPage(props) {
  // getting ISBN
  const { bookId } = ReactRouterDOM.useParams();
  const { state } = props.location;
  const [books, setBooks] = React.useState([]);

  if (!state || !state.book) {
    return <div>Book details not found.</div>;
  }

  const book = state.book;
  console.log(JSON.stringify(book));
  return (
    <React.Fragment>
      <div className='container-book-details'>
        <div className="row">
          <div className="book-details-descr col 7">
            <h2>Details for { book.title }</h2>
              <span className="subtitle">{ book.subtitle } </span>
            <div className="authors"> Written by { book.authors }</div>
            <div className="descr"> { book.description }</div>
          </div>
          <div className="book-details-img col 5 col-md-auto">
            <img src={ book.image }/>
            <BookMeetingDataContainer book={book}/>
          </div>
        </div>
      </div>
    </React.Fragment>
    )
}

function BookMeetingDataContainer(props) {
  const { book } = props;
  const [meetings, setMeetings] = React.useState([]);
  const [user, setUser] = React.useState();


  React.useEffect(() => {
      fetch('/api/get_current_user')
        .then(response => response.json())
        .then(data => {
          setUser(data)
          // if ((data.user_id != "") && (data.user_id != null)) {
          //     console.log("No user")
          //     window.userIsLoggedIn();
          // }
          // else {
          //     console.log("User loged in")
          //     window.userIsLoggedOut();
          // }
        })
        .catch(error => console.error('Error fetching current user:', error));
    }, []);


  React.useEffect(() => {
    fetch('/api/get_all_meetings_for_book', {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "book_id": book.ISBN }),
    })
      .then(response => response.json())
      .then(data => {
          if (data["status"] == "success") {
              setMeetings(data["meetings"]);
            } else {
            console.log(data["message"]) 
          }})
      .catch(error => console.error('Error fetching meetings:', error));
  }, [user]);

  return (
    <React.Fragment>
      <h5>Discussions</h5>
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Day</th>
            <th scope="col">Place</th>
            <th scope="col">Host</th>
            <th scope="col">Guests</th>
          </tr>
        </thead>
        <tbody>
          { meetings.map((meeting) => (
            <BookMeetingRow key={meeting.id} meeting={meeting} user={user} book={book}/>
          ))}
        </tbody>
      </table>
    </React.Fragment>
  );
}

// each row of a meeting table
function BookMeetingRow(props) {
  const { meeting, user, book } = props;
  const [host, setHost] = React.useState({});
 
  // for correct displaying join meeting button and drop meeting button
  const [hideJoinButton, setHideJoinButton] = React.useState(true);
  const [hideDropButton, setHideDropButton] = React.useState(true);

  const [guestsCount, setGuestsCount] = React.useState(meeting.guests_count);

  React.useEffect(() => {
    if (guestsCount >= meeting.max_guests) {
      setHideJoinButton(true);
    } else {
      setHideJoinButton(false);
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

    if (user.user_id && (user.user_id != meeting.host_id)) { // check that user exists, has id and he is not a host
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
      <td>{meeting.date}</td>
      <td>{meeting.place}</td>
      <td>{host.name}</td>
      <td>{guestsCount}/{meeting.max_guests}</td>
      <td>
          <button id="button-join" className="btn btn-success" disabled={hideJoinButton} onClick={joinMeeting}>+</button>
      </td>
      <td>
          <button id="button-drop" className="btn btn-warning" disabled={hideDropButton} onClick={dropMeeting}>-</button>
      </td>
    </tr>
  );
}
