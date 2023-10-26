from flask import Flask, request, render_template, redirect
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
popular_book = pickle.load(open('popular_book.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           rating=list(np.round(popular_df['avg_rating'].values,2)),
                           votes=list(popular_df['num_rating'].values)
                           )
                           

@app.route('/recommend')
def rec():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    if not(user_input):
        return redirect('/')
    def recommend(book_name):
        index=np.where(pt.index==book_name)[0][0]
        similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title']==pt.index[i[0]]]
            temp_rating=popular_book[popular_book['Book-Title']==pt.index[i[0]]]
            temp_rating.drop_duplicates('Book-Title',inplace=True)
            temp_df.drop_duplicates('Book-Title', inplace=True)
            item = []
            item.extend(list(temp_df['Book-Title'].values))
            item.extend(list(temp_df['Book-Author'].values))
            item.extend(list(temp_df['Image-URL-M'].values))
            item.extend(list(np.round(temp_rating['avg_rating'].values,1)))
            item.extend(list(temp_rating['num_rating'].values))
            data.append(item)
        return data
    data = recommend(user_input)
    if data.empty():
        return "<h1>No Such Movie Found</h1>"
    return render_template('recommend.html',
                           data=data)

if __name__=='__main__':
    app.run(debug=True)
