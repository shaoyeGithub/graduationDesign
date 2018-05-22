# from getbottleneck import get_bottleneck
import tensorflow as tf
import sys
import os
import numpy as np
import json
import argparse
from tensorflow.python.platform import gfile
from graduation.diagnosis.getbottleneck import get_bottleneck
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 忽略烦人的警告


def testall(filepath):
    filelist = os.listdir(filepath)
    files = []
    num_positive = 0
    for i in range(len(filelist)):
        child = os.path.join('%s\\%s' % (filepath, filelist[i]))
        imagename = child.split(filepath + "\\")
        if "1" in imagename[1]:
            print(imagename[1])
            image_input = get_bottleneck(child)
            image_input = [np.asarray(image_input)]

            # Set up saved trained model
            with gfile.FastGFile('model/savedgraph.pbtxt', 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')

            with tf.Session() as sess:
                prediction = sess.graph.get_tensor_by_name('Softmax:0')
                inputs = sess.graph.get_tensor_by_name('inputs:0')
                new_saver = tf.train.import_meta_graph('./model/savedmodel.meta')
                new_saver.restore(sess, tf.train.latest_checkpoint('./model'))

                prediction = sess.run(prediction, feed_dict={inputs: image_input})

                print('n score: {}'.format(prediction[0][0]))
                print('p score: {}'.format(prediction[0][1]))

                if prediction[0][1] > 0.5:
                    num_positive += 1;

                    # print("num_positive:"+num_positive)


# testall("train1")
def testOne(fileName):
    image_input = get_bottleneck(fileName)
    image_input = [np.asarray(image_input)]

    # Set up saved trained model
    with gfile.FastGFile('./model/savedgraph.pbtxt', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:

        prediction = sess.graph.get_tensor_by_name('Softmax:0')
        # print("123")
        inputs = sess.graph.get_tensor_by_name('inputs:0')
        # print("23")
        print(os.path.abspath('./model/savedmodel.meta'))
        new_saver = tf.train.import_meta_graph('./model/savedmodel.meta')#这句出错了
        # print("3")
        new_saver.restore(sess, tf.train.latest_checkpoint('./model'))
        prediction = sess.run(prediction, feed_dict={inputs: image_input})

        print('n score: {}'.format(prediction[0][0]))
        print('p score: {}'.format(prediction[0][1]))

    if prediction[0][0] > 0.5:
        return True
    else:
        return False

            # flag=testOne(r"C:\Users\FEITENG\Desktop\GraduationDesign\LymphaticData\biwei\src\biwei\merge\124.jpg")
            # print(flag)
