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
    function openBookDetails() {
      console.log(`${book.title} clicked!`);
      setShowDetails(!showDetails);
    }

    function generateRandomHue() {
      return Math.floor(Math.random() * 361); // Generates random hue between 0 and 360
    }
  
    return (
      <React.Fragment>
        <ReactRouterDOM.Link to={`/books/${book.ISBN}`}>
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


function BookDetailsPage() {
  // const { bookId } = ReactRouterDOM.useParams();
  console.log("Well, im rendering here....")
  return (
    <React.Fragment>
      <div className='details'>Figggnya</div>
      {/* { bookId } */}
    </React.Fragment>)
}
