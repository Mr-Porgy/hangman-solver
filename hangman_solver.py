import json
import requests
import random
import string
import secrets
import time
import re
import collections
try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse
    from urllib import urlencode


def guess(self, word): # word input example: "_ p p _ e "
        ###############################################
        # Replace with your own "guess" function here #
        ###############################################

        # clean the word so that we strip away the space characters
        # replace "_" with "." as "." indicates any character in regular expressions
               
        clean_word = word[::2].replace("_",".")
        
        # find length of passed word
        len_word = len(clean_word)

## existed_letters        
        existed_letters=[]
        existed_letters_num=0
        for letter in clean_word:
          if letter != '.':
            existed_letters_num+=1
            if letter not in existed_letters:
              existed_letters.append(letter)
        
        #print("guessed existed &d letters"  %len(existed_letters))
        #print(existed_letters_num)
        #print(len(self.guessed_letters))
        # grab current dictionary of possible words from self object, initialize new possible words dictionary to empty
        current_dictionary = self.current_dictionary
        new_dictionary = []
        
        # iterate through all of the words in the old plausible dictionary
        for dict_word in current_dictionary:
            # continue if the word is not of the appropriate length
            if len(dict_word) != len_word:
                continue
                
            # if dictionary word is a possible match then add it to the current dictionary
            if re.match(clean_word,dict_word):
                new_dictionary.append(dict_word)
                
        # overwrite old possible words dictionary with updated version
        self.current_dictionary = new_dictionary
        
## remove impossible letters in new_dictionary
#         list_to_remove=[]
#         for letter in self.guessed_letters:
#           for word in new_dictionary: 
#             if letter not in existed_letters and letter not in list_to_remove and letter in word:
#               list_to_remove.append(word)

#         for word in list_to_remove:
#           new_dictionary.remove(word)


## number of grams
        n=min(len_word-2,6)
        #print("using %d gram model" %n)
        if len_word<=3:
          n=len_word-1
          
## n-grams dictionary
        n_char_dictionary=[]
        for word in self.full_dictionary:
          if len(word)>(n-1):
            for i in range (0,len(word)-(n-1)):
              n_char_dictionary.append(word[i:i+n])

        n_c = collections.Counter(n_char_dictionary)
        n_sorted_letter_count = n_c.most_common() 

## most matched n-grams
        word_n_gram_list=[]
        for i in range(0,len(clean_word)-(n-1)):
          word_n_gram_list.append(clean_word[i:i+n])
        
        selected_ngram=""
        periodcount=99
        for grams in word_n_gram_list:
          if grams.count('.')<periodcount and grams.count('.')>0 :
            selected_ngram=grams
            periodcount=grams.count('.')
        #print(selected_ngram)

### Optimized regular expression on '.'

#         re_letter="[^"
#         for letter in self.guessed_letters:
#           if letter not in existed_letters:
#             re_letter+=letter
#         re_letter+=']'
        
#         optimized_ngram=""
#         for letter in selected_ngram:
#           if letter=='.':
#             optimized_ngram+=re_letter
#           else:
#             optimized_ngram+=letter
        
#         print(optimized_ngram)
                 
##### Get Regular Expression similar n gram dictionary      
        ngram_dictionary=[]
        # iterate through all of the words in the old plausible dictionary
        for dict_word in n_char_dictionary:

        


            # if dictionary word is a possible match then add it to the current dictionary
            if re.match(selected_ngram,dict_word):
                ngram_dictionary.append(dict_word)  
                
        # count occurrence of all n-grams in possible word matches              
        ngram_string = "".join(ngram_dictionary)
        
        c4 = collections.Counter(ngram_string)
        matched_ngram_sorted = c4.most_common()   
            
  
        # count occurrence of all characters in possible word matches
#         full_dict_string = "".join(new_dictionary)
        
#         c = collections.Counter(full_dict_string)
#         sorted_letter_count = c.most_common()                   
        
        guess_letter = '!'
        
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
#         print("new_dict length %d" %len(new_dictionary))
#         for letter,instance_count in sorted_letter_count:
#             if letter not in self.guessed_letters and len(new_dictionary)>500 and existed_letters_num<3:
#                 print("method 1")



### Guessing first half of letters in sorted letter frequencies
        #print(self.full_dictionary_common_letter_sorted[0:8])
        for letter,instance_count in self.full_dictionary_common_letter_sorted:
            if letter not in self.guessed_letters and existed_letters_num<int(len_word/2):    
                #print("method 1")             
                guess_letter = letter
                break

### Guessing E,I,A for the first half of letters
#         for letter in "eia":
#             if letter not in self.guessed_letters and existed_letters_num<int(len_word/2):    
#                 #print("method 1")             
#                 guess_letter = letter
#                 break
                
## Using n-grams frequency distribution in full training dictionary to take a guess     
## if less than half of letter are guessed correct, guess O,N,U untill there's enough to build n-gram
        if guess_letter == '!':
#           if existed_letters_num<int(len_word/3):
#             for letter in "onu":
#               if letter not in self.guessed_letters and existed_letters_num<int(4*len_word/7):    
#                 #print("method 1.5")             
#                 guess_letter = letter
#                 break
#           else:
          #print("method 2")
            #print(matched_ngram_sorted[0:5])
          for letter,instance_count in matched_ngram_sorted:
              if letter not in self.guessed_letters:
                  guess_letter = letter
                  break            
      
        # if no word matches in training dictionary, default back to ordering of full dictionary
        if guess_letter == '!':
            #print("method 2")
            sorted_letter_count = self.full_dictionary_common_letter_sorted
            for letter,instance_count in sorted_letter_count:
                if letter not in self.guessed_letters:
                    guess_letter = letter
                    break        
        return guess_letter


 
