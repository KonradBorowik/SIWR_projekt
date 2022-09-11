from turtle import distance
from typing import List
import cv2
from image import Image
from visualizer import get_images
from histograms import compare_histograms
from distance import calc_dist
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor


def f_b(prev_bbox_count: int, current_bbox_count: int):
    matrix = []
    for ver in range(current_bbox_count+1):
        row = []
        for hor in range(current_bbox_count+1):
            if ver == hor != 0:
                row.append(0)
            else:
                row.append(1)
        
        matrix.append(row)

    # print(f'f_b: {matrix}')
    return matrix


def f_u(hists: List, distances: List):
    matrices = []
    nodes = []
    print(f'bboxes count = {len(hists)}')
    for i_ob, object in enumerate(hists): #object_count
        # print(f'object {i_ob}: {object}')
        nodes.append(f'bbox_{i_ob}')
        obj_prob_matrix = [0.55]
        for i_bb, hist in enumerate(object): #connection options
            # print(f'hist {i_ob}: {hist}')
            obj_prob_matrix.append((hist * 0.5 + distances[i_ob][i_bb] * 0.1) / (0.5 + 0.1))
        matrices.append(obj_prob_matrix)
    # print(f'f_u: {matrices}')
    return matrices, nodes


def create_graph(f_b, f_u, nodes):
    Graph = FactorGraph()
    Graph.add_nodes_from(nodes)

    edges = []
    dfs = []
    print(len(nodes))
    print(len(f_u))
    print(f_u)
    for i, node in enumerate(nodes):
        df = DiscreteFactor([node], [len(f_u[i])], f_u[i])

    Graph.add_factors(df)


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
            distances = calc_dist(images[i-1], image)
            print(hists)
            matrix_f_b = f_b(images[i-1].bbox_count, image.bbox_count)
            print(f'f_b: {matrix_f_b}')
            matrices_f_u, nodes_names = f_u(hists, distances)
            print(f'f_u: {matrices_f_u}')
            print(nodes_names)

            create_graph(matrix_f_b, matrices_f_u, nodes_names)
            print('----')
            if i == 3:
                break
