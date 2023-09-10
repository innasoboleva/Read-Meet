function App() {
  
    return (
      <ReactRouterDOM.BrowserRouter>
        <div className="container-fluid">
      <ReactRouterDOM.Switch>
        <ReactRouterDOM.Route path="/" exact>
          <IndexPageContainer />
          {/* <CarouselDataContainer />
          <MeetingDataContainer /> */}
        </ReactRouterDOM.Route>
        
          <ReactRouterDOM.Route path="/books" exact>
              <BooksSearchContainer />
          </ReactRouterDOM.Route>
          <ReactRouterDOM.Route path="/books/:bookId" component={BookDetailsPage} />
        </ReactRouterDOM.Switch>
        </div>
      </ReactRouterDOM.BrowserRouter>
    );
  }
  
  ReactDOM.render(<App />, document.querySelector('#container-books'));
  