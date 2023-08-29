function App() {
  
    return (
      <ReactRouterDOM.BrowserRouter>
        <div className="container-fluid">
          <ReactRouterDOM.Route path="/books" exact>
              <BooksSearchContainer />
          </ReactRouterDOM.Route>
          <ReactRouterDOM.Route path="/books/:bookId" component={BookDetailsPage} />
        </div>
      </ReactRouterDOM.BrowserRouter>
    );
  }
  
  ReactDOM.render(<App />, document.querySelector('#container-books'));
  