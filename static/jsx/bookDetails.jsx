
function BookDetailsPage(props) {
    // getting ISBN
    const { bookId } = ReactRouterDOM.useParams();
    const { state } = props.location;
    const [books, setBooks] = React.useState([]);
  
    if (!state || !state.book) {
      return <div>Book details not found.</div>;
    }
  
    const book = state.book;

    return (
      <React.Fragment>
        <MeetingForm book={book}/>
        <div className='container-book-details'>
          <div className="row">
            <div className="book-details-descr col-7">
              <h2>Details for { book.title }</h2>
                <span className="subtitle">{ book.subtitle } </span>
              <div className="authors"> Written by { book.authors }</div>
              <div className="descr"> { book.description }</div>
              <ReviewsContainer book={book} />
            </div>
            <div className="book-details-img col-5 col-md-auto">
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
      const controller = new AbortController();
      const signal = controller.signal;
  
        fetch('/api/get_current_user', {signal: signal })
          .then(response => response.json())
          .then(data => {
            setUser(data)
          })
          .catch(error => console.error('Error fetching current user:', error));
  
          return () => {
            // cancel the request before component unmounts
            controller.abort();
        };
  
      }, []);
  
  
    React.useEffect(() => {
      const controller = new AbortController();
      const signal = controller.signal;
  
      fetch('/api/get_all_meetings_for_book', {
        signal: signal,
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
  
        return () => {
          // cancel the request before component unmounts
          controller.abort();
      };
  
    }, [user]);
  
    
  
    // const createMeeting = () => {
    //   if (user.user_id) {
    //     fetch('/api/create_meeting', {
    //       method: 'POST',
    //       headers: { 'Content-Type': 'application/json' },
    //       body: JSON.stringify({ "book_id": book.ISBN, "user_id": user.user_id }),
    //     })
    //       .then(response => response.json())
    //       .then(data => {
    //           if (data && data.status == "success") {
    //             setMeetings(prevMeetings => [...prevMeetings, ...data["meeting"]]);
    //           }
    //       })
    //       .catch(error => console.error('Error creating meeting:', error));
    //     };
    //   }
  
    return (
      <React.Fragment>
        <h5>Discussions</h5>
        <button className="btn btn-success" data-bs-toggle="modal" data-bs-target="#meetingForm"> New Meeting </button>
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
  
  
  function ReviewsContainer(props) {
    const { book } = props;
    const [reviews, setReviews] = React.useState([]);
    const [noReviewsMessage, setNoReviewsMessage] = React.useState("");
    let message = "";

    React.useEffect(() => {
      
      fetch('/api/get_reviews_for_book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "book_id": book.ISBN }),
      })
        .then(response => response.json())
        .then(data => {
            if (data && data.status == "success") {
              console.log("There are some reviews")
              setNoReviewsMessage("");
              setReviews(data["reviews"]);
            }
            else {
              console.log("No reviews")
              if (data.code == 204) {
                setNoReviewsMessage(data.message);
              }
            }
        })
        .catch(error => console.error('Error getting goodreads reviews for a book:', error));
        
    }, [])
  
    return (
      <React.Fragment>
        <div className="reviews">
          <h3>Reviews</h3>
          <h6>from Goodreads</h6>
          <ul>
            { (noReviewsMessage.length != 0) ? (<div>{ noReviewsMessage }</div>) : 
              reviews.map((review, index) => (
                <li> <Review key={index} review={review}/></li>
              ))
            }
          </ul>
        </div>
      </React.Fragment>
    )
  }
  
  function Review(props) {
    const { review } = props;
    const [expanded, setExpanded] = React.useState(false);
    const [overflowing, setOverflowing] = React.useState(false);
    // for expanding text review
    const toggleExpansion = () => {
      setExpanded(!expanded);
    };
  
    const textClass = expanded ? 'expanded' : 'review-text';
    const expandedText = React.useRef(null);

    React.useEffect(() => {
      if (expandedText.current) {
        if (expandedText.current.scrollHeight > (expandedText.current.clientHeight + 4)) {
          setOverflowing(true);
        }
      }
    }, [])
  
    return (
      <React.Fragment>
        <div>
          <div className="review-name">
            { review.name }
          </div>
          <div className={textClass} ref={expandedText} dangerouslySetInnerHTML={{ __html: review.text }}>
          </div>
          { overflowing ? <button className="read-more-btn" onClick={toggleExpansion}>
              {expanded ? 'Hide' : 'Read More...'}
            </button> : "" }
            {/* <button className="read-more-btn" onClick={toggleExpansion}>
              {expanded ? 'Hide' : 'Read More...'}
            </button> */}
        </div>
      </React.Fragment>
    )
  }
  
  function MeetingForm(props) {
    const { book } = props;
  
    const currentDate = () => {
      const now = new Date();
  
      // Get the current date and time components
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0'); // Month is zero-indexed
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
  
      // Format the date and time in the desired format
      const formattedDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
      return formattedDateTime
    }
  
    const [expanded, setExpanded] = React.useState(false);
    // for expanding yelp search form 
  
    const toggleYelpForm = () => {
      setExpanded(!expanded);
    }
  
    return (
      <React.Fragment>
        <div className="modal fade hidden" id="meetingForm" tabIndex="-1" role="dialog" aria-labelledby="meetingForm" aria-hidden="true">
          <div className="modal-dialog modal-dialog-centered" role="document">
              <div className="modal-content meeting">
                  <button type="button" className="close" data-bs-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                  </button>
                  <div className="modal-body meetingFormBody">
                      <h3 className="modal-title">New Meeting for {book.title} </h3>
                      <div className="message" id="error-message-signup"></div>
                      
                      <form id="create-meeting-form" className="signin" method="POST">
                          <div className="element">
                              <label htmlFor="day">
                                  Chosee day and time:
                              </label>
                              <input
                                  className="input myInput"
                                  type="datetime-local"
                                  id="day"
                                  name="day"
                                  min={currentDate}
                                  required />
                          </div>
                          <div className="radio-buttons">
                          {/* <div className="form-check"> */}
                              <input className="form-check-input" type="radio" name="meetingOption" id="zoom" />
                              <label className="form-check-label" htmlFor="zoom">
                                Zoom
                              </label>
                              {/* </div> */}
                              {/* <div className="form-check"> */}
                              <input className="form-check-input" type="radio" name="meetingOption" id="offline" defaultChecked />
                              <label className="form-check-label" htmlFor="offline">
                                Meeting-In-Person
                              </label>
                              {/* </div> */}
                          </div>
                          <div className="element">
                              <label htmlFor="languages">
                                  Language
                              </label>
                              <select className="form-select" id="languages" name="languages">
                                <option value="EN">English</option>
                                <option value="ZH">Chinese - 中文</option>
                                <option value="ES">Spanish - español</option>
                                <option value="HI">Hindi - हिन्दी</option>
                                <option value="AR">Arabic - العربية</option>
                                <option value="PT">Portuguese - português</option>
                                <option value="BN">Bengali - বাংলা</option>
                                <option value="RU">Russian - русский</option>
                                <option value="JA">Japanese - 日本語</option>
                                <option value="PA">Punjabi - ਪੰਜਾਬੀ</option>
                            </select>
                          </div>
                          <div className="element">
                              <label htmlFor="overview">
                                  Few words (If you would like to share an agenda or your thoughts)
                              </label>
                              <textarea className="input myInput" id="overview" name="overview" wrap="soft" />
                          </div>
                          <div className="element">
                          <label htmlFor="place">
                                  Place to meet
                          </label>
                            <input type="text" id="autocomplete"/>
                          </div>
                          <div>
                            <button id="search-yelp-form" onClick={toggleYelpForm}>Let's look for a place!</button>
                          </div>
                          {expanded && (
                            <YelpSearchForm expanded={expanded}/>
                          )}
                          
                          <button id="user-signup">Create!</button>
                      </form>
                      
                  </div>
              </div>
          </div>
      </div>
      </React.Fragment>
    )
  }

  
  function YelpSearchForm(props) {
    const { expanded } = props;
    const [places, setPlaces] = React.useState([]);
    const [newSearch, setNewSearch] = React.useState("");
    const [page, setPage] = React.useState(0);
    const [isLoading, setIsLoading] = React.useState(false);
    const [clean, setClean] = React.useState(false);

    const handleYelpSearch = (event) => {
      event.preventDefault();
      // triggers new Yelp search with these parameters
      const input = document.getElementById('search-yelp').value;
      setNewSearch(input);
      setClean(true);
      console.log("New search set:", newSearch);
    };

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
        console.log("Scrolling: ", isScrolling)
      if (!isScrolling) {
        setTimeout(() => {
            isScrolling = true;
            const modalContentElement = document.querySelector('.meetingFormBody');
            const modalContentHeight = modalContentElement.scrollHeight;
            console.log("modalContentHeight:", modalContentHeight)
            const modalContentScrollY = modalContentElement.scrollTop;
            console.log("modalContentScrollY:", modalContentScrollY)
          if ( // changed logic of if statement to implement for modal popup scroll
            // modalContentHeight - modalContentScrollY + 300 >= modalContentElement.offsetHeight
            modalContentScrollY + modalContentElement.offsetHeight + 300 >= modalContentHeight
          ) {
            console.log("PAGE before increment: ", page)
            console.log("Scrolled ONCE");
            
            setPage(prevPage => prevPage + 1);
            setIsLoading(true); 
            
            console.log("PAGE: ", page)
            console.log(isLoading)
          }
          isScrolling = false;
        }, 300); // 300ms delay
      }
    };
  
    const debouncedScrollDown = debounce(scrollDown, 400);

    React.useEffect(() => {
        console.log("EXPANDED: ", expanded);
        if (expanded) {
            console.log("LISTENER ADDED")
            const modalContentElement = document.querySelector('.meetingFormBody');
            modalContentElement.addEventListener('scroll', debouncedScrollDown);
            return () => modalContentElement.removeEventListener('scroll', debouncedScrollDown);
        }  
    }, [expanded, debouncedScrollDown]);
    
    React.useEffect(() => {
        const controller = new AbortController();
        const signal = controller.signal;
        console.log("UseEffect PAGe: ", page);
        console.log("UseEffect new search: ", newSearch);
       
        fetch("/api/get_yelp_places", {
            signal: signal,
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "place": newSearch, "page": page }),
        })
          .then(response => response.json())
          .then(data => {
            if (data["status"] === "success") {
                if (!clean) {
                    setPlaces(prevPlaces => [...prevPlaces, ...data["places"]]); 
                    setIsLoading(false);
                } else {
                    setPlaces(data["places"]);
                    setPage(0);
                    setClean(false);
                }
            }
          })
          .catch(error => console.error('Error getting businesses from Yelp API:', error));
    
          return () => {
            // cancel the request before component unmounts
            controller.abort();
        };
      }, [page, newSearch]);

    
    return (<React.Fragment>
            <div className="yelp-form">
              <p>Yelp Search!</p>
              <div className="element">
                <input type="search" id="search-yelp" />
                <button id="search-yelp-button" onClick={handleYelpSearch}>Search</button>
              </div> { places.map((place, index) => (
                <div className="container">
                <YelpRow key={place.id} place={place} index={index}/>
                </div>
              ))}
               {isLoading && <p>Loading...</p>}
            </div>
          </React.Fragment>
    )}

  
  function YelpRow(props) {
    const { place, index } = props;
    // console.log(JSON.stringify(place.id))

    return (<React.Fragment>
      <div className="row yelp-row">
        <div className="col-4 square-image">
            <img src={place.image}></img>
        </div>
        <div className="col-8 d-flex yelp-text">
            <span className="yelp-name">{index + 1}. {place.name}<p className="yelp-rating">{place.rating}&#9733;</p></span>
            <span className="yelp-address">{place.address}</span>
            <div className="yelp-url"><a link={place.url}>Check hours and reviews here</a></div>
        </div>
      </div>
    </React.Fragment>)
  }