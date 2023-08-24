function MeetingDataContainer() {

    const [meeting, setMeeting] = React.useState([]);
  
    React.useEffect(() => {
      fetch('/api/get_all_meetings')
      .then(response => response.json())
      .then(response => setMeeting(response))
    }, []);
  
    const tradingCards = [];
  
    for (const currentCard of cards) {
      tradingCards.push(
        <TradingCard
          key={currentCard.name}
          name={currentCard.name}
          skill={currentCard.skill}
          imgUrl={currentCard.imgUrl}
        />
      );
    }
  
    function addCard(newCard) {
      const currentCards = [...cards];
      setCards([...currentCards, newCard]);
    }
  
    return (
      <React.Fragment>
        <AddTradingCard addCard={addCard} />
        <h2>Trading Cards</h2>
        <div className="grid">{tradingCards}</div>
      </React.Fragment>
    );
  
  }


ReactDOM.render(<MeetingDataContainer />, document.getElementById('container'));