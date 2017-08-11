from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Input, Convolution1D
from keras.layers import Conv1D, MaxPooling1D, Embedding, Merge, Dropout, LSTM, GRU, Bidirectional, TimeDistributed
from keras.layers.merge import Concatenate
from keras.layers.core import *
from keras.layers import merge, dot, add
from keras import backend as K

# based on paper: Hierarchical Attention networks for document classification
# starting code from:
# * https://github.com/richliao/textClassifier/blob/master/textClassifierHATT.py
# * https://github.com/philipperemy/keras-attention-mechanism/blob/master/attention_lstm.py

SINGLE_ATTENTION_VECTOR = False

def attention_3d_block(inputs, TIME_STEPS):
    # inputs.shape = (batch_size, time_steps, input_dim)
    input_dim = int(inputs.shape[2])
    # (4) alpah_it: then we measure the importance of x as the similarity of u_it with a x level
	#     context vector u_w and get a normalized importance weight alpha_it through a softmax function
    a = Permute((2, 1))(inputs)
    a = Reshape((input_dim, TIME_STEPS))(a)
    a = Dense(TIME_STEPS, activation='softmax')(a)
    
	# (5) s_i: After that, we compute the sentence vector s_i as a weighted sum of the word annotations based on the weights alpha_it.
    if SINGLE_ATTENTION_VECTOR:
        a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
        a = RepeatVector(input_dim)(a)
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    print output_attention_mul.shape   
    # w266 where is the sum?
    #sum_vector = add(output_attention_mul, name= 'attention_sum')
    #sum_vector = merge( output_attention_mul, name='attention_add', mode='add') 
    sum_vector = Lambda(lambda x: K.sum(x, axis=1))(output_attention_mul)
    #K.sum(output_attention_mul, axis=1)
    
    return sum_vector



def build_gru_att_model(MAX_SENTS, MAX_SENT_LENGTH, 
                         max_vocab, embedding_dim, embedding_matrix,
                         num_classes):
    
    # WORDS in one SENTENCE LAYER
    #-----------------------------------------
    #Embedding
	# note_input [sentences, words_in_a_sentence]
    sentence_input = Input(shape=(MAX_SENT_LENGTH,), dtype='int32')
    # use embedding_matrix 
	# (1) embed the words to vectors through an embedding matrix
    embedded_sequences = Embedding(max_vocab + 1,
                            embedding_dim,
                            weights=[embedding_matrix],
                            input_length=MAX_SENT_LENGTH,
                            trainable=True)(sentence_input)

	# (2) GRU to get annotations of words by summarizing information
    #     h_it: We obtain an annotation for a given word  by concatenating the forward hidden state  and
    #     backward hidden state
    l_lstm = Bidirectional(GRU(100, return_sequences=True))(embedded_sequences)
	#  Attention layer
	#  Not all words contribute equally to the representation of the sentence meaning.
	#  Hence, we introduce attention mechanism to extract such words that are important to the meaning of the
	#  sentence and aggregate the representation of those informative words to form a sentence vector
	
	# (3) u_it: we first feed the word annotation through a one-layer MLP to get the hidden representation u_it
    l_dense = TimeDistributed(Dense(200))(l_lstm)

    words_attention_vector = attention_3d_block(l_dense,MAX_SENT_LENGTH) 
    #l_att = Flatten()(attention_mul) 

	#  Keras model that process words in one sentence
    sentEncoder = Model(sentence_input, words_attention_vector)
    
    print sentEncoder.summary()

    # SENTENCE LAYER
    #---------------------------------------------------------------------------------------------------------------------
    note_input = Input(shape=(MAX_SENTS,MAX_SENT_LENGTH), dtype='int32')
	# TimeDistributes wrapper applies a layer to every temporal slice of an input.
	# The input should be at least 3D, and the dimension of index one will be considered to be the temporal dimension
	# Here the sentEncoder is applied to each input record (a note) 
    note_encoder = TimeDistributed(sentEncoder)(note_input)
    l_lstm_sent = Bidirectional(GRU(100, return_sequences=True))(note_encoder)
	#attention layer
    l_dense_sent = TimeDistributed(Dense(200))(l_lstm_sent)
    sentences_attention_vector = attention_3d_block(l_dense_sent,MAX_SENTS) 
    #l_att_sent = Flatten()(attention_mul_sent)
	# output layer
    preds = Dense(num_classes, activation='softmax', name='preds')(sentences_attention_vector)
    
    #model
    model = Model(note_input, preds)

    #model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    print("model fitting - Hierachical Attention GRU")
    print model.summary()

    return model