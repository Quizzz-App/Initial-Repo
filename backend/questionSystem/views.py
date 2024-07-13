from django.shortcuts import render

# Create your views here.

def index(request):
    if request.method == 'POST':
        pass
    context= {
        'categories': ["music", "sport_and_leisure", "film_and_tv", "arts_and_literature", "history", "general_knowledge"],
        'levels': ["easy", "medium", "hard"],
    }
    return render(request, 'quiz/quiz_index.html', context= context)

'''
categories

  

 
 
 "society_and_culture"
 "science" 
 "geography" 
 "food_and_drink"
  

  difficulty
  "easy" 
  "medium"
   "hard"
limit 1- 50
f"https://the-trivia-api.com/api/questions?categories={self.categoriess}&limit={self.question_limit}&difficulty={self.level}"


'''
