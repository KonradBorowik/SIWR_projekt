from turtle import distance
from typing import List
import cv2
from image import Image
from visualizer import get_images
from histograms import compare_histograms
from distance import calc_dist
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference.ExactInference import BeliefPropagation
from itertools import combinations


def f_b(prev_bbox_count: int, current_bbox_count: int):
    matrix = []
    for ver in range(prev_bbox_count+1):
        row = []
        for hor in range(prev_bbox_count+1):
            if ver == hor != 0:
                row.append(0)
            else:
                row.append(1)
        
        matrix.append(row)

    # print(f'f_b: {matrix}')
    return matrix


def f_u(hists: List, bboxes_count_prev, bboxes_count_curr):
    matrices = []
    nodes = []
    print(f'bboxes count = {len(hists)}')
    for i_ob in range(bboxes_count_curr): #object_count
        obj_prob_matrix = [0.55]
        # print(i_ob)
        # print(f'object {i_ob}: {object}')
        nodes.append(f'bbox_{i_ob}')
        for i_bb in range(bboxes_count_prev): #connection options
            #  print(f'hist {i_ob}: {hist}')
            print(hists[i_ob][i_bb])
            # print(distances[i_ob][i_bb])
            obj_prob_matrix.append((hists[i_ob][i_bb] * 0.5) / 0.5)
        matrices.append(obj_prob_matrix)
    # print(f'f_u: {matrices}')
    return matrices, nodes


def create_graph(f_b, f_u, nodes, curr_bbox_count):
    Graph = FactorGraph()
    Graph.add_nodes_from(nodes)

    print(len(nodes))
    print(f_u[0])
    # print(f_u)
    for i, node in enumerate(nodes):
        df = DiscreteFactor([node], [len(f_u[0])], f_u[i])
        Graph.add_factors(df)
        Graph.add_node(df)
        Graph.add_edge(node, df)
    combs = [x for x in combinations(nodes, 2)]
    if curr_bbox_count > 1:
        for i in range(len(combs)):
            df = DiscreteFactor([combs[i][0], combs[i][1]], [len(f_b), len(f_b)], f_b)
            Graph.add_factors(df)
            Graph.add_node(df)
            Graph.add_edge(combs[i][0], df)
            Graph.add_edge(combs[i][1], df)

    print(Graph)
    Graph.check_model()
    bp = BeliefPropagation(Graph)


if __name__ == '__main__':
    images = get_images()
    for i, image in enumerate(images):
        hists = []
        distances = []
        if i > 0:
            print(f'pair {i}')
            if images[i-1].bbox_count == 0 or image.bbox_count == 0:
                print()
                continue
            print(f'prev bbox count = {images[i-1].bbox_count}')
            print(f'curr bbox count = {image.bbox_count}')
            hists = compare_histograms(images[i-1], image)
            # distances = calc_dist(images[i-1], image)
            print(hists)
            # print(distances)
            
            matrix_f_b = f_b(images[i-1].bbox_count, image.bbox_count)
            print(f'f_b: {matrix_f_b}')
            matrices_f_u, nodes_names = f_u(hists, images[i-1].bbox_count, image.bbox_count)
            print(f'f_u: {matrices_f_u}')
            print(nodes_names)

            create_graph(matrix_f_b, matrices_f_u, nodes_names, image.bbox_count)
            print('----')
            if i == 3:
                break
