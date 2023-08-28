function BooksSearchContainer() {
  const [books, setBooks] = React.useState([]);

  React.useEffect(() => {
    // Getting url that is already rendered with search parameters
    const queryParamsString = window.location.search;
    // constructing fetch request with current params
    const newUrlWithSearch = `/api/get_books${queryParamsString}`

    fetch(newUrlWithSearch)
      .then(response => response.json())
      .then(data => {
          if (data["status"] == "success") {
            setBooks(data["books"])
            console.log(data["books"])
          }
        })
      .catch(error => console.error('Error fetching books with search query:', error));
  }, []);
  
    return (
      <React.Fragment>
        <h4>Results</h4>
        <div className="search-all-books d-flex">
          { books.map((book) => (
              <Book key={book.ISBN} book={book} />
            ))}
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