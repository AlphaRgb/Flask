#!/usr/bin/env python3
# coding=utf-8

# import argparse
import tensorflow as tf

def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

# graph = load_graph('/Users/alpha/github/flask/flasky/app/cnn/model/frozen_model.pb')
#
# # We can verify that we can access the list of operations in the graph
# for op in graph.get_operations():
#     print(op.name)


# parser = argparse.ArgumentParser()
# parser.add_argument("--frozen_model_filename", default="results/frozen_model.pb", type=str,
#                     help="Frozen model file to import")
# parser.add_argument("--gpu_memory", default=.2, type=float, help="GPU memory per process")
# args = parser.parse_args()

##################################################
# Tensorflow part
##################################################
print('Loading the model')
graph = load_graph('/Users/alpha/github/flask/flasky/app/cnn/model/frozen_model.pb')
# graph = load_graph('/Users/alpha/github/model/frozen_model.pb')
x = graph.get_tensor_by_name('prefix/p_x:0')
y = graph.get_tensor_by_name('prefix/p_y:0')
keep_prob = graph.get_tensor_by_name('prefix/keep_prob:0')
print(x, y, keep_prob)
print('Starting Session, setting the GPU memory usage to %f' % .2)
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=.2)
sess_config = tf.ConfigProto(gpu_options=gpu_options)
persistent_sess = tf.Session(graph=graph, config=sess_config)

##################################################
# END Tensorflow part
##################################################