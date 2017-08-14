from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Input, MaxPooling1D, Convolution1D, Embedding
from keras.layers.merge import Concatenate
from keras import regularizers


def build_icd9_cnn_att_model(input_seq_length, 
                         max_vocab, external_embeddings, embedding_dim, embedding_matrix,
                         num_filters, filter_sizes,
                         training_dropout_keep_prob,
                         num_classes):
    #Embedding
    model_input = Input(shape=(input_seq_length, ))
    if external_embeddings:
        # use embedding_matrix 
        z = Embedding(max_vocab + 1,
                            embedding_dim,
                            weights=[embedding_matrix],
                            input_length=input_seq_length,
                            trainable=True)(model_input)
    else:
        # train embeddings 
        z =  Embedding(max_vocab + 1, 
                   embedding_dim, 
                   input_length=input_seq_length, embeddings_regularizer=regularizers.l2(0.0001),
                   name="embedding")(model_input)

    # Convolutional block
    conv_blocks = []
    for sz in filter_sizes:
        conv = Convolution1D(filters=num_filters,
                         kernel_size=sz,
                         padding="valid",
                         activation="relu",
                         strides=1)(z)
        # here attention layer instead of macPooling 
        #window_pool_size =  input_seq_length  - sz + 1 
        #conv = MaxPooling1D(pool_size=window_pool_size)(conv)  
        #conv = Flatten()(conv)
        #conv_blocks.append(conv)
        features_attention_vector = attention_util.attention_layerlock(conv)
    #concatenate
    z = Concatenate()(conv_blocks) if len(conv_blocks) > 1 else conv_blocks[0]
    z = Dropout(training_dropout_keep_prob)(z)

    #score prediction
    model_output = Dense(num_classes, activation="sigmoid")(z)

    #creating model
    model = Model(model_input, model_output)
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    
    print model.summary()

    return model