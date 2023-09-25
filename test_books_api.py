import apis.books_api

class TestBooksApi:
    # no key provided
    respond1 = {}
    # key provided, no search args
    respond2 = { "error": { "code": 400, "message": "Missing query.", "errors": [ { "message": "Missing query.", "domain": "global", "reason": "queryRequired", "location": "q", "locationType": "parameter" } ] } }
    # id provided, no key
    respond3 = {}
    # key provided, no id
    respond4 = {}
    # search arg provided and key provided, respond with 2 items
    resond5 = {
        "kind": "books#volumes",
        "totalItems": 1316,
        "items": [
            {
            "kind": "books#volume",
            "id": "rDszEAAAQBAJ",
            "etag": "3Ztza4KqjSI",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/rDszEAAAQBAJ",
            "volumeInfo": {
                "title": "Unit Testing Principles, Practices, and Patterns",
                "authors": [
                "Vladimir Khorikov"
                ],
                "publisher": "Simon and Schuster",
                "publishedDate": "2020-01-06",
                "description": "\"This book is an indispensable resource.\" - Greg Wright, Kainos Software Ltd. Radically improve your testing practice and software quality with new testing styles, good patterns, and reliable automation. Key Features A practical and results-driven approach to unit testing Refine your existing unit tests by implementing modern best practices Learn the four pillars of a good unit test Safely automate your testing process to save time and money Spot which tests need refactoring, and which need to be deleted entirely Purchase of the print book includes a free eBook in PDF, Kindle, and ePub formats from Manning Publications. About The Book Great testing practices maximize your project quality and delivery speed by identifying bad code early in the development process. Wrong tests will break your code, multiply bugs, and increase time and costs. You owe it to yourself—and your projects—to learn how to do excellent unit testing. Unit Testing Principles, Patterns and Practices teaches you to design and write tests that target key areas of your code including the domain model. In this clearly written guide, you learn to develop professional-quality tests and test suites and integrate testing throughout the application life cycle. As you adopt a testing mindset, you’ll be amazed at how better tests cause you to write better code. What You Will Learn Universal guidelines to assess any unit test Testing to identify and avoid anti-patterns Refactoring tests along with the production code Using integration tests to verify the whole system This Book Is Written For For readers who know the basics of unit testing. Examples are written in C# and can easily be applied to any language. About the Author Vladimir Khorikov is an author, blogger, and Microsoft MVP. He has mentored numerous teams on the ins and outs of unit testing. Table of Contents: PART 1 THE BIGGER PICTURE 1 ¦ The goal of unit testing 2 ¦ What is a unit test? 3 ¦ The anatomy of a unit test PART 2 MAKING YOUR TESTS WORK FOR YOU 4 ¦ The four pillars of a good unit test 5 ¦ Mocks and test fragility 6 ¦ Styles of unit testing 7 ¦ Refactoring toward valuable unit tests PART 3 INTEGRATION TESTING 8 ¦ Why integration testing? 9 ¦ Mocking best practices 10 ¦ Testing the database PART 4 UNIT TESTING ANTI-PATTERNS 11 ¦ Unit testing anti-patterns",
                "industryIdentifiers": [
                {
                    "type": "ISBN_13",
                    "identifier": "9781638350293"
                },
                {
                    "type": "ISBN_10",
                    "identifier": "1638350299"
                }
                ],
                "readingModes": {
                "text": true,
                "image": false
                },
                "pageCount": 442,
                "printType": "BOOK",
                "categories": [
                "Computers"
                ],
                "maturityRating": "NOT_MATURE",
                "allowAnonLogging": true,
                "contentVersion": "1.1.1.0.preview.2",
                "panelizationSummary": {
                "containsEpubBubbles": false,
                "containsImageBubbles": false
                },
                "imageLinks": {
                "smallThumbnail": "http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                "thumbnail": "http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
                },
                "language": "en",
                "previewLink": "http://books.google.com/books?id=rDszEAAAQBAJ&printsec=frontcover&dq=unit+testing&hl=&cd=1&source=gbs_api",
                "infoLink": "https://play.google.com/store/books/details?id=rDszEAAAQBAJ&source=gbs_api",
                "canonicalVolumeLink": "https://play.google.com/store/books/details?id=rDszEAAAQBAJ"
            },
            "saleInfo": {
                "country": "US",
                "saleability": "FOR_SALE",
                "isEbook": true,
                "listPrice": {
                "amount": 36.99,
                "currencyCode": "USD"
                },
                "retailPrice": {
                "amount": 36.99,
                "currencyCode": "USD"
                },
                "buyLink": "https://play.google.com/store/books/details?id=rDszEAAAQBAJ&rdid=book-rDszEAAAQBAJ&rdot=1&source=gbs_api",
                "offers": [
                {
                    "finskyOfferType": 1,
                    "listPrice": {
                    "amountInMicros": 36990000,
                    "currencyCode": "USD"
                    },
                    "retailPrice": {
                    "amountInMicros": 36990000,
                    "currencyCode": "USD"
                    },
                    "giftable": true
                }
                ]
            },
            "accessInfo": {
                "country": "US",
                "viewability": "PARTIAL",
                "embeddable": true,
                "publicDomain": false,
                "textToSpeechPermission": "ALLOWED_FOR_ACCESSIBILITY",
                "epub": {
                "isAvailable": true,
                "acsTokenLink": "http://books.google.com/books/download/Unit_Testing_Principles_Practices_and_Pa-sample-epub.acsm?id=rDszEAAAQBAJ&format=epub&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                },
                "pdf": {
                "isAvailable": false
                },
                "webReaderLink": "http://play.google.com/books/reader?id=rDszEAAAQBAJ&hl=&source=gbs_api",
                "accessViewStatus": "SAMPLE",
                "quoteSharingAllowed": false
            },
            "searchInfo": {
                "textSnippet": "&quot;This book is an indispensable resource."
            }
            },
            {
            "kind": "books#volume",
            "id": "cindfHv-_WMC",
            "etag": "5oJCYJ6ohpw",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/cindfHv-_WMC",
            "volumeInfo": {
                "title": "Unit Testing in Java",
                "subtitle": "How Tests Drive the Code",
                "authors": [
                "Johannes Link",
                "Peter Fröhlich"
                ],
                "publisher": "Morgan Kaufmann",
                "publishedDate": "2003-06-03",
                "description": "Software testing is indispensable and is one of the most discussed topics in software development today. Many companies address this issue by assigning a dedicated software testing phase towards the end of their development cycle. However, quality cannot be tested into a buggy application. Early and continuous unit testing has been shown to be crucial for high quality software and low defect rates. Yet current books on testing ignore the developer's point of view and give little guidance on how to bring the overwhelming amount of testing theory into practice. Unit Testing in Java represents a practical introduction to unit testing for software developers. It introduces the basic test-first approach and then discusses a large number of special issues and problem cases. The book instructs developers through each step and motivates them to explore further. Shows how the discovery and avoidance of software errors is a demanding and creative activity in its own right and can build confidence early in a project. Demonstrates how automated tests can detect the unwanted effects of small changes in code within the entire system. Discusses how testing works with persistency, concurrency, distribution, and web applications. Includes a discussion of testing with C++ and Smalltalk.",
                "industryIdentifiers": [
                {
                    "type": "ISBN_10",
                    "identifier": "1558608680"
                },
                {
                    "type": "ISBN_13",
                    "identifier": "9781558608689"
                }
                ],
                "readingModes": {
                "text": false,
                "image": true
                },
                "pageCount": 172,
                "printType": "BOOK",
                "categories": [
                "Computers"
                ],
                "maturityRating": "NOT_MATURE",
                "allowAnonLogging": false,
                "contentVersion": "0.4.2.0.preview.1",
                "panelizationSummary": {
                "containsEpubBubbles": false,
                "containsImageBubbles": false
                },
                "imageLinks": {
                "smallThumbnail": "http://books.google.com/books/content?id=cindfHv-_WMC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                "thumbnail": "http://books.google.com/books/content?id=cindfHv-_WMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
                },
                "language": "en",
                "previewLink": "http://books.google.com/books?id=cindfHv-_WMC&printsec=frontcover&dq=unit+testing&hl=&cd=2&source=gbs_api",
                "infoLink": "http://books.google.com/books?id=cindfHv-_WMC&dq=unit+testing&hl=&source=gbs_api",
                "canonicalVolumeLink": "https://books.google.com/books/about/Unit_Testing_in_Java.html?hl=&id=cindfHv-_WMC"
            },
            "saleInfo": {
                "country": "US",
                "saleability": "NOT_FOR_SALE",
                "isEbook": false
            },
            "accessInfo": {
                "country": "US",
                "viewability": "PARTIAL",
                "embeddable": true,
                "publicDomain": false,
                "textToSpeechPermission": "ALLOWED",
                "epub": {
                "isAvailable": false
                },
                "pdf": {
                "isAvailable": true,
                "acsTokenLink": "http://books.google.com/books/download/Unit_Testing_in_Java-sample-pdf.acsm?id=cindfHv-_WMC&format=pdf&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                },
                "webReaderLink": "http://play.google.com/books/reader?id=cindfHv-_WMC&hl=&source=gbs_api",
                "accessViewStatus": "SAMPLE",
                "quoteSharingAllowed": false
            },
            "searchInfo": {
                "textSnippet": "Unit Testing in Java How Tests Drive the Code Johannes Link With contributions by Peter Fröhlich Forewords by Erich Gamma and Frank Westphal &quot;This...is a practical introduction to using automated unit tests and the test-first approach in ..."
            }
            },
        ]
        }
    # same result but next page

    book_url = "https://www.googleapis.com/books/v1/volumes?q=" # add search args to the url
    book_url_with_id = "https://www.googleapis.com/books/v1/volumes/" # id + ?key=yourKey

    def test_get_random_search_param():
        pass
    
    # gets google response either with errors or with results, I'm using mock responds
    def test_get_search_result_for_params(param, page=0, on_page=None):
        pass


    def test_get_list_of_books_for_page(search_result):
        pass


    def test_get_books_info_from_response(items, start=None, stop=None):
        pass


    def test_find_popular_book(info):
        pass

    # runs 3 other methods one after each other
    def test_find_list_of_books(params, page):
        pass


    def test_find_book(book_id):
        pass