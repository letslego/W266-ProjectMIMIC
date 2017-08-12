from keras.models import  Model
from keras.layers import Dense, Dropout, Flatten, Input,  Embedding,Bidirectional
from keras.layers.merge import Concatenate
from keras.layers import LSTM
from keras.layers import  MaxPooling1D, Embedding, Merge, Dropout, LSTM, Bidirectional
from keras.layers.merge import Concatenate
from keras.layers.core import *
from keras.layers import merge, dot, add
from keras import backend as K

def attention_3d_block(inputs, TIME_STEPS):
    # inputs.shape = (batch_size, time_steps, input_dim)
    input_dim = int(inputs.shape[2])
    # (4) alpah_it: then we measure the importance of x as the similarity of u_it with a x level
	#     context vector u_w and get a normalized importance weight alpha_it through a softmax function
    a = Permute((2, 1))(inputs)
    a = Reshape((input_dim, TIME_STEPS))(a)
    a = Dense(TIME_STEPS, activation='softmax')(a)
    
	# (5) s_i: After that, we compute the sentence vector s_i as a weighted sum of the word annotations based on the weights alpha_it.
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul') 
    sum_vector = Lambda(lambda x: K.sum(x, axis=1))(output_attention_mul)    
    return sum_vector

def build_lstm_att_model(input_seq_length, 
                         max_vocab, external_embeddings, embedding_trainable, embedding_dim, embedding_matrix,                         
                         num_classes):
    #Embedding
    model_input = Input(shape=(input_seq_length, ))
    if external_embeddings:
        # use embedding_matrix 
        z = Embedding(max_vocab + 1,
                            embedding_dim,
                            weights=[embedding_matrix],
                            input_length=input_seq_length,
                            trainable=embedding_trainable)(model_input)
    else:
        # train embeddings 
        z =  Embedding(max_vocab + 1, 
                   embedding_dim, 
                   input_length=input_seq_length, 
                   name="embedding")(model_input)

    # LSTM
    l_lstm = LSTM(100,return_sequences=True)(z)
    
    #attention
    words_attention_vector = attention_3d_block(l_lstm,input_seq_length) 
    
    #score prediction 
    model_output = Dense(num_classes, activation="sigmoid")(words_attention_vector)

    #creating model
    model = Model(model_input, model_output)
    # what to use for tf.nn.softmax_cross_entropy_with_logits?
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    #model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    print model.summary()

    return model