import json
from collections import defaultdict


def create_labels_dict(files_labels, tag=None):
    labels_dict = {}
    for file in files_labels:
        if tag:
            file_id_clean = file.split("/")[-1].replace(f'__{tag}','')
        else:
            file_id_clean = file.split("/")[-1]
        labels_dict[file_id_clean] = {
            "file_id_clean": file_id_clean,
            "file": file
        }
    return labels_dict


def merge_labels(labels, labels_llm):
    common_labels = set(labels.keys()).intersection(set(labels_llm.keys()))
    print(f"Number of common labels: {len(common_labels)}")
    labels_final = {}
    for label in common_labels:
        with open(labels[label]["file"]) as f:
            label_data = json.load(f)
        with open(labels_llm[label]["file"]) as f:
            label_llm_data = json.load(f)
        file_id = label_data["file_id"]
        labels_final[file_id] = {
            "labels": {},
            "predicted_labels": {}
        }
        labels_final[file_id]["labels"]["names"] = label_data.get("names", [])
        labels_final[file_id]["labels"]["phone_numbers"] = label_data.get("phone_numbers", [])
        labels_final[file_id]["labels"]["email_addresses"] = label_data.get("email_addresses", [])
        labels_final[file_id]["labels"]["physical_addresses"] = label_data.get("physical_addresses", [])
        labels_final[file_id]["predicted_labels"]["names"] = label_llm_data.get("names", [])
        labels_final[file_id]["predicted_labels"]["phone_numbers"] = label_llm_data.get("phone_numbers", [])
        labels_final[file_id]["predicted_labels"]["email_addresses"] = label_llm_data.get("email_addresses", [])
        labels_final[file_id]["predicted_labels"]["physical_addresses"] = label_llm_data.get("physical_addresses", [])

    return labels_final


def calculate_metrics(data):
    metrics = defaultdict(lambda: {"TP": 0, "FP": 0, "FN": 0})

    for _, item in data.items():
        gt_labels = item['labels']
        pred_labels = item['predicted_labels']

        for category in gt_labels:
            gt_entities = set(gt_labels[category])
            pred_entities = set(pred_labels[category])

            TP = len(gt_entities.intersection(pred_entities))
            FP = len(pred_entities - gt_entities)
            FN = len(gt_entities - pred_entities)

            metrics[category]["TP"] += TP
            metrics[category]["FP"] += FP
            metrics[category]["FN"] += FN

    for category in metrics:
        TP = metrics[category]["TP"]
        FP = metrics[category]["FP"]
        FN = metrics[category]["FN"]

        precision = TP / (TP + FP) if TP + FP > 0 else 0
        recall = TP / (TP + FN) if TP + FN > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

        metrics[category].update({"Precision": precision, "Recall": recall, "F1 Score": f1})

    return metrics


def calculate_overall_metrics(metrics):
    total_TP = sum([metrics[category]["TP"] for category in metrics])
    total_FP = sum([metrics[category]["FP"] for category in metrics])
    total_FN = sum([metrics[category]["FN"] for category in metrics])

    overall_precision = total_TP / (total_TP + total_FP) if total_TP + total_FP > 0 else 0
    overall_recall = total_TP / (total_TP + total_FN) if total_TP + total_FN > 0 else 0
    overall_f1 = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall) if overall_precision + overall_recall > 0 else 0

    return {
        "Overall Precision": overall_precision,
        "Overall Recall": overall_recall,
        "Overall F1 Score": overall_f1
    }
