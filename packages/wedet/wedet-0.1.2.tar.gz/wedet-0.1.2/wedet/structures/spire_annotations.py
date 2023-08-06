#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os
import sys
import logging
import numpy as np
import cv2
import torch

from ..structures.boxes import Boxes
from ..structures.instances import Instances


def find_contours(*args, **kwargs):
    """
    Wraps cv2.findContours to maintain compatiblity between versions
    3 and 4
    Returns:
        contours, hierarchy
    """
    if cv2.__version__.startswith('4'):
        contours, hierarchy = cv2.findContours(*args, **kwargs)
    elif cv2.__version__.startswith('3'):
        _, contours, hierarchy = cv2.findContours(*args, **kwargs)
    else:
        raise AssertionError(
            'cv2 must be either version 3 or 4 to call this method')

    return contours, hierarchy


def load_class_desc(dataset='coco', logger=logging.getLogger()):
    """
    载入class_desc文件夹中的类别信息，txt文件的每一行代表一个类别
    :param dataset: str 'coco'
    :param logger
    :return: list ['cls1', 'cls2', ...]
    """
    desc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'class_desc')
    desc_names = []
    for f in os.listdir(desc_dir):
        if f.endswith('.txt'):
            desc_names.append(os.path.splitext(f)[0])
    # 如果类别描述文件存在，则返回所有类别名称，否则会报错
    cls_names = []
    if dataset in desc_names:
        with open(os.path.join(desc_dir, dataset + '.txt')) as f:
            for line in f.readlines():
                if len(line.strip()) > 0:
                    cls_names.append(line.strip().replace(' ', '_').lower())
    else:
        raise NameError('[spire]: {}.txt not exist in "class_desc"'.format(dataset))
    # 类别描述文件不能为空，否则会报错
    if len(cls_names) > 0:
        logger.info('loading {} class descriptions.'.format(len(cls_names)))
        return cls_names
    else:
        raise RuntimeError('[spire]: {}.txt is EMPTY'.format(dataset))


def load_class_trans(trans='visdrone_12_10', logger=logging.getLogger()):
    """
    载入class_desc/class_transfor文件夹中的类别转换信息，txt文件的每一行代表一组转换，如class1,class2
    转换后舍弃用'__'表示
    :param trans: str 'visdrone_12_10'
    :param logger
    :return: dict {'class1': 'class2', ...}
    """
    trans_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'class_desc', 'class_trans')
    trans_names = []
    for f in os.listdir(trans_dir):
        if f.endswith('.txt'):
            trans_names.append(os.path.splitext(f)[0])
    # 如果类别转换描述文件存在，则返回所有转换字典，否则会报错
    cls_dict = {}
    if trans in trans_names:
        with open(os.path.join(trans_dir, trans + '.txt')) as f:
            for line in f.readlines():
                if len(line.strip()) > 0:
                    pair = line.strip().split(',')
                    if len(pair) != 2:
                        raise RuntimeError('[spire]: line should be "class1,class2" in {}.txt'.format(trans))
                    cls_dict[pair[0].strip().replace(' ', '_').lower()] = pair[1].strip().replace(' ', '_').lower()
    else:
        raise NameError('[spire]: {}.txt not exist in "class_desc/class_trans"'.format(trans))
    # 转换类别描述文件不能为空，否则会报错
    if len(cls_dict) > 0:
        logger.info('loading {} class trans descriptions.'.format(len(cls_dict)))
        return cls_dict
    else:
        raise RuntimeError('[spire]: {}.txt is EMPTY'.format(trans))


class SpireAnno(object):
    """
    spire格式标注生成器类
    """
    def __init__(
        self,
        dataset='coco',
        class_trans=None,
        spire_dir='/tmp',
        max_det=100,
        logger=logging.getLogger()
    ):
        self.logger = logger
        self.spire_dir = spire_dir
        self.classes = load_class_desc(dataset, logger)
        self.class_id = {}
        self.id_class = {}
        if class_trans is not None:
            self.class_trans = load_class_trans(class_trans, logger)
            self.classes = list(self.class_trans.keys())
            id = 0
            for cls1, cls2 in self.class_trans.items():
                if cls2 != '__':
                    self.class_id[cls2] = id
                    self.id_class[id] = cls2
                    id += 1
        else:
            self.class_trans = None
            self.class_id = {}
            for id, cls in enumerate(self.classes):
                self.class_id[cls] = id
                self.id_class[id] = cls

        self.anno_dir = None
        self.anno_colors = self._create_colors(len(self.classes))
        self.num_classes = len(self.classes)
        self.max_det = max_det
        self.video_name = None
        self.video_frame_cnt = 1

        if not os.path.exists(self.spire_dir):
            os.makedirs(self.spire_dir)

    @staticmethod
    def _create_colors(length=1):
        import matplotlib.pyplot as plt
        cmap = plt.get_cmap('rainbow')
        colors = [cmap(i) for i in np.linspace(0, 1, length)]
        colors = [(int(rgba[2] * 255), int(rgba[1] * 255), int(rgba[0] * 255)) for rgba in colors]
        return colors

    def to_instances(self, spire_file_name):
        """
        将spire格式的json文件转换为Instances格式
        :param spire_file_name: (str) e.g. 'COCO_val2014_000000000139.jpg.json'
                                or (dict) {'file_name':'', 'height':...}
        :return: wedet.structures.instances
        """
        if isinstance(spire_file_name, dict):
            ann_dict = spire_file_name
        else:
            ann_dict = json.loads(open(spire_file_name, 'r').read())

        assert 'annos' in ann_dict.keys(), "'annos' should be in spire_annotation_dict.keys()"
        # assert 'annos' in ann_dict.keys() and len(ann_dict['annos']) > 0, "len(ann_dict['annos']) should be > 0"
        heigth, width = ann_dict['height'], ann_dict['width']

        import torch

        if len(ann_dict['annos']) == 0:
            bbox = Boxes(torch.zeros(0, 4))
        else:
            bbox = Boxes(torch.tensor([b['bbox'] for b in ann_dict['annos']]))

        keeps = None
        labels = []
        if len(ann_dict['annos']) > 0:
            keeps = []
            if self.class_trans is not None:
                for b in ann_dict['annos']:
                    b_cn = self.class_trans[b['category_name'].replace(' ', '_').lower()]
                    if b_cn == '__':  # 需要丢掉的类别
                        labels.append(-1)
                        keeps.append(0)
                    else:
                        labels.append(self.class_id[b_cn])
                        keeps.append(1)
                keeps = torch.tensor(keeps, dtype=torch.bool)
            else:
                # 将空格替换为下划线
                for b in ann_dict['annos']:
                    if b['category_name'] == "ignored-regions":
                        labels.append(-1)
                        keeps.append(0)
                    else:
                        labels.append(self.class_id[b['category_name'].replace(' ', '_').lower()])
                        keeps.append(1)
                keeps = torch.tensor(keeps, dtype=torch.bool)
        labels = torch.tensor(labels, dtype=torch.long)

        if len(ann_dict['annos']) > 0 and 'score' in ann_dict['annos'][0]:
            scores = torch.tensor([b['score'] for b in ann_dict['annos']])
            inst = Instances((heigth, width), boxes=bbox, labels=labels, scores=scores)
        else:
            inst = Instances((heigth, width), boxes=bbox, labels=labels)

        if keeps is not None:
            inst = inst[keeps]
        return inst

    def visualize_instances(
        self,
        image,
        instances,
        score_threshold=0.2,
        vis_gt=False,
        thickness=1,
        vis_label=True,
        vis_color=None,
        already_trans=True,
        output_spire_json=False,
        image_name=None,
    ):
        f"""
        将BoxList的检测结果显示在图像上
        :param image: (np.ndarray) 输入图像opencv读取
        :param instances: (List(List)) 检测结果: [[x1,y1,x2,y2,class_id,score], ...] & class_id: [0,1,...]
        :param score_threshold: (float) 得分过滤
        :param vis_gt: 没有scores得分，比如显示真值
        :param thickness: 窗口粗细
        :param vis_label: 是否显示标签
        :param vis_color: 显示颜色
        :param already_trans: 已经进行了类别转换
        :param output_spire_json: 输出spire格式json文件，用于可视化与评价
        :param image_name: 图像名称，输出spire格式json文件名称为 image_name.json
        :return:
        """
        nh, nw = image.shape[:2]  # instances.image_size
        # assert image.shape[0] == nh and image.shape[1] == nw, "Input image size not equal with Instances.image_size"

        import torch
        # reshape prediction (a BoxList) into the original image size
        if vis_gt:
            instances = [i.append(1.) for i in instances]

        annos = []
        if len(instances) > 0:
            #  sort by scores, and draw bbox
            instances = torch.tensor(instances)
            """
            scores = instances[:, -1]
            keep = torch.nonzero(scores > score_threshold).squeeze(1)
            if keep.numel() > 1:
                instances = instances[keep]
            """
            scores = instances[:, -1]
            _, idx = scores.sort(0, descending=True)
            if idx.numel() > 1:
                instances = instances[idx]

            # coco_eval.py/prepare_for_coco_detection
            scores = instances[:, -1].tolist()
            labels = instances[:, -2].int().tolist()
            bboxes = instances[:, :4].tolist()

            canvas = image.copy()
            coco_names = self.classes
            coco_colors = self.anno_colors
            for i, (bbox, score, label) in enumerate(zip(bboxes, scores, labels)):
                x1, y1, x2, y2 = bbox
                # label = label - 1  # -1 表示去掉背景类
                if already_trans and self.class_trans is not None and label < len(self.id_class):
                    color = coco_colors[label]
                    name = self.id_class[label]
                    caption = "#{} {} {:.3f}".format(label, name, score)
                elif label < len(coco_names):
                    color = coco_colors[label]
                    name = coco_names[label]
                    if self.class_trans is not None:
                        name = self.class_trans[name]
                        if name == '__':  # 需要丢掉的类别
                            continue
                    caption = "#{} {} {:.3f}".format(label, name, score)
                else:
                    color = (0, 255, 0)
                    caption = "#{}, s({:.3f})".format(label, score)
                    name = 'unknown'

                if vis_color is not None:
                    color = vis_color

                if output_spire_json:
                    anno = {}
                    TO_REMOVE = 1
                    x, y, w, h = x1, y1, x2 - x1 + TO_REMOVE, y2 - y1 + TO_REMOVE
                    anno['bbox'] = [float(x), float(y), float(w), float(h)]
                    anno['score'] = float(score)
                    anno['category_name'] = name
                    anno['area'] = w * h
                    annos.append(anno)

                cv2.rectangle(canvas, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness, cv2.LINE_AA)
                if vis_label:
                    # cv2.putText(canvas, caption, (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1,
                    #             cv2.LINE_AA)
                    cv2.putText(canvas, caption, (int(x1 + 5), int(y1 + 15)), cv2.FONT_HERSHEY_COMPLEX, 0.4, color, 1,
                                cv2.LINE_AA)
        else:
            canvas = image.copy()

        if output_spire_json:
            json_dict = dict()
            assert image_name is not None, "Should provide image_name when output_spire_json=True"
            json_dict['file_name'] = image_name
            json_dict['height'] = nh
            json_dict['width'] = nw
            json_dict['annos'] = annos

            anno_dir = os.path.join(self.spire_dir, 'annotations')
            if not os.path.exists(anno_dir):
                os.makedirs(anno_dir)

            anno_fn = os.path.join(anno_dir, image_name + '.json')
            f = open(anno_fn, 'w', encoding='utf-8')
            json.dump(json_dict, f)

        return canvas

    def _assert_classes(self, len_input):
        """
        防止输入类别不等于预定义数据集类别
        :param len_input: int
        :return:
        """
        assert len_input == len(self.classes), '[spire]: Input length ({}) != len(self.classes)'.format(len_input)

    def from_detectron2(
        self,
        result,
        image_name=None,
        image=None,
        confidence=0.01,
        input_gt=False,
        process_area=None,
        output_visdrone_format=False,
    ):
        """
        将maskrcnn-benchmark的结果转换为spire标注
        :param result: (Instances) |- pred_boxes (Boxes) [n, 4]
                                   |- scores (torch.Tensor) [n,]
                                   |- pred_classes (torch.Tensor) [n,]
        :param image_name (str)
        :param image (np.ndarray)
        :param confidence (float)
        :param input_gt (bool)
        :param process_area (None or list[image_w, image_h, start_x, start_y, process_width, process_height])
                只用来说明处理区域，不对结果产生影响
        :param output_visdrone_format (bool) 是否输出VisDrone官方格式txt文件，但只能用于VisDrone数据集
        :return:
        """
        import torch

        im_h, im_w = result.image_size
        if input_gt:
            result.set('scores', torch.ones(len(result)))

        bbox_np = result.get('pred_boxes').tensor.cpu().detach().numpy()
        scores_np = result.get('scores').cpu().detach().numpy()
        labels_np = result.get('pred_classes').cpu().detach().numpy()

        if image_name is None:
            if self.video_name is not None:
                image_name = self.video_name + "_{}.jpg".format(str(self.video_frame_cnt).zfill(8))
            else:
                image_name = "{}.jpg".format(str(self.video_frame_cnt).zfill(8))
            self.video_frame_cnt += 1
        else:
            image_name = os.path.basename(image_name)
        self.logger.debug("image_name: {}".format(image_name))

        if output_visdrone_format:
            visdrone_format_dir = os.path.join(self.spire_dir, 'visdrone_format')
            if not os.path.exists(visdrone_format_dir):
                os.makedirs(visdrone_format_dir)
            visdrone_txt_fn = os.path.join(visdrone_format_dir, os.path.splitext(image_name)[0] + '.txt')
            visdrone_txt_fo = open(visdrone_txt_fn, "w")

        annos = []
        for i in range(len(bbox_np)):
            bbox = bbox_np[i]
            score = scores_np[i]
            label = labels_np[i]  # - 1   # -1 表示去掉背景类

            class_ci = self.classes[label]
            if self.class_trans is not None:
                class_ci = self.class_trans[class_ci]
                if class_ci == '__':   # 需要丢掉的类别
                    continue

            anno = {}
            TO_REMOVE = 1
            x, y, w, h = bbox[0], bbox[1], bbox[2] - bbox[0] + TO_REMOVE, bbox[3] - bbox[1] + TO_REMOVE
            anno['bbox'] = [float(x), float(y), float(w), float(h)]
            anno['score'] = float(score)
            if anno['score'] < confidence:
                continue
            anno['category_name'] = class_ci
            anno['area'] = w * h
            annos.append(anno)

            if output_visdrone_format:
                visdrone_category_trans = {"pedestrian": 1, "people": 2, "bicycle": 3, "car": 4, "van": 5, "truck": 6,
                                           "tricycle": 7, "awning-tricycle": 8, "bus": 9, "motor": 10}
                visdrone_txt_fo.write("{},{},{},{},{},{},0,0\n".format(
                    x, y, w, h, score, visdrone_category_trans[class_ci]
                ))

        if output_visdrone_format:
            visdrone_txt_fo.close()

        json_dict = dict()
        json_dict['file_name'] = image_name
        json_dict['height'] = im_h
        json_dict['width'] = im_w
        json_dict['annos'] = annos
        if process_area is not None:
            json_dict['process_area'] = process_area[2:]
            # json_dict['height'] = process_area[1]
            # json_dict['width'] = process_area[0]

        anno_dir = os.path.join(self.spire_dir, 'annotations')
        if not os.path.exists(anno_dir):
            os.makedirs(anno_dir)
        if image is not None:
            assert image.shape[0] == im_h and image.shape[1] == im_w, "Image size not equal with Instances.image_size!"
            image_dir = os.path.join(self.spire_dir, 'scaled_images')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            cv2.imwrite(os.path.join(image_dir, image_name), image)

        self.anno_dir = anno_dir  # 保存anno_dir，用来合成测试json
        anno_fn = os.path.join(anno_dir, image_name + '.json')
        f = open(anno_fn, 'w', encoding='utf-8')
        json.dump(json_dict, f)

    def _generate_coco_json(self, anno_dir=None):
        """
        根据spire annotations生成coco评价格式的json，之后调用cocoapi进行评价
        :param anno_dir (str): 外部输入的anno_dir，默认使用self.anno_dir
        :return:
        """
        if anno_dir is not None:
            self.anno_dir = anno_dir
            if not (anno_dir.endswith('annotations') or anno_dir.endswith('detection-1')):
                self.anno_dir = os.path.join(anno_dir, 'annotations')

        coco_results = []
        for image_id, mapped_id in self.id_to_img_map.items():
            file_name = self.coco.imgs[mapped_id]['file_name'] + '.json'
            '''
            name = self.coco.imgs[mapped_id]['file_name']
            import shutil
            p1 = os.path.join('/home/jario/dataset/coco/val2014', name)
            p2 = os.path.join('/home/jario/dataset/coco/minival2014', name)
            shutil.copy(p1, p2)
            '''
            with open(os.path.join(self.anno_dir, file_name), 'r') as f:
                json_str = f.read()
                json_dict = json.loads(json_str)

            # boxlist = self.to_boxlist(json_dict)
            # boxlist = boxlist.convert('xywh')

            image_width = self.coco.imgs[mapped_id]["width"]
            image_height = self.coco.imgs[mapped_id]["height"]

            boxes, scores, labels = [], [], []
            '''
            for bi in range(len(boxlist)):
                boxes.append(boxlist.bbox[bi].tolist())
                scores.append(boxlist.extra_fields['scores'][bi].item())
                labels.append(boxlist.extra_fields['labels'][bi].item())
            '''
            for anno in json_dict['annos']:
                boxes.append(anno['bbox'])
                scores.append(anno['score'])
                labels.append(self.class_id[anno['category_name']] + 1)

            mapped_labels = [self.contiguous_category_id_to_json_id[i] for i in labels]

            coco_results.extend(
            [
                {
                    "image_id": mapped_id,
                    "category_id": mapped_labels[k],
                    "bbox": box,
                    "score": scores[k],
                }
                for k, box in enumerate(boxes)
            ])
        return coco_results

    def _eval_on_cocoapi(self, coco_gt, coco_results, json_result_file, iou_type="bbox"):
        """
        调用cocoapi进行实际评价
        :param coco_gt (cocoapi): COCO(coco_annotations)
        :param coco_results (dict): 自己生成的测试结果
        :param json_result_file (str): 将coco_results转换到json文件中
        :param iou_type (str): 评价类型['bbox', 'segm']
        :return:
        """
        with open(json_result_file, "w") as f:
            json.dump(coco_results, f)

        from pycocotools.coco import COCO
        from pycocotools.cocoeval import COCOeval

        coco_dt = coco_gt.loadRes(str(json_result_file)) if coco_results else COCO()

        # coco_dt = coco_gt.loadRes(coco_results)
        coco_eval = COCOeval(coco_gt, coco_dt, iou_type)
        coco_eval.evaluate()
        coco_eval.accumulate()
        coco_eval.summarize()
        return coco_eval

    def _cocoapi_init(self, ground_truth_json, anno_dir=None):
        from pycocotools.coco import COCO

        if anno_dir is not None:
            self.anno_dir = anno_dir
            if not (anno_dir.endswith('annotations') or anno_dir.endswith('detection-1')):
                self.anno_dir = os.path.join(anno_dir, 'annotations')

        self.coco = COCO(ground_truth_json)
        self.ids = list(self.coco.imgs.keys())
        # sort indices for reproducible results
        self.ids = sorted(self.ids)
        self.json_category_id_to_contiguous_id = {
            v: i + 1 for i, v in enumerate(self.coco.getCatIds())
        }
        self.contiguous_category_id_to_json_id = {
            v: k for k, v in self.json_category_id_to_contiguous_id.items()
        }
        self.id_to_img_map = {k: v for k, v in enumerate(self.ids)}

    def cocoapi_eval(self, ground_truth_json, anno_dir=None):
        """
        用cocoapi进行评价
        :param ground_truth_json (str): path to coco-format annotations, e.g. 'instances_minival2014.json'
        :param anno_dir (str): 外部输入的anno_dir，默认使用self.anno_dir
        :return:
        """
        self._cocoapi_init(ground_truth_json, anno_dir)
        coco_results_bbox = self._generate_coco_json(anno_dir)

        iou_type = 'bbox'
        return self._eval_on_cocoapi(
            self.coco,
            coco_results_bbox,
            os.path.join(self.spire_dir, iou_type + '.json'),
            iou_type,
        )
