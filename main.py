import pandas as pd
import nltk
import long_responses as long

#Load dataframe
mental_health_dataset = pd.read_csv('Mental_Health_FAQ.csv')

#initialize a dictionary
response_patterns = {}

#Add responses from dataset
for index, row in mental_health_dataset.iterrows():
    user_message = row['Questions'].lower()
    response = row['Answers']
    response_patterns[user_message] = response

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    #counts how many words are present
    for word in user_message.split():
        if word in recognised_words:
            message_certainty += 1

    #Calculating the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    #checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    #must either have the required words or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages():
    while True:
        #Using NLP to extract keywords from the user's input
        user_message = input('You: ')
        user_keywords = nltk.word_tokenize(user_message)

        highest_prob_list = {}

        # Simplifies response creation / adds it to the dict
        def response(bot_response, list_of_words, single_response=False, required_words=[]):
            nonlocal highest_prob_list
            highest_prob_list[bot_response] = message_probability(user_message, list_of_words, single_response, required_words)

        #Responses
        response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
        response('See you!', ['bye', 'goodbye'], single_response=True)
        response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
        response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
        response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

        #Longer responses
        response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
        response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
        response(long.R_HEALTH, ['depression', 'symptoms', 'causes', 'treatment'], single_response=True)

        #Find the response with the highest probability
        best_match = max(highest_prob_list, key=highest_prob_list.get)

        #If the probability is high enough, return the response
        if highest_prob_list[best_match] >= 50:
            print(best_match)
        else:
            print('Sorry, I don\'t understand.')

if __name__ == '__main__':
    check_all_messages()