import pytest
import re
from service.word_tokenizer import WordFrequencyAnalyzer, WordAnalyzer


@pytest.mark.parametrize(('word', 'sentence'), [
    ('遅れ', '【07月11日 00時25分現在】関西本線での遅れの影響により、一部の列車に遅れが発生しております。 #JR東海運行情報 #中央線'),
    ('運休', 'おはようございます太陽の光週末は大雨の影響により列車の遅延並びに運休で、ご利用のお客様には大変ご迷惑をおかけ致しました。'),
    ('運転見合わせ', '7月11日0時5分現在： 大雨の影響により、今後は運休や運転見合わせが見込まれるため、以下の対象となるきっぷについては、払戻し・有効期間の変更を無手数料で行いますので、お近くのJRの駅にきっぷをお持ちください。また、インターネット予約の場合は、'),
    ('取り止め', '7月11日0時0分現在： 木次線#では大雨に伴い、宍道駅〜木次駅間では、本日（7月11日）は終日運転を取り止めます。なお、代行輸送を行います。※列車と代行輸送は接続しません。 #JR西日本 #木次線'),
    ('取りやめ', '7月11日0時0分現在： 木次線では大雨に伴い、宍道駅〜木次駅間では、本日（7月11日）は終日運転を取りやめます。なお、代行輸送を行います。※列車と代行輸送は接続しません。 #JR西日本 #木次線'),
    ('振替輸送実施中', '7:06 【運行情報】大雨の影響で神奈川新町駅〜上大岡駅間の上下線の運転を見合わせ。\n次の路線にて振替輸送実施中です。\nＪＲ線、東急線、相鉄線、横浜市営地下鉄線、りんかい線、東京モノレール、都営地下鉄... #京急 #keikyu'),

    ('避難指示', '松江市で避難指示\n松江市は、大雨で浸水の被害が発生するおそれがあるとして、大橋川南側の橋南地区の3万4173世帯7万1490人に、#避難指示 を出しました。\n5段階の警戒レベルのうち警戒レベル4の情報で、危険な場所から全員避難するよう呼びかけています。'),
    ('緊急安全確保', '【速報 JUST IN 】鹿児島 湧水町 全域に「緊急安全確保」 命を守る行動を #nhk_news'),
    ('氾濫危険水位', '【速報 JUST IN 】鹿児島 姶良 別府川 氾濫危険水位に 蒲生町の観測所 #nhk_news'),
    ('通行止め', '【大雨影響】高速道路の通行止めの状況（17時現在です）'),
    ('高齢者等避難', '松江 島根地区と美保関地区に高齢者等避難の情報 #nhk_news'),
    ('避難指示', '広島 鳥取 兵庫 【避難指示】\n危険な場所から避難を\n土砂災害の危険性高まる'),
    ('緊急安全確保', '緊急安全確保 命を守る行動を！\n広島 三原市新たな地域を追加\n広島県三原市は、天井川の水があふれたとして沼田東地区に加え午前9時40分新たに明神5丁目、そして土砂崩れが起きた小泉地区にも「緊急安全確保」の情報を出しました。'),

    # ('東京都', '東京都全域に緊急安全確保'),
])

def test_can_token(sentence, word) -> bool:
    analyzer = WordFrequencyAnalyzer(WordFrequencyAnalyzer.TRAFFIC_CHAR_FILTER, WordFrequencyAnalyzer.TRAFFIC_USER_DIC)
    tokens = analyzer.get_tokens(sentence)
    assert word in [t[0] for t in tokens]

def test_word_frequency_analyzer() -> bool:
    analyzer = WordFrequencyAnalyzer(WordFrequencyAnalyzer.TRAFFIC_CHAR_FILTER, WordFrequencyAnalyzer.TRAFFIC_USER_DIC)
    tokens = analyzer.get_tokens('松江市で避難指示\n松江市は、大雨で浸水の被害が発生するおそれがあるとして、大橋川南側の橋南地区の3万4173世帯7万1490人に、#避難指示 を出しました。\n5段階の警戒レベルのうち警戒レベル4の情報で、危険な場所から全員避難するよう呼びかけています。')
    words = [t[0] for t in tokens]
    assert '松江市' in words
    assert '避難指示' in words

def test_word_analyzer() -> bool:
    analyzer = WordAnalyzer(WordFrequencyAnalyzer.TRAFFIC_CHAR_FILTER, WordFrequencyAnalyzer.TRAFFIC_USER_DIC)

    tokens = analyzer.get_tokens('緊急安全確保 命を守る行動を！\n広島 三原市新たな地域を追加\n広島県三原市は、天井川の水があふれたとして沼田東地区に加え午前9時40分新たに明神5丁目、そして土砂崩れが起きた小泉地区にも「緊急安全確保」の情報を出しました。')
    words = [t.base_form for t in tokens]
    assert '広島' in words
    assert '三原' in words
    assert '緊急安全確保' in words


    tokens = analyzer.get_tokens('山形県によりますと、午前9時20分ごろに、新庄市を流れる指首野川の堀端観測所で、氾濫の危険性が非常に高い「氾濫危険水位」を超えました。\n山形県は川に近づかないよう厳重な警戒を呼びかけています。')
    words = [t.base_form for t in tokens]
    assert '山形' in words
    assert '新庄' in words
    assert '氾濫危険水位' in words
