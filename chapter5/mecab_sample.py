import MeCab

tagger = MeCab.Tagger()
tagger.parse('')#これは.parseToNode()の不具合を回避するためのハック

#.parseToNode()で最初の形態素を表すNodeオブジェクトを取得する
node = tagger.parseToNode('すもももももももものうち')

while node:
    #.surfaceは形態素の文字列、.feartureは品詞などを含む文字列をそれぞれ取り出す
    print(node.surface, node.feature)
    node = node.next #次のnodeの取得