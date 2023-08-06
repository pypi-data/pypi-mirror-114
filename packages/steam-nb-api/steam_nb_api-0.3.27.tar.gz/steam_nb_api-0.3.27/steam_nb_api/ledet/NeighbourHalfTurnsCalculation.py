import scipy.io
import numpy as np
import os
import h5py

def half_turn_from_meter(meters, sAvePositions, nodeTohalfTurn, el_order_half_turns):
    # el_turn value, meter index/key | dictionary
    elturn_from_length = dict(zip(sAvePositions, nodeTohalfTurn))

    # find the key with the closest value to meters, then returns the value of that key
    el_turn = elturn_from_length[meters] if meters in elturn_from_length else elturn_from_length[min(elturn_from_length.keys(), key=lambda k: abs(k-meters))]
    half_turn = el_order_half_turns[el_turn-1]

    return half_turn

def neighbours_recursive(magnet_object, near_neigh, magnet_name, geometry_dir):
    sAvePositions_path = geometry_dir + '/sAvePositions.mat'
    nodeTohalfTurn_path = geometry_dir + '/nodeToHalfTurn.mat'
    el_order_half_turns_path = geometry_dir + '/el_order_half_turns.mat'
    sAvePositions, nodeTohalfTurn, el_order_half_turns = load_geometries(sAvePositions_path, nodeTohalfTurn_path, el_order_half_turns_path)

    initial_position = magnet_object.Inputs.sim3D_Tpulse_sPosition

    height_from = magnet_object.Inputs.iContactAlongHeight_From
    height_to = magnet_object.Inputs.iContactAlongHeight_To

    width_from = magnet_object.Inputs.iContactAlongWidth_From
    width_to = magnet_object.Inputs.iContactAlongWidth_To

    neighbours = [half_turn_from_meter(initial_position, sAvePositions, nodeTohalfTurn, el_order_half_turns)]

    for _ in range(near_neigh):

        # El Order
        new_queue_el_order = []
        for turn in neighbours:
            i = np.where(el_order_half_turns == turn)
            i = int(i[0][0])

            if i != 0:
                new_queue_el_order.append(el_order_half_turns[i - 1])

            if i != (len(el_order_half_turns) - 1):
                new_queue_el_order.append(el_order_half_turns[i + 1])

        # Width and Height
        new_queue_w_h = []
        for f, t in zip(height_from, height_to):
            if f in neighbours:
                new_queue_w_h.append(t)

            if t in neighbours:
                new_queue_w_h.append(f)

        for f, t in zip(width_from, width_to):
            if f in neighbours:
                new_queue_w_h.append(t)

            if t in neighbours:
                new_queue_w_h.append(f)

        neighbours = np.hstack((neighbours, new_queue_el_order))
        neighbours = np.hstack((neighbours, new_queue_w_h))
        neighbours = np.array(list(dict.fromkeys(neighbours))) # remove duplicates

    #print('\n{} iterations => half-turns with finer mesh: {}'.format(near_neigh, len(neighbours)))

    return neighbours

def load_geometries(sAvePositions_path, nodeTohalfTurn_path, el_order_half_turns_path):
    sAvePositions_raw = scipy.io.loadmat(sAvePositions_path)
    nodeTohalfTurn_raw = scipy.io.loadmat(nodeTohalfTurn_path)
    el_order_half_turns_raw = scipy.io.loadmat(el_order_half_turns_path)

    sAvePositions = np.array(sAvePositions_raw['sAvePositions'][0])
    nodeTohalfTurn = np.array(nodeTohalfTurn_raw['nodeToHalfTurn'][0])
    el_order_half_turns = np.array(el_order_half_turns_raw['el_order_half_turns'][0])

    return sAvePositions, nodeTohalfTurn, el_order_half_turns
