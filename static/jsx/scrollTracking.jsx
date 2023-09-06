// Scroll listener, with debouce option so it won't get called many times at once
const useScrollTracking = (threshold) => {
    
    const [page, setPage] = React.useState(0);
    const [isLoading, setIsLoading] = React.useState(false);
    console.log('IM IN SCROLL FILE');
    let isScrolling = false;
  
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
        console.log('IM IN SCROLL scrollDown');
        if (!isScrolling) {
            setTimeout(() => {
            isScrolling = true;
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - threshold) {
                console.log("Scrolled ONCE");
                setIsLoading(true);
                setPage(prevPage => prevPage + 1);
            }
            isScrolling = false;
        }, 300); // 300ms delay
      }
    };
  
    const debouncedScrollDown = debounce(scrollDown, 300);
  
    React.useEffect(() => {
        console.log('added scroll to window');
        window.addEventListener('scroll', debouncedScrollDown);
        return () => window.removeEventListener('scroll', debouncedScrollDown);
    }, [debouncedScrollDown]);
  
    return { page, isLoading };
  };