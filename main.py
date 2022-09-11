from typing import List
from visualizer import get_images
from histograms import compare_histograms
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference.ExactInference import BeliefPropagation
from itertools import combinations
import argparse
from pathlib import Path


def f_b(prev_bbox_count: int):
    '''
    create matrix that consists of 1 with 0 on the diagonal. element [0][0] equals 1!
    '''    
    matrix = []
    for ver in range(prev_bbox_count+1):
        row = []
        for hor in range(prev_bbox_count+1):
            if ver == hor != 0:
                row.append(0)
            else:
                row.append(1)
        
        matrix.append(row)

    return matrix


def f_u(hists: List, bboxes_count_prev, bboxes_count_curr):
    '''
    Create matrices with probability factor of object from current img being the same object from previous picture.
    '''
    matrices = []
    nodes = []
    for i_ob in range(bboxes_count_curr):
        obj_prob_matrix = [0.55]
        nodes.append(f'bbox_{i_ob}')
        for i_bb in range(bboxes_count_prev):
            obj_prob_matrix.append(hists[i_ob][i_bb] *10)
        matrices.append(obj_prob_matrix)
    return matrices, nodes


def create_graph(f_b, f_u, nodes, curr_bbox_count):
    '''
    Creating graph nodes/edges
    '''
    Graph = FactorGraph()
    Graph.add_nodes_from(nodes)

    # create single connections object->f_u
    for i, node in enumerate(nodes):
        df = DiscreteFactor([node], [len(f_u[0])], f_u[i])
        Graph.add_factors(df)
        Graph.add_node(df)
        Graph.add_edge(node, df)
    combs = [x for x in combinations(nodes, 2)]
    
    #create more nodes and edges if there are more than one object found in image
    if curr_bbox_count > 1:
        for i in range(len(combs)):
            df = DiscreteFactor([combs[i][0], combs[i][1]], [len(f_b), len(f_b)], f_b)
            Graph.add_factors(df)
            Graph.add_node(df)
            Graph.add_edge(combs[i][0], df)
            Graph.add_edge(combs[i][1], df)

    # finalize graph creation, calculate and get outcome
    Graph.check_model()
    bp = BeliefPropagation(Graph)
    bp.calibrate()
    values = bp.map_query(Graph.get_variable_nodes(), show_progress=False)
    
    return values


def printing_outcome(values, nodes):
    outcome = []
    for node in nodes:
        bbox_number = values[node]
        outcome.append(bbox_number - 1)
    
    string = ''
    for out in outcome:
        string += str(out) + ' '

    print(string[:-1])


if __name__ == '__main__':
    # get path to read imnages from
    parser = argparse.ArgumentParser()
    parser.add_argument('images_dir', type=str)
    args = parser.parse_args()
    images_dir = Path(args.images_dir)

    # read images
    images = get_images(images_dir)

    for i, image in enumerate(images):
        if i == 0:
            # print new bboxes for first image
            print(f'-1 ' * image.bbox_count)
        hists = []
        if i > 0:
            if image.bbox_count == 0:
                # print empty line if no bboxes on current image
                print()
            elif images[i-1].bbox_count == 0:
                # print -1 for every new bbox
                print(f'-1 ' * image.bbox_count)
            else:
                # get comparison data
                hists = compare_histograms(images[i-1], image)
                
                #create f_u and f_b matrices
                matrix_f_b = f_b(images[i-1].bbox_count)
                matrices_f_u, nodes_names = f_u(hists, images[i-1].bbox_count, image.bbox_count)

                #create graph
                outcome = create_graph(matrix_f_b, matrices_f_u, nodes_names, image.bbox_count)
                #print result
                printing_outcome(outcome, nodes_names)
