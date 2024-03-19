// parent component for book details
function BookDetailsPage(props) {
    // getting book
    const { state } = props.location;
    const [createMeeting, setCreateMeeting] = React.useState(false);
    const [user, setUser] = React.useState();
    let book = null;

    const [blob, setBlob] = React.useState(null);

    // nav bar built in JS updates user info
    window.updateUserOnDetailsPage = (newUser) => {
      console.log("User state changed, new user: ", newUser)
      setUser(newUser);
    }
    console.log("State", state);
    console.log("Props", props.match.params);

    if ((!state || !state.book) && !props.match.params) {
      return <div>Book details not found.</div>;
    } else if (!state || !state.book) {
      const bookId = props.match.params;

      const getBookUrl = `/api/get_book?book=${bookId}`
      console.log("Book url", getBookUrl)
      fetch(getBookUrl, {
        signal: signal
      })
        .then(response => response.json())
        .then(data => {
          if (data["status"] === "success") {
            book = data[book]; // appending new books to existing list
            console.log("Book is set", book)
          }
        })
        .catch(error => console.error('Error fetching books with search query:', error));

        return () => {
          // cancel the request before component unmounts
          controller.abort();
      };
    } else {
      book = state.book;
      console.log("Title", book.title);
    }
  
    const newMeeting = () => {
      setCreateMeeting(true);
    }

    const setVideoBlob = (vblob) => {
      // console.log("here is video:", vblob)
      // setBlob(vblob);
    }

    React.useEffect(() => {
      // for aborting fetch requests, when user redirects the page
      const controller1 = new AbortController();
  
      fetch('/api/get_current_user', {signal: controller1.signal })
        .then(response => response.json())
        .then(data => {
          setUser(data)
        })
        .catch(error => console.error('Error fetching current user:', error));
       
      // if (window.s3 == null) {
      //    fetch('/api/get_aws_keys')
      //   .then(response => response.json())
      //   .then(data => {
      //     if (data.status == 'success') {
   
      //       AWS.config.update({
      //         region: 'us-east-2',
      //         accessKeyId: data.data[0], // 'your-access-key-id',
      //         secretAccessKey: data.data[1] //'your-secret-access-key',
      //       });
      //       window.s3 = new AWS.S3();
      //   }})
      //   .catch(error => console.error('Error fetching AWS keys:', error));
      // }
      return () => {
        // cancel the request before the component unmounts
        controller1.abort();
      };
    }, []);

    return (
      <React.Fragment>
        <MeetingForm book={book} user={user} handleCreateMeeting={newMeeting} setVideoBlob={setVideoBlob} />
        <div className='container-book-details'>
          <div className="row details-meetings-page">
            <div className="book-details-descr col-5">
              <h2>Details for { book.title }</h2>
                <span className="subtitle">{ book.subtitle } </span>
              <div className="authors"> Written by { book.authors }</div>
              <div className="descr"> { book.description }</div>
              <ReviewsContainer book={book} />
            </div>
            <div className="book-details-img col-7 col-md-auto">
              <img src={ book.image_url } alt={`Picture cover for ${book.title}`}/>
              <BookMeetingDataContainer user={user} book={book} blob={blob} createMeeting={createMeeting} setCreateMeeting={setCreateMeeting} />
            </div>
          </div>
        </div>
      </React.Fragment>
      )
  }
  
  // Table to show all upcoming meetings for picked book
function BookMeetingDataContainer(props) {
  const { book, user, createMeeting, setCreateMeeting, blob } = props;
  const [meetings, setMeetings] = React.useState([]);
  // const [newMeetingData, setNewMeetingData] = React.useState({});
  
  // React.useEffect(() => {
  //   if(user && newMeetingData && blob ) { // && blob
  //     // checking blob size
  //     fetch(blob)
  //     .then((response) => response.blob())
  //     .then((rblob) => {
  //       // Check the size of the Blob
  //       const sizeInBytes = rblob.size;
  //       const sizeInMB = sizeInBytes / (1024 * 1024); // Convert to megabytes
  //       console.log(`Blob size: ${sizeInBytes} bytes (${sizeInMB} MB)`);

  //       const params = {
  //         Bucket: 'readmeet-video',
  //         Key: `${user.user_id}/${newMeetingData.id}/video.mp4`, 
  //         Body: rblob, // Blob data
  //         ContentType: 'video/mp4', // content type
  //       };
  //       // upload the Blob to S3
  //       window.s3.upload(params, (err, data) => {
  //         if (err) {
  //           console.error('Error uploading to S3:', err);
  //         } else {
  //           console.log('Uploaded to S3:', data.Location);
  //         }
  //       });
  //     })
  //     .catch((error) => {
  //       console.error('Error fetching Blob:', error);
  //     });
    
  //   return () => {
  //     setNewMeetingData({});
  //   }
  //   }
  // }, [newMeetingData])

  React.useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch('/api/get_all_meetings_for_book', {
      signal: signal,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "book_id": book.book_id }),
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
  
  React.useEffect(() => {
    if (createMeeting) {
      // reset the state to prevent repeated actions
      setCreateMeeting(false);

      const formInputs = {
        day: document.querySelector('#day').value,
        timezone: document.querySelector('#timezone').value,
        offline: document.querySelector('input[type="radio"]:checked').id,
        language: document.querySelector('#languages').value,
        overview: document.querySelector('#overview').value,
        place: document.querySelector('#autocomplete-address').value,
        max_guests: document.querySelector('#max-guests').value,
        video_url: blob ? true : null
      };

      const resultOfValidForm = isFormValid(formInputs);
      const validForm = (resultOfValidForm.status == "success");
      if (user && user.user_id && validForm) {
        // if input correct and user is logged in, create a new meeting
        document.querySelector('#error-message-new-meeting').innerText = ""; // cleaning modal if there were any error-messages

        fetch('/api/create_meeting', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "book_id": book.book_id, "user_id": user.user_id, "inputs": formInputs }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                console.log("New meeting is created!")

                setMeetings((prevMeetings) => {
                  console.log("Data for new meeting: ", data["new_meeting"])
                  let result = [...prevMeetings, data["new_meeting"]];
                  return result
                });
                
                var modalElement = document.querySelector('#meetingForm');
                var modal = bootstrap.Modal.getInstance(modalElement);
                if (modal) {
                    modal.hide(); // Bootstrap's method
                }
                // sending blob to Amazon S3, triggered by setNewMeetingData
                setNewMeetingData(data["new_meeting"]);
                console.log("Metting data....", data.new_meeting)
              }
              else {
                console.log("Error: meeting was not created")
                document.querySelector('#error-message-new-meeting').innerText = data['message']
              }
          })
          .catch(error => console.error('Error creating new meeting:', error));
        } else {
          // show error message on the form, input is incorrect
          if (resultOfValidForm.message != null) {
            document.querySelector('#error-message-new-meeting').innerText = resultOfValidForm.message;
          } else {
            document.querySelector('#error-message-new-meeting').innerText = "";
          }
        }
    }
  }, [createMeeting]);

  const isFormValid = (formInputs) => {
    // checking date, must be in the future
    const now = new Date();
    const inputDate = new Date(formInputs.day);
    const isDateCorrect = (inputDate > now);
    if (!isDateCorrect) {
      return { "status": "error", "message": "Date of meeting cannot be in the past, please check!" }
    }
    if (formInputs.offline == 'offline') {
      if (formInputs.place == "") {
        return { "status": "error", "message": "If meeting in person, you need to pick a place to meet. Please check." }
      }
    }
    if (formInputs.max_guests == "") { // type: number automatically check for valid number, min 1
      return { "status": "error", "message": "You need to specify maximum of attending guests." }
    }
    
    return { "status": "success" }
  }

  return (
    <React.Fragment>
      <h5>Discussions</h5>
      <button className="btn btn-success" data-bs-toggle="modal" data-bs-target="#meetingForm"> New Meeting </button>
      <table className="table table-hover">
        <thead>
          <tr>
            <th scope="col">Where</th>
            <th scope="col">Host</th>
            <th scope="col">Guests</th>
          </tr>
        </thead>
        <tbody>
          { meetings.sort((a, b) => new Date(a.date) - new Date(b.date)) // Sort meetings by date
          .map((meeting) => (
            <BookMeetingRow key={meeting.id} meeting={meeting} user={user}/>
          ))}
        </tbody>
      </table>
    </React.Fragment>
  );
}

// each row of a meeting table
function BookMeetingRow(props) {
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
    if ((user.user_id == null) || (user.user_id == meeting.host_id) || (guestsCount >= meeting.max_guests)) {
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
    
    }, [meeting]);

  const joinMeeting = () => {
    console.log(`${meeting.id}`)
    if (user.user_id && (user.user_id != meeting.host_id)) {
      fetch('/api/join_meeting', {
        method: 'UPDATE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
      })
        .then(response => response.json())
        .then(data => {
            if (data && data.status == "success") {
                setHideJoinButton(true);
                setHideDropButton(false);
                setGuestsCount(prevGuestsCount => prevGuestsCount + 1);
                meeting.guests_count = meeting.guests_count + 1;
            }
        })
        .catch(error => console.error('Error joining meeting:', error));
    };
    }
    
    const dropMeeting = () => {
      if (user.user_id && (user.user_id != meeting.host_id)) {
        fetch('/api/drop_meeting', {
          method: 'UPDATE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "meeting_id": meeting.id, "user_id": user.user_id }),
        })
          .then(response => response.json())
          .then(data => {
              if (data && data.status == "success") {
                  setHideDropButton(true);
                  setHideJoinButton(false);
                  setGuestsCount(prevGuestsCount => prevGuestsCount - 1);
                  meeting.guests_count = meeting.guests_count - 1;
              }
          })
          .catch(error => console.error('Error dropping meeting:', error));
      };
      }

  // converting date of meeting from UTC to local user's time
  const date = new Date(meeting.date);
  // the user's local timezone
  const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const options = { timeZone: userTimeZone, year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' };
  const localDateString = date.toLocaleDateString('en-US', options);

  return (
    <tr>
      <td>{meeting.offline ? meeting.place : 'Zoom'} on {localDateString}</td>
      <td>{meeting.host_name}</td>
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

// Table for showing reviews (got from Goodreads web-app)
function ReviewsContainer(props) {
  const { book } = props;
  const [reviews, setReviews] = React.useState([]);
  const [noReviewsMessage, setNoReviewsMessage] = React.useState("");

  React.useEffect(() => {
    
    fetch('/api/get_reviews_for_book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "book_isbn": book.ISBN }),
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
            console.log(data)
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
              <li className="review"> <Review key={index} review={review}/></li>
            ))
          }
        </ul>
      </div>
    </React.Fragment>
  )
}

// each review of Review table
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
      </div>
    </React.Fragment>
  )
}

// form for creating a new meeting
function MeetingForm(props) {
  const { book, user, handleCreateMeeting, setVideoBlob } = props;
  const errorMessage = "";
  const [expanded, setExpanded] = React.useState(false);
  const [mediaVisible, setMediaVisible] = React.useState(false);
  const [hideCreateButton, setHideCreateButton] = React.useState(true);

  // switching labels on yelp search button
  React.useEffect(() => {
    const text = expanded ? "Hide Yelp search" : "Or let's look for a place!";
    document.querySelector('#search-yelp-form').innerText = text;
  }, [expanded]);

  // for expanding yelp search form 
  const toggleYelpForm = (env) => {
    env.preventDefault();
    console.log("Yelp form toggled: ", expanded);
    setExpanded(!expanded);
  };

  const toggleMediaRecorder = (env) => {
    env.preventDefault();
    console.log("Media Recorder toggled: ", mediaVisible);
    setMediaVisible(!mediaVisible);
    document.getElementById("open-media-recorder").textContent = mediaVisible ? "Start Recording" : "Cancel Video Recording";
  };

  const yelpError = () => {
    document.querySelector('#error-message-yelp').innerText = "No information on Yelp for your zipcode";
    setExpanded(false);
  };

  const updateAddressInForm = (name, address) => {
    document.querySelector('#autocomplete-address').value = `${name}, ${address}`;
    setExpanded(false);
  };

  React.useEffect(() => {

    if (user && user.user_id != null) {
      setHideCreateButton(false);
    } else {
      setHideCreateButton(true);
    }
  }, [user]);
  

  const handleSubmit = (event) => {
    event.preventDefault();
    // mediaClose();
    handleCreateMeeting();
    mediaCloseOnSubmit();
  };

  const [zoomMeeting, setZoomMeeting] = React.useState(false);

  const mediaClose = () => {
    setMediaVisible(false);
    setVideoBlob(null);
  }

  const mediaCloseOnSubmit = () => {
    setMediaVisible(false);
  }

 
  return (
    <React.Fragment>
      <div className="modal fade hidden" id="meetingForm" tabIndex="-1" role="dialog" aria-labelledby="meetingForm" aria-hidden="true">
        <div className="modal-dialog modal-dialog-centered" role="document">
            <div className="modal-content meeting">
                <button type="button" className="close" data-bs-dismiss="modal" aria-label="Close" onClick={mediaClose}>
                    <span aria-hidden="true">&times;</span>
                </button>
                <div className="modal-body meetingFormBody">
                    <h3 className="modal-title">New Meeting for {book.title} </h3>
                    <div className="message" id="error-message-signup"></div>
                    
                    <form id="create-meeting-form" className="signin" method="POST">
                      <div className="message" id="error-message-new-meeting">{errorMessage}</div>
                        <div className="element">
                            <label htmlFor="day">
                                Chosee day and time: <span className="red-indicator">*required</span>
                            </label>
                            <input
                                className="input myInput"
                                type="datetime-local"
                                id="day"
                                name="day"
                                required 
                                alt="pick a meeting date here"/>
                        </div>

                        <div className="element">
                          <select id="timezone">

                            <option value="UTC-12">(UTC-12:00) International Date Line West</option>
                            <option value="UTC-11">(UTC-11:00) Coordinated Universal Time-11</option>
                            <option value="UTC-10">(UTC-10:00) Hawaii</option>
                            <option value="UTC-9">(UTC-09:00) Alaska</option>
                            <option value="UTC-8">(UTC-08:00) Pacific Time (US & Canada)</option>
                            <option value="UTC-7">(UTC-07:00) Arizona</option>
                            <option value="UTC-6">(UTC-06:00) Central Time (US & Canada)</option>
                            <option value="UTC-5">(UTC-05:00) Eastern Time (US & Canada)</option>
                            <option value="UTC-4">(UTC-04:00) Atlantic Time (Canada)</option>
                            <option value="UTC-3">(UTC-03:00) Greenland</option>
                            <option value="UTC-2">(UTC-02:00) Mid-Atlantic</option>
                            <option value="UTC-1">(UTC-01:00) Azores</option>
                            <option value="UTC">(UTC) Coordinated Universal Time</option>
                            <option value="UTC+1">(UTC+01:00) Central European Time</option>
                            <option value="UTC+2">(UTC+02:00) Eastern European Time</option>
                            <option value="UTC+3">(UTC+03:00) Moscow Time</option>
                            <option value="UTC+3:30">(UTC+03:30) Iran Time</option>
                            <option value="UTC+4">(UTC+04:00) Gulf Standard Time</option>
                            <option value="UTC+4:30">(UTC+04:30) Afghanistan</option>
                            <option value="UTC+5">(UTC+05:00) Pakistan Lahore Time</option>
                            <option value="UTC+5:30">(UTC+05:30) India Standard Time</option>
                            <option value="UTC+5:45">(UTC+05:45) Nepal Time</option>
                            <option value="UTC+6">(UTC+06:00) Bangladesh Standard Time</option>
                            <option value="UTC+6:30">(UTC+06:30) Cocos Islands Time</option>
                            <option value="UTC+7">(UTC+07:00) Indochina Time</option>
                            <option value="UTC+8">(UTC+08:00) China Taiwan Time</option>
                            <option value="UTC+8:45">(UTC+08:45) Australia Eucla Time</option>
                            <option value="UTC+9">(UTC+09:00) Japan Standard Time</option>
                            <option value="UTC+9:30">(UTC+09:30) Australia Central Time</option>
                            <option value="UTC+10">(UTC+10:00) Australia Eastern Time</option>
                            <option value="UTC+10:30">(UTC+10:30) Lord Howe Island Time</option>
                            <option value="UTC+11">(UTC+11:00) Srednekolymsk Time</option>
                            <option value="UTC+11:30">(UTC+11:30) Norfolk Island Time</option>
                            <option value="UTC+12">(UTC+12:00) New Zealand Standard Time</option>
                            <option value="UTC+12:45">(UTC+12:45) Chatham Islands Time</option>
                            <option value="UTC+13">(UTC+13:00) Phoenix Islands Time</option>
                            <option value="UTC+14">(UTC+14:00) Line Islands Time</option>

                          </select>
                        </div>

                        <div className="radio-buttons">
                            <input className="form-check-input" type="radio" name="meetingOption" id="zoom" checked={zoomMeeting} onChange={() => setZoomMeeting(true)} alt="radio button to pick a zoom meeting"/>
                            <label className="form-check-label" htmlFor="zoom">
                              Zoom
                            </label>
                            
                            <input className="form-check-input" type="radio" name="meetingOption" id="offline" checked={!zoomMeeting} onChange={() => setZoomMeeting(false)} alt="radio button to pick a real life meeting"/>
                            <label className="form-check-label" htmlFor="offline">
                              Meeting-In-Person <span className="red-indicator">*required</span>
                            </label>
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
                        <label htmlFor="max-guests">
                                Maximum attending guests<span className="red-indicator">*required</span>
                        </label>
                          <input type="number" id="max-guests" required min="1" step="1" alt="put a number of guests that allowed to come"/>
                        </div>
                        <div className="element">
                        <label htmlFor="place">
                                Add address and name for a place to meet:{zoomMeeting ? null : <span className='red-indicator'>*required</span>}
                        </label>
                          <input type="text" id="autocomplete-address" alt="put a meeting address here or find a place on yelp lower on the form for address autocompletion "/>
                        </div>
                        <div>
                          <button id="open-media-recorder" onClick={toggleMediaRecorder}>Start Video Note</button>
                        </div>
                        {mediaVisible && (<VideoRecorder setVideoBlob={setVideoBlob}/>)}
                        <div>
                          <button id="search-yelp-form" onClick={toggleYelpForm}>Or let's look for a place!</button>
                        </div>
                        <div className="message" id="error-message-yelp"></div>
                        {expanded && (
                          <YelpSearchForm expanded={expanded} yelpError={yelpError} updateAddressInForm={updateAddressInForm}/>
                        )}
                        
                        <button className="btn btn-success" id="meeting-create"  disabled={hideCreateButton} onClick={handleSubmit}>Create!</button>
                    </form>
                    
                </div>
            </div>
        </div>
    </div>
    </React.Fragment>
  )
}

// Form for searching places on Yelp
function YelpSearchForm(props) {
  const { expanded, yelpError, updateAddressInForm } = props;
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
          const modalContentScrollY = modalContentElement.scrollTop;
        if ( // changed logic of if statement to implement for modal popup scroll
          // was modalContentHeight - modalContentScrollY + 300 >= modalContentElement.offsetHeight
          modalContentScrollY + modalContentElement.offsetHeight + 300 >= modalContentHeight
        ) {
          console.log("Page before increment: ", page, "scrolled 1 time")
          setPage(prevPage => prevPage + 1);
          setIsLoading(true); 
        }
        isScrolling = false;
      }, 300); // 300ms delay
    }
  };

  const debouncedScrollDown = debounce(scrollDown, 400);

  React.useEffect(() => {
      
      if (expanded) {
          const modalContentElement = document.querySelector('.meetingFormBody');
          modalContentElement.addEventListener('scroll', debouncedScrollDown);
          return () => modalContentElement.removeEventListener('scroll', debouncedScrollDown);
      }  
  }, [expanded, debouncedScrollDown]);
  
  React.useEffect(() => {
      const controller = new AbortController();
      const signal = controller.signal;
      console.log("UseEffect new search: ", newSearch, "page: ", page);
      
      fetch("/api/get_yelp_places", {
          signal: signal,
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ "place": newSearch, "page": page }),
      })
        .then(response => response.json())
        .then(data => {
          if (data["status"] === "success") {
            document.querySelector('#error-message-yelp').innerText = "";
              if (!clean) {
                  setPlaces(prevPlaces => [...prevPlaces, ...data["places"]]); 
                  setIsLoading(false);
              } else {
                  setPlaces(data["places"]);
                  setPage(0);
                  setClean(false);
              }
          } else {
            yelpError(true);
          }
        })
        .catch((error) => {
          console.error('Error getting businesses from Yelp API:', error)
          yelpError(true);
        });
  
        return () => {
          // cancel the request before component unmounts
          controller.abort();
      };
    }, [page, newSearch]);

  
  return (<React.Fragment>
          <div className="yelp-form">
            <div className="element">
            You can look for a place to meet here:
              <input type="search" id="search-yelp" alt="put a word or phrase for yelp search here for choosing address to meet"/>
              <button id="search-yelp-button" onClick={handleYelpSearch}>Search</button>
            </div> { places.map((place, index) => (
              <div className="container">
              <YelpRow key={place.id} place={place} index={index} updateAddressInForm={updateAddressInForm}/>
              </div>
            ))}
              {isLoading && <p>Loading...</p>}
          </div>
        </React.Fragment>
  )}

// each row of yelp result table
function YelpRow(props) {
  const { place, index, updateAddressInForm } = props;

  return (<React.Fragment>
    <div className="row yelp-row">
      <div className="col-4 square-image" onClick={() => updateAddressInForm(place.name, place.address)}>
          <img src={place.image} alt="Image for picked place on yelp"></img>
      </div>
      <div className="col-8 d-flex yelp-text">
          <span className="yelp-name" onClick={() => updateAddressInForm(place.name, place.address)}>{index + 1}. {place.name}<p className="yelp-rating">{place.rating}&#9733;</p></span>
          <span className="yelp-address">{place.address}</span>
          <div className="yelp-url"><a link={place.url}>Check hours and reviews here</a></div>
      </div>
    </div>
  </React.Fragment>)
}


function VideoRecorder(props) {
  const { setVideoBlob } = props;

  const [recording, setRecording] = React.useState(false);
  const [videoURL, setVideoURL] = React.useState(null);
  const [cameraStarted, setCameraStarted] = React.useState(false);
  const mediaRecorderRef = React.useRef(null);
  const videoRef = React.useRef(null);

  React.useEffect(() => {
    if(videoURL){
      console.log("New blob was recorded")
      setVideoBlob(videoURL);
      console.log(videoURL)
    }
  }, [videoURL])

  const mediaStreamConstraints = {
    audio: true,
    video: true,
  };

  const startRecording = (ev) => {
    ev.preventDefault();

    if (!cameraStarted) {
      // camera hasn't started yet, need to start it now
      navigator.mediaDevices
        .getUserMedia(mediaStreamConstraints)
        .then((resultingMediaStream) => {
          if (videoRef.current && 'srcObject' in videoRef.current) {
            videoRef.current.srcObject = resultingMediaStream;
          }
          setCameraStarted(true);
        })
        .catch((error) => {
          console.error('Error accessing audio and video:', error);
        });
        const stopButton = document.getElementById("stop-recording");
        stopButton.style.display = "inline";
        document.getElementById("start-recording").innerText = 'Start';
        
      } else {
      // camera has already started, start recording
      const mediaRecorder = new MediaRecorder(videoRef.current.srcObject);
      mediaRecorderRef.current = mediaRecorder;
      const chunks = [];

      mediaRecorder.ondataavailable = (ev) => {
        chunks.push(ev.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'video/mp4' });
        setVideoURL(URL.createObjectURL(blob));
      };

      mediaRecorder.start();
      setRecording(true);
    }
  };

  const stopRecording = (ev) => {
    ev.preventDefault();

    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  return (
    <div>
      <video id="video-block" ref={videoRef} autoPlay controls />
      <button id="start-recording" onClick={startRecording} disabled={recording}>
        Start Recording
      </button>
      <button id="stop-recording" onClick={stopRecording} disabled={!recording}>
        Stop
      </button>
      {videoURL && (
        <video id="your-video" src={videoURL} autoPlay controls>
          Your browser doesn't support video playback.
        </video>
      )}
    </div>
  );
}