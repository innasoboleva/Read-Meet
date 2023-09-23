// Book search table
function BooksSearchContainer() {
  const [page, setPage] = React.useState(0);
  const [books, setBooks] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);

  const [status, setStatus] = React.useState("loading"); // if no book were found, status == error, if found == success

  // setting the same height for each book (div) for each row on the screen
  const containerRef = React.useRef(null);

  React.useEffect(() => {
    function setRowHeights() {
      
      if (containerRef.current) {
        const container = containerRef.current;
        const divs = container.querySelectorAll('.search-book-div');

        const containerWidth = container.clientWidth; // Width of the container
        const divWidth = 260; // Fixed width of each div
        const divsPerRow = Math.floor(containerWidth / divWidth); // Calculate divs per row
      
        let maxHeight = 0;
        divs.forEach((div, index) => {
          // Set the min-height to ensure a constant height
          div.style.minHeight = `${maxHeight}px`;
    
          const height = div.clientHeight;
          if (height > maxHeight) {
            maxHeight = height;
          }
    
          // when all divs are done in the row, set the height for each
          if ((index + 1) % divsPerRow === 0) {
            for (let i = index - divsPerRow + 1; i <= index; i++) {
              divs[i].style.minHeight = `${maxHeight}px`;
            }
            maxHeight = 0;
          }
        });
      } 
    }

    setRowHeights();
    // recalculates heights on window resize
    window.addEventListener('resize', setRowHeights);

    // Clean up the event listener on component unmount
    return () => {
      window.removeEventListener('resize', setRowHeights);
    };
  }, [status, books]);


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
      setTimeout(() => {
        isScrolling = true;
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
    const controller = new AbortController();
    const signal = controller.signal;
    // Getting url that is already rendered with search parameters
    const queryParamsString = window.location.search;

    // constructing fetch request with current params and page, starting is 0
    const newUrl = `/api/get_books${queryParamsString ? queryParamsString + '&' : '?'}page=${page}`
    console.log("URL: ", newUrl)
    fetch(newUrl, {
      signal: signal
     })
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data["status"] === "success") {
          setIsLoading(false);
          setBooks(prevBooks => [...prevBooks, ...data["books"]]); // appending new books to existing list
          setStatus("success");
        } else {
          setStatus("error");
        }
      })
      .catch(error => {
        console.error('Error fetching books with search query:', error);
        setStatus("error");
      });

      return () => {
        // cancel the request before component unmounts
        controller.abort();
    };
  }, [page]);
  
  return (
    <React.Fragment>
      <h4>Results</h4>
      { status == "success" ? (<div ref={containerRef} className="search-all-books d-flex">
        {books.map((book, index) => (
          <Book key={index} book={book} />
        ))}
        {isLoading && <p>Loading...</p>}
      </div>
      ) : status == "error" ? (
        <React.Fragment>
          <div>No books were found.</div>
        </React.Fragment>
      ) : (
        <p>Loading...</p>
      )}
    </React.Fragment>
  );
}

// representing each book
function Book(props) {
  const { book } = props;

  function generateRandomHue() {
    return Math.floor(Math.random() * 361); // Generates random hue between 0 and 360
  }

  return (
    <React.Fragment>
      <ReactRouterDOM.Link
        key={book.book_id}
        to={{
          pathname: `/books/${book.book_id}`,
          state: { book }
        }}>
      <div className="search-book-div">
        <div className="book-image-background" style={{ backgroundColor: `hsl(${generateRandomHue()}, 40%, 95%)`}}></div>
          <div className="image-block">
            <img src={book.image_url} className="img-fluid" alt={`Picture cover for ${book.title}`} />
          </div>
        <div className="book-contents">
          <div className="title">{book.title}</div>
          {/* render subtitle if present in the book */}
          { book.subtitle ? <span className="subtitle">{book.subtitle}</span> : <span/> }
          <div className="authors">{book.authors}</div>
        </div>
      </div>
      </ReactRouterDOM.Link>
    </React.Fragment>
  );
}
