import traceback
import argparse

def read_input_file(input_file):
    pid_to_text = {}
    with open(input_file, 'r') as f:
        for line in f:
            pid = line[:9]
            text = line[9:].strip()
            pid_to_text[pid] = text
    return pid_to_text


def read_label_file(pid_to_text, label_file):
    '''
    读取纠正结果
    :param filename:
    :return:
    '''
    error_set, det_set, cor_set = set(), set(), set()
    with open(label_file, 'r', encoding='utf-8') as f:
        for line in f:
            terms = line.strip().split(',')
            terms = [t.strip() for t in terms]
            pid = terms[0]
            if pid not in pid_to_text:
                continue
            if len(terms) == 2 and terms[-1] == '-1':
                continue
            text = pid_to_text[pid]
            if (len(terms)-2) % 4 == 0:
                error_num = int((len(terms)-2) / 4)
                for i in range(error_num):
                    loc, typ, wrong, correct = terms[i*4+1: (i+1)*4+1]
                    loc = int(loc)
                    cor_text = text[:loc] + correct + text[loc+len(wrong):]
                    error_set.add((pid, loc, wrong, cor_text))
                    det_set.add((pid, loc, wrong))
                    cor_set.add((pid, cor_text))
            else:
                raise Exception('check your data format: {}'.format(line))
    assert len(error_set) == len(det_set) == len(cor_set)
    return error_set, det_set, cor_set


def cal_f1(ref_num, pred_num, right_num):
    precision = float(right_num) / pred_num
    recall = float(right_num) / ref_num
    if precision + recall < 1e-6:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return f1 * 100


def evaluate(input_file, ref_file, pred_file):
    pid_to_text = read_input_file(input_file)
    ref_error_set, ref_det_set, ref_cor_set = read_label_file(pid_to_text, ref_file)
    pred_error_set, pred_det_set, pred_cor_set = read_label_file(pid_to_text, pred_file)

    ref_num = len(ref_cor_set)
    pred_num = len(pred_cor_set)

    det_right_num = 0
    for error in ref_error_set:
        pid, loc, wrong, cor_text = error
        if (pid, loc, wrong) in pred_det_set or (pid, cor_text) in pred_cor_set:
            det_right_num += 1
    detect_f1 = cal_f1(ref_num, pred_num, det_right_num)
    
    cor_right_num = len(ref_cor_set & pred_cor_set)
    correct_f1 = cal_f1(ref_num, pred_num, cor_right_num)

    final_score = 0.8 * detect_f1 + 0.2 * correct_f1
    print("detect_f1: {}".format(detect_f1))
    print("correct_f1: {}".format(correct_f1))
    print("final_score: {}".format(final_score))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',
                        help='Path to the input file',
                        required=True)
    parser.add_argument('-r', '--ref_file',
                        help='Path to the reference label file',
                        required=True)
    parser.add_argument('-p', '--pred_file',
                        help='Path to the predict label file',
                        required=True)
    args = parser.parse_args()
    try:
        evaluate(args.input_file, args.ref_file, args.pred_file)
    except:
        traceback.print_exc()
