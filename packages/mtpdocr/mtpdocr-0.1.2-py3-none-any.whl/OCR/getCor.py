import argparse
import json
import os
import re

from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory

project_path = os.path.dirname(os.path.abspath(__file__))
os.system("export CUDA_VISIBLE_DEVICES=0,1,2,3")


def get_word_coordinates(word_to_search: str, img_path: str, lang: str, output_path, multiple: bool,
                         print_all: bool, expect_credibility: float) -> list:
    """获取目标文字坐标"""
    if lang is None:
        lang = "ch"
    result = get_ocr_result(word_to_search, img_path, lang, output_path)
    rec_result = {}
    rec_list = []
    max_credibility_word_index = -1
    max_credibility = -1.0
    print("Start printing recganized words")
    for line in result:
        all_rec_result = {}
        rec_info = {}
        coordinate = []  # 存放匹配字符串的坐标
        x = y = 0
        word = line[1][0]  # 识别出来的文字
        for point in line[0]:
            x = int(point[0]) + x
            y = int(point[1]) + y
        credibility = line[1][1]  # 识别出来的文字可信度
        if expect_credibility is not None and float(credibility) < expect_credibility:
            continue
        else:
            x_avg = x / 4
            y_avg = y / 4
            coordinate.append(x_avg)
            coordinate.append(y_avg)
            all_rec_result[word] = coordinate
            print(json.dumps(all_rec_result))
            if re.match(word_to_search, word):
                rec_info["word"] = word
                rec_info["cordinate"] = coordinate
                rec_info["credibility"] = str(credibility)
                rec_list.append(rec_info)
                if float(credibility) > max_credibility:
                    max_credibility = credibility
                    max_credibility_word_index = len(rec_list) - 1
    print("Stop printing recognized words")
    list_length = len(rec_list)
    if list_length > 0:
        if not multiple:
            rec_info = rec_list[max_credibility_word_index]
            rec_list.clear()
            rec_list.append(rec_info)
    rec_result["result"] = rec_list
    json_result = json.dumps(rec_result)  # 转字符串中的单引号-->双引号
    print(json_result)


def get_ocr_result(word: str, img_path: str, lang: str, output_path: str) -> list:
    """获取识别结果"""
    if word is None:
        return None
    ocr = PaddleOCR(use_gpu=False, use_angle_cls=True, lang=lang)  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    if output_path is not None:
        draw_result(img_path, result, output_path)
    return result


def draw_result(img_path: str, result: str, output_path: str):
    """绘制结果图"""
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path=project_path + '/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    output_img_name = output_path + "result." + img_path.split(".")[1]
    im_show.save(output_img_name)


def getCor():
    """
    打印目标文字坐标
    :return:
    """
    parser = argparse.ArgumentParser(usage="mtPaddleOcr --word $word --imgpath $imgpath --output $output --fuzzy "
                                           "--multiple --printall",
                                     description="图片文字坐标返回（--word、--imgpath必填）")
    parser.add_argument('--word', required=True, type=str, help="要查找的文字")
    parser.add_argument('--imgpath', required=True, type=str, help="要识别的图片路径")
    parser.add_argument('--lang', choices=['ch', 'en'], help="ch:中文 en：英文")
    parser.add_argument('--outputpath', type=str, default=None, help="结果绘制成图片后的保存地址")
    parser.add_argument('--credibility', type=float, default=None, help="可信度阈值")
    parser.add_argument('--fuzzy', action="store_true", default=False, help="是否模糊匹配，默认精准匹配")
    parser.add_argument('--multiple', action="store_true", help="允许匹配多个结果，默认只返回可信值最高的一个")
    parser.add_argument('--printall', action="store_true", help="是否打印其他识别结果，默认不打印")

    args = parser.parse_args()

    is_fuzzy = args.fuzzy
    word = args.word
    img_path = args.imgpath
    language = args.lang
    multiple = args.multiple
    output_path = args.outputpath
    print_all = args.printall
    expect_credibility = args.credibility
    print(is_fuzzy)

    if output_path is not None:
        if not str(output_path).endswith("/"):
            output_path = output_path + "/"

    if is_fuzzy:
        deal_word = ".*(?i)"
        for ch in word:
            if ch in ["I", "1", "l"]:
                temp = '["I", "1", "l"]{1}'
            elif ch in ["i", "j"]:
                temp = '["i", "j"]{1}'
            elif ch in ["o", "0", "O"]:
                temp = '["o", "0", "O"]{1}'
            elif ch in ["q", "g"]:
                temp = '["q", "g"]{1}'
            else:
                temp = ch
            deal_word = deal_word + temp
        deal_word = deal_word + ".*"
    else:
        deal_word = word
    get_word_coordinates(deal_word, img_path, language, output_path, multiple, print_all, expect_credibility)


if __name__ == '__main__':
    getCor()
