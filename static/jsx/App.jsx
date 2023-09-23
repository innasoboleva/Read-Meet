function App() {
  
    return (
      <ReactRouterDOM.BrowserRouter>
        <div className="container-fluid">
        <ReactRouterDOM.Switch>
          <ReactRouterDOM.Route exact path="/" >
            <IndexPageContainer />
          </ReactRouterDOM.Route>
          
            <ReactRouterDOM.Route exact path="/books" >
                <BooksSearchContainer />
            </ReactRouterDOM.Route>
            <ReactRouterDOM.Route path="/books/:bookId" component={BookDetailsPage} />
          </ReactRouterDOM.Switch>
        </div>
      </ReactRouterDOM.BrowserRouter>
    );
  }
  
  ReactDOM.render(<App />, document.querySelector('#container-books'));
  