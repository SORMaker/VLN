import json, os
scan_dir = "matterport_mesh/v1/scans"

preds_path = "/home/xiezy/projects/VLN-Tutorial/MapGPT/datasets/exprs_map/4o/test/preds"
connentivity_path = "/home/xiezy/projects/VLN-Tutorial/visualization/topdown_map/connectivity"
mapgpt_json_save_folder = 'output_json_files/mapgpt_json_files'

groundtruth_json_path = '/home/xiezy/projects/VLN-Tutorial/visualization/topdown_map/train_shortest_agent/train_shortest_agent.json'
groundtruth_json_save_folder = 'output_json_files/groundtruth_json_files'

seq_json_path = '/home/xiezy/projects/VLN-Tutorial/visualization/topdown_map/seq_agent/seq2seq_teacher_imagenet_train_iter_20000.json'
seq_json_save_folder = '/home/xiezy/projects/VLN-Tutorial/visualization/topdown_map/output_json_files/seq_json_files'
def get_mapgpt_list(scans, instr_path):
    result = []
    for scan in scans:
        for path in instr_path:
            instr_json = preds_path + "/" + path
            with open(instr_json) as f:
                mapgpt_instr_data = json.load(f)
                if mapgpt_instr_data['scan'] == scan:
                    temp_id, temp_tj = mapgpt_instr_data['instr_id'], mapgpt_instr_data['trajectory']
                    result.append({"instr_id": temp_id, "scan": scan, "trajectory": temp_tj})
    return result

def get_gen_json(conn_json_path, map_list):
    gen_josn=[]
    trajectory = map_list['trajectory']
    # print(trajectory)
    with open(conn_json_path) as f:
        conn_data = json.load(f)
    for tj in trajectory:
        for i, item in enumerate(conn_data):
            if tj[0] in item['image_id']:
                gen_josn.append(conn_data[i])
    return gen_josn

def mapgpt_json_gen():
    files = os.listdir(scan_dir)

    if not os.path.exists(mapgpt_json_save_folder):
        os.makedirs(mapgpt_json_save_folder)

    conn_files = os.listdir(connentivity_path)
    conn_subfiles = {file:j for file in files for j in conn_files if file in j}

    mapgpt_instr_path = os.listdir(preds_path)
    mapgpt_list = get_mapgpt_list(files, mapgpt_instr_path)              

    for map in mapgpt_list:
        conn_json_path = connentivity_path + "/" + conn_subfiles[map['scan']]
        gen_json = get_gen_json(conn_json_path, map)
        file_path = os.path.join(mapgpt_json_save_folder, '%s_%s.json' % (map['scan'], map['instr_id']))
        with open(file_path, 'w') as fp:
            json.dump(gen_json, fp)
        # with open('%s_%s.json' % (map['scan'], map['instr_id']), 'w') as fp:
        #     json.dump(gen_json, fp)

def jolin_mesh_gen():
    jolin_mesh_names = []
    print(f"Current working directory: {os.getcwd()}")
    files = os.listdir(scan_dir)
    for id, name in enumerate(files):
        subfolder = os.listdir(scan_dir + "/" + name + "/matterport_mesh/")
        jolin_mesh_names.append([name,subfolder[0]])
        
    with open('mesh_json/jolin_mesh_names.json', 'w') as fp:
        json.dump(jolin_mesh_names, fp)

def groundTruth_json_gen():
    files = os.listdir(scan_dir)
    if not os.path.exists(groundtruth_json_save_folder):
        os.makedirs(groundtruth_json_save_folder)

    with open(groundtruth_json_path) as f:
        groundtruth_data = json.load(f)
    
    conn_files = os.listdir(connentivity_path)
    conn_subfiles = {file:j for file in files for j in conn_files if file in j}

    mapgpt_instr_path = os.listdir(preds_path)
    mapgpt_list = get_mapgpt_list(files, mapgpt_instr_path)
    groundtruth_map_data = []
    for map in mapgpt_list:
        for i, item in enumerate(groundtruth_data):
            groundtruth_tj = []
            if map['instr_id'] == item['instr_id']:
                for tj in item['trajectory']:
                    groundtruth_tj.append([tj[0]])
                groundtruth_map_data.append({"instr_id": item['instr_id'], "scan": map['scan'], "trajectory": groundtruth_tj})

    for map in groundtruth_map_data:
        conn_json_path = connentivity_path + "/" + conn_subfiles[map['scan']]
        # print(groundtruth_map_data)
        gen_groundtruth_json = get_gen_json(conn_json_path, map)
        file_path = os.path.join(groundtruth_json_save_folder, '%s_%s.json' % (map['scan'], map['instr_id']))
        with open(file_path, 'w') as fp:
            json.dump(gen_groundtruth_json, fp)

def seq_json_gen():
    files = os.listdir(scan_dir)
    if not os.path.exists(seq_json_save_folder):
        os.makedirs(seq_json_save_folder)

    with open(seq_json_path) as f :
        seq_data = json.load(f)
    print(len(seq_data))

    conn_files = os.listdir(connentivity_path)
    conn_subfiles = {file:j for file in files for j in conn_files if file in j}

    mapgpt_instr_path = os.listdir(preds_path)
    mapgpt_list = get_mapgpt_list(files, mapgpt_instr_path)

    seq_map_data = []
    for map in mapgpt_list:
        for i, item in enumerate(seq_data):
            seq_tj = []
            if map['instr_id'] == item['instr_id']:
                for tj in item['trajectory']:
                    seq_tj.append([tj[0]])
                seq_map_data.append({"instr_id": item['instr_id'], "scan": map['scan'], "trajectory": seq_tj})

    for map in seq_map_data:
        conn_json_path = connentivity_path + "/" + conn_subfiles[map['scan']]
        # print(groundtruth_map_data)
        gen_seq_json = get_gen_json(conn_json_path, map)
        file_path = os.path.join(seq_json_save_folder, '%s_%s.json' % (map['scan'], map['instr_id']))
        with open(file_path, 'w') as fp:
            json.dump(gen_seq_json, fp)

def main():
    jolin_mesh_gen()
    mapgpt_json_gen()
    groundTruth_json_gen()
    seq_json_gen()

if __name__ == "__main__":
    main()