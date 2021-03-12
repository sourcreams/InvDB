from glove import Glove
import Corpus

corpus = Corpus()

sent_token = [["안녕", "하세요"], ["지니티토리", "입니다"]]

corpus.fit(sent_token, window=20)

# model
glove = Glove(no_components=128, learning_rate=0.01)
glove.fit(corpus.matrix, epochs=50, no_threads=4, verbose=False)
glove.add_dictionary(corpus.dictionary)

# save
glove.save(DATA_DIR + '/glove_w20_epoch50.model')