import wolframalpha
import wikipedia
client = wolframalpha.Client('K9T6JG-KJVJTEK8X7')


while True:
    query = input("Enter: ")
    try:
            try:
                res = client.query(query)
                results = next(res.results).text
                print(results)
                        
            except:
                results = wikipedia.summary(query, sentences=2)
                print("Here's is something I've found on our server - ")
                print(results)
            
    except:
        print("Sorry some servers are not responding, please try again later ")