import sys
import logging

import cv2

logging.basicConfig(level=logging.INFO) #INFOレベル以上のログを出力する

try:
    input_path = sys.argv[1]
    output_path = sys.argv[2]
except IndexError:
    print('Usage: python detect_faces.py INPUT_PATH OUTPUT_PATH', file=sys.stderr)
    exit(1)

#特徴良ファイルのパスを指定して、分類期オブジェクトを作成する
#ここではOpenCVに付属している学習済みの顔の特徴良ファイルを使用する
#cv2.data.headcascadeはデータディレクトリのパス。公式のPythonバインディングには存在しないので注意
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

image = cv2.imread(input_path) #画像ファイルを読み込む
if image is None:
    #画像ファイルが存在しない場合はエラーを表示して終了する
    logging.error(f'Image "{input_path}" not found.')
    exit(1)

#顔を検出する、特徴量ファイルが存在しない場合はこの時点でエラーになるので注意
faces = classifier.detectMultiScale(image)
logging.info(f'Found {len(faces)} faces.') #検出できた顔の数を出力

#検出された顔のリストについて反復処理し、顔を囲む白い四角形を描画する
#x, y, w, h はそれぞれ検出された顔のx座標, y座標, 幅, 高さを表す
for x, y, w, h in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), color=(255, 255, 255), thickness=2)
cv2.imwrite(output_path, image)