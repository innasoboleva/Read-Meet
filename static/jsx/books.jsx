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
  
    function openBookDetails() {
      console.log(`${book.title} clicked!`);
    }
  
    return (
      <React.Fragment>
        <div className="search-book-div" onClick={openBookDetails}>
          <div>
            <img src={book.image} className="img-fluid" alt={`Picture cover for ${book.title}`} />
          </div>
          <div className="title">{book.title}</div>
          {/* render subtitle only if present in the book */}
          {/* { book.subtitle ? <span className="subtitle"><br></br>{book.subtitle}</span> : null } */}
          <div className="authors">{book.authors}</div>
          
        </div>
      </React.Fragment>
    );
  }
  
  ReactDOM.render(<BooksSearchContainer />, document.getElementById('container-books'));