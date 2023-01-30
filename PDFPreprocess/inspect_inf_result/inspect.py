with open('inf.log', 'r', encoding='utf-8') as log_file, open('rec_banila_train.txt', 'r', encoding='utf-8') as GT_file:
    lines = [line[:-1].split('.png:') for line in log_file.readlines()]
    gt_dict = dict()
    for gt_line in GT_file.readlines():
        k, v = gt_line.split('\t')
        gt_dict[k[:-4]] = v[:-1]
    for idx, line in enumerate(lines):
        key = line[0].split("Predicts of ")[1]
        result = line[1][2:].split(", 0.")[0][:-1]
        gt = gt_dict[key]
        if gt != result:
            print(f"progress: {idx}/{len(lines)} path: {key}.png")
            print(f"result len: {len(result)} gt len: {len(gt)}")
            print(f"result:\t{result}")
            print(f"gt:\t\t{gt}\n")