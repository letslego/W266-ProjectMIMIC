from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Input, Convolution1D
from keras.layers import Conv1D, MaxPooling1D, Embedding, Merge, Dropout, LSTM, GRU, Bidirectional, TimeDistributed
from keras.layers.merge import Concatenate
from keras.layers.core import *
from keras.layers import merge, dot, add
from keras import backend as K

import attention_util

# based on paper: Hierarchical Attention networks for document classification
# starting code from:
# * https://github.com/richliao/textClassifier/blob/master/textClassifierHATT.py
# but the github sources above had misteakes that had been corrected here

def conv_layer(input,input_seq_length, num_filters,filter_sizes): 
    
    conv_blocks = []
    for sz in filter_sizes:
        conv = Convolution1D(filters=num_filters,                         
                         kernel_size=sz,
                         padding="valid",
                         activation="relu",
                         strides=1)(input)
        window_pool_size =  input_seq_length  - sz + 1 
        conv = MaxPooling1D(pool_size=window_pool_size)(conv)  
        conv = Flatten()(conv)
        conv_blocks.append(conv)

    #concatenate
    z = Concatenate()(conv_blocks) if len(conv_blocks) > 1 else conv_blocks[0]
    return z





def build_hierarhical_att_model(MAX_SENTS, MAX_SENT_LENGTH, 
                         max_vocab, embedding_dim, num_filters,filter_sizes, 
                         num_classes):
    
    # WORDS in one SENTENCE LAYER
    #-----------------------------------------
    #Embedding
	# note_input [sentences, words_in_a_sentence]
    sentence_input = Input(shape=(MAX_SENT_LENGTH,), dtype='int32')
    # use embedding_matrix 
	# (1) embed the words to vectors through an embedding matrix
    #embedded_sequences = Embedding(max_vocab + 1,
    #                       embedding_dim,
    #                       weights=[embedding_matrix],
    #                        input_length=MAX_SENT_LENGTH,
    #                        trainable=True)(sentence_input)
    embedded_sequences =  Embedding(max_vocab + 1, 
                   embedding_dim, 
                   input_length=MAX_SENT_LENGTH, embeddings_regularizer=regularizers.l2(0.0001),
                   name="embedding")(sentence_input)

	# (2) GRU to get annotations of words by summarizing information
    #     h_it: We obtain an annotation for a given word  by concatenating the forward hidden state  and
    #     backward hidden state
    h_it_sentence_vector = Bidirectional(GRU(50, return_sequences=True))(embedded_sequences)
    #sentence_vector = conv_layer(embedded_sequences, MAX_SENT_LENGTH, num_filters,filter_sizes)
    
	#  Attention layer
	#  Not all words contribute equally to the representation of the sentence meaning.
	#  Hence, we introduce attention mechanism to extract such words that are important to the meaning of the
	#  sentence and aggregate the representation of those informative words to form a sentence vector
	
	# (3) u_it: we first feed the word annotation through a one-layer MLP to get the hidden representation u_it
    #l_dense = TimeDistributed(Dense(10))(sentence_vector)

    words_attention_vector = attention_util.attention_layer(h_it_sentence_vector,MAX_SENT_LENGTH) 
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
    document_vector = Bidirectional(GRU(50, return_sequences=True))(note_encoder)
    #document_vector = conv_layer(note_encoder,MAX_SENTS, num_filters,filter_sizes)
    
	#attention layer
    #l_dense_sent = TimeDistributed(Dense(250))(document_vector)
    sentences_attention_vector = attention_util.attention_layer(document_vector,MAX_SENTS) 
    #l_att_sent = Flatten()(attention_mul_sent)
	# output layer
    preds = Dense(num_classes, activation='sigmoid', name='preds')(sentences_attention_vector)
    
    #model
    model = Model(note_input, preds)

    #model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=False)
    model.compile(loss="binary_crossentropy", optimizer="sgd", metrics=["accuracy"])

    print("model fitting - Hierachical Attention GRU")
    print model.summary()

    return model