from apis import books_api


class TestBooksApi:
    # Mock data, search arg provided and key provided, respond with 2 items
    respond1 = {
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
                "text": True,
                "image": False
                },
                "pageCount": 442,
                "printType": "BOOK",
                "categories": [
                "Computers"
                ],
                "maturityRating": "NOT_MATURE",
                "allowAnonLogging": True,
                "contentVersion": "1.1.1.0.preview.2",
                "panelizationSummary": {
                "containsEpubBubbles": False,
                "containsImageBubbles": False
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
                "isEbook": True,
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
                    "giftable": True
                }
                ]
            },
            "accessInfo": {
                "country": "US",
                "viewability": "PARTIAL",
                "embeddable": True,
                "publicDomain": False,
                "textToSpeechPermission": "ALLOWED_FOR_ACCESSIBILITY",
                "epub": {
                "isAvailable": True,
                "acsTokenLink": "http://books.google.com/books/download/Unit_Testing_Principles_Practices_and_Pa-sample-epub.acsm?id=rDszEAAAQBAJ&format=epub&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                },
                "pdf": {
                "isAvailable": False
                },
                "webReaderLink": "http://play.google.com/books/reader?id=rDszEAAAQBAJ&hl=&source=gbs_api",
                "accessViewStatus": "SAMPLE",
                "quoteSharingAllowed": False
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
                "text": False,
                "image": True
                },
                "pageCount": 172,
                "printType": "BOOK",
                "categories": [
                "Computers"
                ],
                "maturityRating": "NOT_MATURE",
                "allowAnonLogging": False,
                "contentVersion": "0.4.2.0.preview.1",
                "panelizationSummary": {
                "containsEpubBubbles": False,
                "containsImageBubbles": False
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
                "isEbook": False
            },
            "accessInfo": {
                "country": "US",
                "viewability": "PARTIAL",
                "embeddable": True,
                "publicDomain": False,
                "textToSpeechPermission": "ALLOWED",
                "epub": {
                "isAvailable": False
                },
                "pdf": {
                "isAvailable": True,
                "acsTokenLink": "http://books.google.com/books/download/Unit_Testing_in_Java-sample-pdf.acsm?id=cindfHv-_WMC&format=pdf&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
                },
                "webReaderLink": "http://play.google.com/books/reader?id=cindfHv-_WMC&hl=&source=gbs_api",
                "accessViewStatus": "SAMPLE",
                "quoteSharingAllowed": False
            },
            "searchInfo": {
                "textSnippet": "Unit Testing in Java How Tests Drive the Code Johannes Link With contributions by Peter Fröhlich Forewords by Erich Gamma and Frank Westphal &quot;This...is a practical introduction to using automated unit tests and the test-first approach in ..."
            }
            },
        ]
    }
    # Mock data, one book result got by ID from google books
    respond2 = {
  "kind": "books#volume",
  "id": "T7-bDwAAQBAJ",
  "etag": "g+WKIESFUTc",
  "selfLink": "https://www.googleapis.com/books/v1/volumes/T7-bDwAAQBAJ",
  "volumeInfo": {
    "title": "Dog Is Love",
    "subtitle": "Why and How Your Dog Loves You",
    "authors": [
      "Clive D. L. Wynne"
    ],
    "publisher": "Houghton Mifflin Harcourt",
    "publishedDate": "2019",
    "description": "\u003cb\u003e\"Lively and fascinating... The reader comes away cheered, better informed, and with a new and deeper appreciation for our amazing canine companions and their enormous capacity for love.\"--Cat Warren, \u003ci\u003eNew York Times\u003c/i\u003e best-selling author of\u003ci\u003eWhat the Dog Knows\u003c/i\u003e \u003c/b\u003e\u003cbr\u003e \u003cbr\u003e \u003cb\u003eDoes your dog love you?\u003c/b\u003e \u003cbr\u003e Every dog lover knows the feeling. The nuzzle of a dog's nose, the warmth of them lying at our feet, even their whining when they want to get up on the bed. It really seems like our dogs love us, too. But for years, scientists have resisted that conclusion, warning against anthropomorphizing our pets. Enter Clive Wynne, a pioneering canine behaviorist whose research is helping to usher in a new era: one in which love, not intelligence or submissiveness, is at the heart of the human-canine relationship. Drawing on cuttingâe'edge studies from his lab and others around the world, Wynne shows that affection is the very essence of dogs, from their faces and tails to their brains, hormones, even DNA. This scientific revolution is revealing more about dogs' unique origins, behavior, needs, and hidden depths than we ever imagined possible.\u003cbr\u003e \u003cbr\u003e A humane, illuminating book,\u003ci\u003eDog Is Love\u003c/i\u003e is essential reading for anyone who has ever loved a dog--and experienced the wonder of being loved back.",
    "industryIdentifiers": [
      {
        "type": "ISBN_10",
        "identifier": "132854396X"
      },
      {
        "type": "ISBN_13",
        "identifier": "9781328543967"
      }
    ],
    "readingModes": {
      "text": False,
      "image": True
    },
    "pageCount": 272,
    "printedPageCount": 277,
    "dimensions": {
      "height": "22.90 cm",
      "width": "15.20 cm",
      "thickness": "2.40 cm"
    },
    "printType": "BOOK",
    "categories": [
      "Pets / Dogs / General",
      "Psychology / Animal & Comparative Psychology",
      "Science / Life Sciences / Evolution"
    ],
    "maturityRating": "NOT_MATURE",
    "allowAnonLogging": False,
    "contentVersion": "0.0.1.0.preview.1",
    "panelizationSummary": {
      "containsEpubBubbles": False,
      "containsImageBubbles": False
    },
    "imageLinks": {
      "smallThumbnail": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&imgtk=AFLRE70hBWdXHEyyLG76PhsL0IxYdLu-xiXtfrlsr-NhAZxvpPHssbkQXL4Sy7e0zc9xgy3Vr8XGFxCI6EnIteWJUKF8TXABGaO3n-Ts_7w7x0J0RAXEWgDGjZq-SxBg5z6Ck0kSAxYL&source=gbs_api",
      "thumbnail": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70oFaS9bNbP-kFpaUefEZoHfnj7aQf0Affb1mWIyZsO-pAEHwCD9YhsCEtSpXk8W_d1xnKHxOidynsJMaIn5e3LtQNHI_ZtDHhZXv-JZ0tAFb_3ysN6N6bWHU0ibpfpsyvXFrXx&source=gbs_api",
      "small": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=2&edge=curl&imgtk=AFLRE70S1wSuzveR3gMqHUQfyipBl4BEW33bih0WKMfeL40NOavNZL1EA1obtH6WPvjp-x-XMsTe9pwZdwwHhmgE3odyNSmlxiFhpZIAEeGKxYgeeIzgSvcPiAQsE1Cn3I3WjIFP9o7C&source=gbs_api",
      "medium": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=3&edge=curl&imgtk=AFLRE71xUSeBr0AzgZ-fUtgHUt8ESthYIfIFFlQRNMC7KXz5IZuSz0dV6v1d2ZHfEjw96ZKRXgEq_TIMhctDslr_QhTNoq0J64UkPl0txcoy1hp34yWbRmWIuaVunKHI4g5_gAAz2Kjx&source=gbs_api",
      "large": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=4&edge=curl&imgtk=AFLRE72gGTVW5RCqXHCVd_GFoMnfmkec83_RHCRej3JXBIRkMtxUxsnnntAgUsOmvXlY9t_WO7INaHxn6OvfPyR-F8nog4ZgbmOJEZX-rGG3IbcfXXBpt4do4A_6y_tAJFFxOYHwDL8D&source=gbs_api",
      "extraLarge": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=6&edge=curl&imgtk=AFLRE70YFsFzz13IeijjT7QijSL-nbIq4aEz9P42Uh0zSMMhD74g4W_ScOhlnpC3WjGfXjytqhe-iVUXJUkhEOoA39D8MTSem2FNDFtbQM2kcxsW6xyOogy1nfodDDdnb7UAlqn49c0X&source=gbs_api"
    },
    "language": "en",
    "previewLink": "http://books.google.com/books?id=T7-bDwAAQBAJ&hl=&source=gbs_api",
    "infoLink": "https://play.google.com/store/books/details?id=T7-bDwAAQBAJ&source=gbs_api",
    "canonicalVolumeLink": "https://play.google.com/store/books/details?id=T7-bDwAAQBAJ"
  },
  "saleInfo": {
    "country": "US",
    "saleability": "NOT_FOR_SALE",
    "isEbook": False
  },
  "accessInfo": {
    "country": "US",
    "viewability": "PARTIAL",
    "embeddable": True,
    "publicDomain": False,
    "textToSpeechPermission": "ALLOWED",
    "epub": {
      "isAvailable": False
    },
    "pdf": {
      "isAvailable": True,
      "acsTokenLink": "http://books.google.com/books/download/Dog_Is_Love-sample-pdf.acsm?id=T7-bDwAAQBAJ&format=pdf&output=acs4_fulfillment_token&dl_type=sample&source=gbs_api"
    },
    "webReaderLink": "http://play.google.com/books/reader?id=T7-bDwAAQBAJ&hl=&source=gbs_api",
    "accessViewStatus": "SAMPLE",
    "quoteSharingAllowed": False
  }
}

    def test_get_random_search_param(self):
        """ Checking wordlist file, getting random word, asserting result is not empty string """
        random_word = books_api._get_random_search_param()
        assert len(random_word) > 0 and isinstance(random_word, str) # shpould return non empty string


    def test_get_list_of_books_for_page_all_books(self):
        """ With provided google response with 2 book asserting reading information is correct, getting all books """
        search_result = { "status": "success", "response": self.respond1, "on_page": None } # displaying all books
        result = books_api._get_list_of_books_for_page(search_result)
        assert result["books"] == [{ 'book_id': 'rDszEAAAQBAJ', 'title': 'Unit Testing Principles, Practices, and Patterns', 'subtitle': '', \
                  'authors':"Vladimir Khorikov", 'description': '"This book is an indispensable resource." - Greg Wright, Kainos Software Ltd. Radically improve your testing practice and software quality with new testing styles, good patterns, and reliable automation. Key Features A practical and results-driven approach to unit testing Refine your existing unit tests by implementing modern best practices Learn the four pillars of a good unit test Safely automate your testing process to save time and money Spot which tests need refactoring, and which need to be deleted entirely Purchase of the print book includes a free eBook in PDF, Kindle, and ePub formats from Manning Publications. About The Book Great testing practices maximize your project quality and delivery speed by identifying bad code early in the development process. Wrong tests will break your code, multiply bugs, and increase time and costs. You owe it to yourself—and your projects—to learn how to do excellent unit testing. Unit Testing Principles, Patterns and Practices teaches you to design and write tests that target key areas of your code including the domain model. In this clearly written guide, you learn to develop professional-quality tests and test suites and integrate testing throughout the application life cycle. As you adopt a testing mindset, you’ll be amazed at how better tests cause you to write better code. What You Will Learn Universal guidelines to assess any unit test Testing to identify and avoid anti-patterns Refactoring tests along with the production code Using integration tests to verify the whole system This Book Is Written For For readers who know the basics of unit testing. Examples are written in C# and can easily be applied to any language. About the Author Vladimir Khorikov is an author, blogger, and Microsoft MVP. He has mentored numerous teams on the ins and outs of unit testing. Table of Contents: PART 1 THE BIGGER PICTURE 1 ¦ The goal of unit testing 2 ¦ What is a unit test? 3 ¦ The anatomy of a unit test PART 2 MAKING YOUR TESTS WORK FOR YOU 4 ¦ The four pillars of a good unit test 5 ¦ Mocks and test fragility 6 ¦ Styles of unit testing 7 ¦ Refactoring toward valuable unit tests PART 3 INTEGRATION TESTING 8 ¦ Why integration testing? 9 ¦ Mocking best practices 10 ¦ Testing the database PART 4 UNIT TESTING ANTI-PATTERNS 11 ¦ Unit testing anti-patterns',\
                    'ISBN':'9781638350293', 'image_url': 'http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' },
                  { 'book_id': 'cindfHv-_WMC', 'title': 'Unit Testing in Java', 'subtitle': 'How Tests Drive the Code', \
                  'authors': "Johannes Link, Peter Fröhlich", 'description': "Software testing is indispensable and is one of the most discussed topics in software development today. Many companies address this issue by assigning a dedicated software testing phase towards the end of their development cycle. However, quality cannot be tested into a buggy application. Early and continuous unit testing has been shown to be crucial for high quality software and low defect rates. Yet current books on testing ignore the developer's point of view and give little guidance on how to bring the overwhelming amount of testing theory into practice. Unit Testing in Java represents a practical introduction to unit testing for software developers. It introduces the basic test-first approach and then discusses a large number of special issues and problem cases. The book instructs developers through each step and motivates them to explore further. Shows how the discovery and avoidance of software errors is a demanding and creative activity in its own right and can build confidence early in a project. Demonstrates how automated tests can detect the unwanted effects of small changes in code within the entire system. Discusses how testing works with persistency, concurrency, distribution, and web applications. Includes a discussion of testing with C++ and Smalltalk.",\
                      'ISBN': '9781558608689', 'image_url': 'http://books.google.com/books/content?id=cindfHv-_WMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' }]

    
    def test_get_list_of_books_for_page_one_book(self):
        """ With provided google response with 2 book asserting reading information is correct, getting one book """
        search_result = { "status": "success", "response": self.respond1, "on_page": 1 } # displaying 1 book
        result = books_api._get_list_of_books_for_page(search_result)
        assert result['books'] == [{ "book_id": 'rDszEAAAQBAJ', 'title': 'Unit Testing Principles, Practices, and Patterns', 'subtitle': '', \
                  'authors':"Vladimir Khorikov", 'description': "\"This book is an indispensable resource.\" - Greg Wright, Kainos Software Ltd. Radically improve your testing practice and software quality with new testing styles, good patterns, and reliable automation. Key Features A practical and results-driven approach to unit testing Refine your existing unit tests by implementing modern best practices Learn the four pillars of a good unit test Safely automate your testing process to save time and money Spot which tests need refactoring, and which need to be deleted entirely Purchase of the print book includes a free eBook in PDF, Kindle, and ePub formats from Manning Publications. About The Book Great testing practices maximize your project quality and delivery speed by identifying bad code early in the development process. Wrong tests will break your code, multiply bugs, and increase time and costs. You owe it to yourself—and your projects—to learn how to do excellent unit testing. Unit Testing Principles, Patterns and Practices teaches you to design and write tests that target key areas of your code including the domain model. In this clearly written guide, you learn to develop professional-quality tests and test suites and integrate testing throughout the application life cycle. As you adopt a testing mindset, you’ll be amazed at how better tests cause you to write better code. What You Will Learn Universal guidelines to assess any unit test Testing to identify and avoid anti-patterns Refactoring tests along with the production code Using integration tests to verify the whole system This Book Is Written For For readers who know the basics of unit testing. Examples are written in C# and can easily be applied to any language. About the Author Vladimir Khorikov is an author, blogger, and Microsoft MVP. He has mentored numerous teams on the ins and outs of unit testing. Table of Contents: PART 1 THE BIGGER PICTURE 1 ¦ The goal of unit testing 2 ¦ What is a unit test? 3 ¦ The anatomy of a unit test PART 2 MAKING YOUR TESTS WORK FOR YOU 4 ¦ The four pillars of a good unit test 5 ¦ Mocks and test fragility 6 ¦ Styles of unit testing 7 ¦ Refactoring toward valuable unit tests PART 3 INTEGRATION TESTING 8 ¦ Why integration testing? 9 ¦ Mocking best practices 10 ¦ Testing the database PART 4 UNIT TESTING ANTI-PATTERNS 11 ¦ Unit testing anti-patterns",\
                    'ISBN':'9781638350293', 'image_url': 'http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' }]

    
    def test_get_books_info_from_response_all_books(self):
        """ With provided google response with 2 book asserting reading information is correct, getting all books """
        books = self.respond1.get('items', [])
        result = books_api._get_books_info_from_response(books) # get all results
        assert  [{ 'book_id': 'rDszEAAAQBAJ', 'title': 'Unit Testing Principles, Practices, and Patterns', 'subtitle': '', \
                  'authors':"Vladimir Khorikov", 'description': '"This book is an indispensable resource." - Greg Wright, Kainos Software Ltd. Radically improve your testing practice and software quality with new testing styles, good patterns, and reliable automation. Key Features A practical and results-driven approach to unit testing Refine your existing unit tests by implementing modern best practices Learn the four pillars of a good unit test Safely automate your testing process to save time and money Spot which tests need refactoring, and which need to be deleted entirely Purchase of the print book includes a free eBook in PDF, Kindle, and ePub formats from Manning Publications. About The Book Great testing practices maximize your project quality and delivery speed by identifying bad code early in the development process. Wrong tests will break your code, multiply bugs, and increase time and costs. You owe it to yourself—and your projects—to learn how to do excellent unit testing. Unit Testing Principles, Patterns and Practices teaches you to design and write tests that target key areas of your code including the domain model. In this clearly written guide, you learn to develop professional-quality tests and test suites and integrate testing throughout the application life cycle. As you adopt a testing mindset, you’ll be amazed at how better tests cause you to write better code. What You Will Learn Universal guidelines to assess any unit test Testing to identify and avoid anti-patterns Refactoring tests along with the production code Using integration tests to verify the whole system This Book Is Written For For readers who know the basics of unit testing. Examples are written in C# and can easily be applied to any language. About the Author Vladimir Khorikov is an author, blogger, and Microsoft MVP. He has mentored numerous teams on the ins and outs of unit testing. Table of Contents: PART 1 THE BIGGER PICTURE 1 ¦ The goal of unit testing 2 ¦ What is a unit test? 3 ¦ The anatomy of a unit test PART 2 MAKING YOUR TESTS WORK FOR YOU 4 ¦ The four pillars of a good unit test 5 ¦ Mocks and test fragility 6 ¦ Styles of unit testing 7 ¦ Refactoring toward valuable unit tests PART 3 INTEGRATION TESTING 8 ¦ Why integration testing? 9 ¦ Mocking best practices 10 ¦ Testing the database PART 4 UNIT TESTING ANTI-PATTERNS 11 ¦ Unit testing anti-patterns',\
                    'ISBN':'9781638350293', 'image_url': 'http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' },
                  { 'book_id': 'cindfHv-_WMC', 'title': 'Unit Testing in Java', 'subtitle': 'How Tests Drive the Code', \
                  'authors': "Johannes Link, Peter Fröhlich", 'description': "Software testing is indispensable and is one of the most discussed topics in software development today. Many companies address this issue by assigning a dedicated software testing phase towards the end of their development cycle. However, quality cannot be tested into a buggy application. Early and continuous unit testing has been shown to be crucial for high quality software and low defect rates. Yet current books on testing ignore the developer's point of view and give little guidance on how to bring the overwhelming amount of testing theory into practice. Unit Testing in Java represents a practical introduction to unit testing for software developers. It introduces the basic test-first approach and then discusses a large number of special issues and problem cases. The book instructs developers through each step and motivates them to explore further. Shows how the discovery and avoidance of software errors is a demanding and creative activity in its own right and can build confidence early in a project. Demonstrates how automated tests can detect the unwanted effects of small changes in code within the entire system. Discusses how testing works with persistency, concurrency, distribution, and web applications. Includes a discussion of testing with C++ and Smalltalk.",\
                      'ISBN': '9781558608689', 'image_url': 'http://books.google.com/books/content?id=cindfHv-_WMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' }] == result["books"]


    def test_get_books_info_from_response_one_book(self):
        """ With provided google response with 2 book asserting reading information is correct, getting one book """
        books = self.respond1.get('items', [])
        result = books_api._get_books_info_from_response(books, start=0, stop=1)
        assert result['books'] == [{ "book_id": 'rDszEAAAQBAJ', 'title': 'Unit Testing Principles, Practices, and Patterns', 'subtitle': '', \
                  'authors':"Vladimir Khorikov", 'description': "\"This book is an indispensable resource.\" - Greg Wright, Kainos Software Ltd. Radically improve your testing practice and software quality with new testing styles, good patterns, and reliable automation. Key Features A practical and results-driven approach to unit testing Refine your existing unit tests by implementing modern best practices Learn the four pillars of a good unit test Safely automate your testing process to save time and money Spot which tests need refactoring, and which need to be deleted entirely Purchase of the print book includes a free eBook in PDF, Kindle, and ePub formats from Manning Publications. About The Book Great testing practices maximize your project quality and delivery speed by identifying bad code early in the development process. Wrong tests will break your code, multiply bugs, and increase time and costs. You owe it to yourself—and your projects—to learn how to do excellent unit testing. Unit Testing Principles, Patterns and Practices teaches you to design and write tests that target key areas of your code including the domain model. In this clearly written guide, you learn to develop professional-quality tests and test suites and integrate testing throughout the application life cycle. As you adopt a testing mindset, you’ll be amazed at how better tests cause you to write better code. What You Will Learn Universal guidelines to assess any unit test Testing to identify and avoid anti-patterns Refactoring tests along with the production code Using integration tests to verify the whole system This Book Is Written For For readers who know the basics of unit testing. Examples are written in C# and can easily be applied to any language. About the Author Vladimir Khorikov is an author, blogger, and Microsoft MVP. He has mentored numerous teams on the ins and outs of unit testing. Table of Contents: PART 1 THE BIGGER PICTURE 1 ¦ The goal of unit testing 2 ¦ What is a unit test? 3 ¦ The anatomy of a unit test PART 2 MAKING YOUR TESTS WORK FOR YOU 4 ¦ The four pillars of a good unit test 5 ¦ Mocks and test fragility 6 ¦ Styles of unit testing 7 ¦ Refactoring toward valuable unit tests PART 3 INTEGRATION TESTING 8 ¦ Why integration testing? 9 ¦ Mocking best practices 10 ¦ Testing the database PART 4 UNIT TESTING ANTI-PATTERNS 11 ¦ Unit testing anti-patterns",\
                    'ISBN':'9781638350293', 'image_url': 'http://books.google.com/books/content?id=rDszEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api' }]
       


    def test__get_book_for_book_ID(self):
        """ With provided google response with book that was searched for by ID asserting reading information is correct """
        response = { "status": "success", "response": self.respond2 }
        result = books_api._get_book_for_book_ID(response)
        assert result["book"] == {"book_id": "T7-bDwAAQBAJ", "title": "Dog Is Love", \
                                  "subtitle": "Why and How Your Dog Loves You", "authors": "Clive D. L. Wynne",\
                                    "description": "\u003cb\u003e\"Lively and fascinating... The reader comes away cheered, better informed, and with a new and deeper appreciation for our amazing canine companions and their enormous capacity for love.\"--Cat Warren, \u003ci\u003eNew York Times\u003c/i\u003e best-selling author of\u003ci\u003eWhat the Dog Knows\u003c/i\u003e \u003c/b\u003e\u003cbr\u003e \u003cbr\u003e \u003cb\u003eDoes your dog love you?\u003c/b\u003e \u003cbr\u003e Every dog lover knows the feeling. The nuzzle of a dog's nose, the warmth of them lying at our feet, even their whining when they want to get up on the bed. It really seems like our dogs love us, too. But for years, scientists have resisted that conclusion, warning against anthropomorphizing our pets. Enter Clive Wynne, a pioneering canine behaviorist whose research is helping to usher in a new era: one in which love, not intelligence or submissiveness, is at the heart of the human-canine relationship. Drawing on cuttingâe'edge studies from his lab and others around the world, Wynne shows that affection is the very essence of dogs, from their faces and tails to their brains, hormones, even DNA. This scientific revolution is revealing more about dogs' unique origins, behavior, needs, and hidden depths than we ever imagined possible.\u003cbr\u003e \u003cbr\u003e A humane, illuminating book,\u003ci\u003eDog Is Love\u003c/i\u003e is essential reading for anyone who has ever loved a dog--and experienced the wonder of being loved back.", \
                                        "ISBN": "9781328543967", "image_url": "http://books.google.com/books/publisher/content?id=T7-bDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&imgtk=AFLRE70oFaS9bNbP-kFpaUefEZoHfnj7aQf0Affb1mWIyZsO-pAEHwCD9YhsCEtSpXk8W_d1xnKHxOidynsJMaIn5e3LtQNHI_ZtDHhZXv-JZ0tAFb_3ysN6N6bWHU0ibpfpsyvXFrXx&source=gbs_api"}

  