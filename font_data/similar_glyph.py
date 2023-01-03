from pathlib import Path

sim_glyph_dict = {
    str(0x00b7):''
}
print(sim_glyph_dict.keys())
# katakana middle dot 0xff65
# middle dot 0x00b7
# 아래 아 0x119E
# 아래 아 0x318d

inf_log = [
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63744.jpg:('豈', 0.9667600393295288)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63745.jpg:('更', 0.9708418846130371)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63746.jpg:('車', 0.9982892870903015)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63747.jpg:('賈', 0.9965444207191467)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63748.jpg:('滑', 0.9991723299026489)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63749.jpg:('串', 0.9979343414306641)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63750.jpg:('句', 0.9694108963012695)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63751.jpg:('龜', 0.9995617270469666)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63752.jpg:('龜', 0.9995617270469666)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63753.jpg:('契', 0.9993939399719238)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63754.jpg:('金', 0.9808732867240906)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63755.jpg:('喇', 0.9957778453826904)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63756.jpg:('奈', 0.7389212846755981)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63757.jpg:('懶', 0.9992188215255737)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63758.jpg:('癩', 0.9995114803314209)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63759.jpg:('羅', 0.9844611287117004)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63760.jpg:('蘿', 0.9449524283409119)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63761.jpg:('螺', 0.999901533126831)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63762.jpg:('裸', 0.9948427081108093)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63763.jpg:('邏', 0.9943206310272217)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63764.jpg:('樂', 0.986677885055542)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63765.jpg:('洛', 0.9905701875686646)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63766.jpg:('烙', 0.9942830204963684)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63767.jpg:('珞', 0.9960535764694214)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63768.jpg:('落', 0.9998670816421509)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63769.jpg:('酪', 0.9075369238853455)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63770.jpg:('駱', 0.9897797703742981)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63771.jpg:('亂', 0.998573899269104)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63772.jpg:('卯', 0.703230619430542)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63773.jpg:('欄', 0.9885028004646301)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63774.jpg:('爛', 0.9973668456077576)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63775.jpg:('蘭', 0.9999271631240845)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63776.jpg:('鸞', 0.9961064457893372)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63777.jpg:('嵐', 0.9997556805610657)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63778.jpg:('濫', 0.9996355772018433)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63779.jpg:('藍', 0.9983206391334534)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63780.jpg:('襤', 0.9997572302818298)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63781.jpg:('拉', 0.9932683110237122)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63782.jpg:('臘', 0.9676330089569092)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63783.jpg:('蠟', 0.9950778484344482)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63784.jpg:('廁', 0.785591721534729)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63785.jpg:('朗', 0.9975927472114563)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63786.jpg:('浪', 0.9997684359550476)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63787.jpg:('狼', 0.9995948672294617)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63788.jpg:('郞', 0.9997121691703796)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63789.jpg:('來', 0.9987891316413879)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63790.jpg:('冷', 0.9065390229225159)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63791.jpg:('勞', 0.9979833364486694)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63792.jpg:('擄', 0.9987046718597412)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63793.jpg:('櫓', 0.9997482895851135)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63794.jpg:('爐', 0.9767716526985168)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63795.jpg:('盧', 0.9744834899902344)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63796.jpg:('老', 0.9992916584014893)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63797.jpg:('蘆', 0.9906448125839233)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63798.jpg:('虜', 0.9957578778266907)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63799.jpg:('路', 0.9966083765029907)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63800.jpg:('露', 0.9939767122268677)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63801.jpg:('魯', 0.9974530339241028)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63802.jpg:('鷺', 0.9699934124946594)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63803.jpg:('碌', 0.9998281002044678)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63804.jpg:('祿', 0.9927524328231812)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63805.jpg:('綠', 0.7525457739830017)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63806.jpg:('菉', 0.9991948008537292)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63807.jpg:('錄', 0.9998990297317505)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63808.jpg:('鹿', 0.9458691477775574)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63809.jpg:('論', 0.999908447265625)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63810.jpg:('壟', 0.992561399936676)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63811.jpg:('弄', 0.9990589022636414)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63812.jpg:('籠', 0.9992365837097168)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63813.jpg:('聾', 0.9449405670166016)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63814.jpg:('牢', 0.9917815327644348)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63815.jpg:('磊', 0.9989709854125977)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63816.jpg:('賂', 0.9915488958358765)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63817.jpg:('雷', 0.9568741917610168)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63818.jpg:('壘', 0.8601754307746887)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63819.jpg:('屢', 0.9994148015975952)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63820.jpg:('樓', 0.9950725436210632)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63821.jpg:('淚', 0.9986646175384521)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63822.jpg:('漏', 0.9982238411903381)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63823.jpg:('累', 0.9996966123580933)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63824.jpg:('縷', 0.9964757561683655)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63825.jpg:('陋', 0.9972136616706848)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63826.jpg:('勒', 0.9996885061264038)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63827.jpg:('肋', 0.9823247194290161)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63828.jpg:('凜', 0.6785510778427124)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63829.jpg:('凌', 0.998058021068573)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63830.jpg:('稜', 0.999957799911499)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63831.jpg:('綾', 0.9840282797813416)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63832.jpg:('菱', 0.9646074175834656)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63833.jpg:('陵', 0.9960011839866638)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63834.jpg:('讀', 0.9994255304336548)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63835.jpg:('拏', 0.9996869564056396)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63836.jpg:('樂', 0.9884687066078186)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63837.jpg:('諾', 0.9968486428260803)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63838.jpg:('丹', 0.9950586557388306)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63839.jpg:('寧', 0.9947094917297363)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63840.jpg:('怒', 0.9799812436103821)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63841.jpg:('率', 0.9974693059921265)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63842.jpg:('異', 0.9991620779037476)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63843.jpg:('北', 0.9995836615562439)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63844.jpg:('磻', 0.9852758646011353)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63845.jpg:('便', 0.9970765113830566)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63846.jpg:('復', 0.9988898634910583)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63847.jpg:('不', 0.9979076385498047)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63848.jpg:('泌', 0.9868453741073608)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63849.jpg:('數', 0.9969797134399414)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63850.jpg:('索', 0.8419669270515442)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63851.jpg:('參', 0.9487302899360657)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63852.jpg:('塞', 0.9911171197891235)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63853.jpg:('省', 0.7995791435241699)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63854.jpg:('葉', 0.9999014139175415)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63855.jpg:('說', 0.9777286648750305)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63856.jpg:('殺', 0.9978681802749634)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63857.jpg:('辰', 0.9951902627944946)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63858.jpg:('沈', 0.9978556036949158)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63859.jpg:('拾', 0.9924059510231018)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63860.jpg:('若', 0.9931134581565857)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63861.jpg:('掠', 0.999371349811554)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63862.jpg:('略', 0.9006808996200562)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63863.jpg:('亮', 0.9992291927337646)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63864.jpg:('雨', 0.5415733456611633)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63865.jpg:('凉', 0.7903677225112915)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63866.jpg:('梁', 0.9964913725852966)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63867.jpg:('糧', 0.9986945986747742)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63868.jpg:('良', 0.9989506006240845)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63869.jpg:('諒', 0.999840497970581)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63870.jpg:('量', 0.9937866926193237)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63871.jpg:('勵', 0.998878538608551)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63872.jpg:('呂', 0.9916412830352783)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63873.jpg:('女', 0.8952253460884094)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63874.jpg:('廬', 0.9634897112846375)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63875.jpg:('旅', 0.9981151819229126)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63876.jpg:('濾', 0.9843347668647766)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63877.jpg:('礪', 0.9981156587600708)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63878.jpg:('閭', 0.3443313241004944)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63879.jpg:('驪', 0.9942610263824463)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63880.jpg:('麗', 0.9882405996322632)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63881.jpg:('黎', 0.9976525902748108)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63882.jpg:('力', 0.8964128494262695)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63883.jpg:('曆', 0.9991704225540161)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63884.jpg:('歷', 0.9584366083145142)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63885.jpg:('轢', 0.9884536862373352)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63886.jpg:('年', 0.9864237904548645)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63887.jpg:('憐', 0.9998476505279541)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63888.jpg:('戀', 0.9999449253082275)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63889.jpg:('撚', 0.9782246351242065)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63890.jpg:('漣', 0.9950141310691833)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63891.jpg:('煉', 0.9990167617797852)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63892.jpg:('璉', 0.9903014898300171)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63893.jpg:('秊', 0.977269172668457)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63894.jpg:('練', 0.9984952211380005)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63895.jpg:('聯', 0.9982730150222778)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63896.jpg:('輦', 0.9997552037239075)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63897.jpg:('蓮', 0.9973790645599365)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63898.jpg:('連', 0.9432162642478943)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63899.jpg:('鍊', 0.7244628071784973)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63900.jpg:('列', 0.9435490965843201)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63901.jpg:('劣', 0.9990612864494324)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63902.jpg:('咽', 0.9807177186012268)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63903.jpg:('烈', 0.9676525592803955)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63904.jpg:('裂', 0.9675941467285156)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63905.jpg:('說', 0.991239607334137)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63906.jpg:('廉', 0.999354898929596)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63907.jpg:('念', 0.9992972612380981)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63908.jpg:('捻', 0.9979239702224731)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63909.jpg:('殮', 0.9928629994392395)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63910.jpg:('簾', 0.9983144998550415)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63911.jpg:('獵', 0.9997816681861877)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63912.jpg:('令', 0.9902368187904358)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63913.jpg:('囹', 0.9931063055992126)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63914.jpg:('寧', 0.9882786273956299)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63915.jpg:('嶺', 0.9995648264884949)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63916.jpg:('怜', 0.9361358880996704)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63917.jpg:('玲', 0.9996622800827026)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63918.jpg:('瑩', 0.9847463369369507)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63919.jpg:('羚', 0.9511760473251343)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63920.jpg:('聆', 0.9961122870445251)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63921.jpg:('鈴', 0.9900875687599182)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63922.jpg:('零', 0.9618921875953674)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63923.jpg:('靈', 0.7774072289466858)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63924.jpg:('領', 0.9959738850593567)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63925.jpg:('例', 0.9922448992729187)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63926.jpg:('禮', 0.9978824257850647)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63927.jpg:('醴', 0.9962407350540161)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63928.jpg:('隸', 0.49963828921318054)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63929.jpg:('惡', 0.9997984766960144)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63930.jpg:('了', 0.9957684278488159)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63931.jpg:('僚', 0.9997243285179138)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63932.jpg:('寮', 0.9993451237678528)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63933.jpg:('尿', 0.9965376853942871)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63934.jpg:('料', 0.9951449036598206)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63935.jpg:('樂', 0.99033522605896)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63936.jpg:('燎', 0.9995808005332947)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63937.jpg:('療', 0.9991173148155212)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63938.jpg:('蓼', 0.9837125539779663)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63939.jpg:('遼', 0.9855967164039612)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63940.jpg:('龍', 0.9998540878295898)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63941.jpg:('暈', 0.8871971368789673)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63942.jpg:('阮', 0.9978019595146179)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63943.jpg:('劉', 0.998016357421875)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63944.jpg:('杻', 0.9968762397766113)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63945.jpg:('柳', 0.9976189732551575)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63946.jpg:('流', 0.9996297359466553)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63947.jpg:('溜', 0.9937071204185486)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63948.jpg:('琉', 0.9885470867156982)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63949.jpg:('留', 0.9981544613838196)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63950.jpg:('硫', 0.9942499399185181)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63951.jpg:('紐', 0.996117115020752)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63952.jpg:('類', 0.9920756816864014)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63953.jpg:('六', 0.9949230551719666)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63954.jpg:('戮', 0.9984549283981323)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63955.jpg:('陸', 0.9996371269226074)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63956.jpg:('倫', 0.9991657733917236)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63957.jpg:('崙', 0.9992063641548157)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63958.jpg:('淪', 0.9879947304725647)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63959.jpg:('輪', 0.9959239959716797)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63960.jpg:('律', 0.9988742470741272)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63961.jpg:('慄', 0.9997504353523254)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63962.jpg:('栗', 0.9956745505332947)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63963.jpg:('率', 0.9983731508255005)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63964.jpg:('隆', 0.9991194605827332)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63965.jpg:('利', 0.9952268600463867)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63966.jpg:('吏', 0.9990359544754028)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63967.jpg:('履', 0.9968848824501038)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63968.jpg:('易', 0.9986024498939514)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63969.jpg:('李', 0.998680055141449)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63970.jpg:('梨', 0.9956385493278503)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63971.jpg:('泥', 0.998084545135498)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63972.jpg:('理', 0.9997250437736511)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63973.jpg:('痢', 0.9997492432594299)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63974.jpg:('罹', 0.9966689944267273)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63975.jpg:('裏', 0.994690477848053)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63976.jpg:('裡', 0.996154248714447)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63977.jpg:('里', 0.9971569776535034)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63978.jpg:('離', 0.9966515898704529)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63979.jpg:('匿', 0.9976502060890198)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63980.jpg:('溺', 0.9866341352462769)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63981.jpg:('吝', 0.995526134967804)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63982.jpg:('燐', 0.9987871050834656)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63983.jpg:('璘', 0.9985364675521851)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63984.jpg:('藺', 0.9994365572929382)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63985.jpg:('隣', 0.9995061159133911)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63986.jpg:('鱗', 0.9959908127784729)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63987.jpg:('麟', 0.9835870862007141)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63988.jpg:('林', 0.9920985698699951)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63989.jpg:('淋', 0.9994200468063354)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63990.jpg:('臨', 0.9999758005142212)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63991.jpg:('立', 0.9697141051292419)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63992.jpg:('笠', 0.9996613264083862)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63993.jpg:('粒', 0.9993667006492615)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63994.jpg:('狀', 0.984650731086731)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63995.jpg:('炙', 0.996986448764801)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63996.jpg:('識', 0.9819819331169128)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63997.jpg:('什', 0.9575940370559692)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63998.jpg:('茶', 0.6912945508956909)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/63999.jpg:('刺', 0.9514049887657166)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64000.jpg:('切', 0.9869717955589294)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64001.jpg:('度', 0.8604315519332886)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64002.jpg:('拓', 0.9901102185249329)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64003.jpg:('糖', 0.9813622832298279)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64004.jpg:('宅', 0.9869083166122437)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64005.jpg:('洞', 0.9917830228805542)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64006.jpg:('暴', 0.9996274709701538)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64007.jpg:('輻', 0.9998635053634644)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64008.jpg:('行', 0.9950047135353088)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64009.jpg:('降', 0.9861838221549988)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64010.jpg:('見', 0.9962122440338135)",
"/home/sayi/workspace/OCR/TrainDataPreprocess/font_data/kor_rec/trainDotum_24_data/64011.jpg:('廓', 0.9966999888420105)",
]
# need_check = [

cjkcomp2unif_dict = {
    0xf900: 0x8c48,
    0xf901: 0x66f4,
    0xf902: 0x8eca,
    0xf903: 0x8cc8,
    0xf904: 0x6ed1,
    0xf905: 0x4e32,
    0xf906: 0x53e5,
    0xf907: 0x9f9c,
    0xf908: 0x9f9c,
    0xf909: 0x5951,
    0xf90a: 0x91d1,
    0xf90b: 0x5587,
    0xf90c: 0x5948,
    0xf90d: 0x61f6,
    0xf90e: 0x7669,
    0xf90f: 0x7f85,
    0xf910: 0x863f,
    0xf911: 0x87ba,
    0xf912: 0x88f8,
    0xf913: 0x908f,
    0xf914: 0x6a02,
    0xf915: 0x6d1b,
    0xf916: 0x70d9,
    0xf917: 0x73de,
    0xf918: 0x843d,
    0xf919: 0x916a,
    0xf91a: 0x99f1,
    0xf91b: 0x4e82,
    0xf91c: 0x5375,
    0xf91d: 0x6b04,
    0xf91e: 0x721b,
    0xf91f: 0x862d,
    0xf920: 0x9e1e,
    0xf921: 0x5d50,
    0xf922: 0x6feb,
    0xf923: 0x85cd,
    0xf924: 0x8964,
    0xf925: 0x62c9,
    0xf926: 0x81d8,
    0xf927: 0x881f,
    0xf928: 0x5eca,
    0xf929: 0x6717,
    0xf92a: 0x6d6a,
    0xf92b: 0x72fc,
    0xf92c: 0x90de,
    0xf92d: 0x4f86,
    0xf92e: 0x51b7,
    0xf92f: 0x52de,
    0xf930: 0x64c4,
    0xf931: 0x6ad3,
    0xf932: 0x7210,
    0xf933: 0x76e7,
    0xf934: 0x8001,
    0xf935: 0x8606,
    0xf936: 0x865c,
    0xf937: 0x8def,
    0xf938: 0x9732,
    0xf939: 0x9b6f,
    0xf93a: 0x9dfa,
    0xf93b: 0x788c,
    0xf93c: 0x797f,
    0xf93d: 0x7da0,
    0xf93e: 0x83c9,
    0xf93f: 0x9304,
    0xf940: 0x9e7f,
    0xf941: 0x8ad6,
    0xf942: 0x58df,
    0xf943: 0x5f04,
    0xf944: 0x7c60,
    0xf945: 0x807e,
    0xf946: 0x7262,
    0xf947: 0x78ca,
    0xf948: 0x8cc2,
    0xf949: 0x96f7,
    0xf94a: 0x58d8,
    0xf94b: 0x5c62,
    0xf94c: 0x6a13,
    0xf94d: 0x6dda,
    0xf94e: 0x6f0f,
    0xf94f: 0x7d2f,
    0xf950: 0x7e37,
    0xf951: 0x964b,
    0xf952: 0x52d2,
    0xf953: 0x808b,
    0xf954: 0x51dc,
    0xf955: 0x51cc,
    0xf956: 0x7a1c,
    0xf957: 0x7dbe,
    0xf958: 0x83f1,
    0xf959: 0x9675,
    0xf95a: 0x8b80,
    0xf95b: 0x62cf,
    0xf95c: 0x6a02,
    0xf95d: 0x8afe,
    0xf95e: 0x4e39,
    0xf95f: 0x5be7,
    0xf960: 0x6012,
    0xf961: 0x7387,
    0xf962: 0x7570,
    0xf963: 0x5317,
    0xf964: 0x78fb,
    0xf965: 0x4fbf,
    0xf966: 0x5fa9,
    0xf967: 0x4e0d,
    0xf968: 0x6ccc,
    0xf969: 0x6578,
    0xf96a: 0x7d22,
    0xf96b: 0x53c3,
    0xf96c: 0x585e,
    0xf96d: 0x7701,
    0xf96e: 0x8449,
    0xf96f: 0x8aaa,
    0xf970: 0x6bba,
    0xf971: 0x8fb0,
    0xf972: 0x6c88,
    0xf973: 0x62fe,
    0xf974: 0x82e5,
    0xf975: 0x63a0,
    0xf976: 0x7565,
    0xf977: 0x4eae,
    0xf978: 0x5169,
    0xf979: 0x51c9,
    0xf97a: 0x6881,
    0xf97b: 0x7ce7,
    0xf97c: 0x826f,
    0xf97d: 0x8ad2,
    0xf97e: 0x91cf,
    0xf97f: 0x52f5,
    0xf980: 0x5442,
    0xf981: 0x5973,
    0xf982: 0x5eec,
    0xf983: 0x65c5,
    0xf984: 0x6ffe,
    0xf985: 0x792a,
    0xf986: 0x95ad,
    0xf987: 0x9a6a,
    0xf988: 0x9e97,
    0xf989: 0x9ece,
    0xf98a: 0x529b,
    0xf98b: 0x66c6,
    0xf98c: 0x6b77,
    0xf98d: 0x8f62,
    0xf98e: 0x5e74,
    0xf98f: 0x6190,
    0xf990: 0x6200,
    0xf991: 0x649a,
    0xf992: 0x6f23,
    0xf993: 0x7149,
    0xf994: 0x7489,
    0xf995: 0x79ca,
    0xf996: 0x7df4,
    0xf997: 0x806f,
    0xf998: 0x8f26,
    0xf999: 0x84ee,
    0xf99a: 0x9023,
    0xf99b: 0x934a,
    0xf99c: 0x5217,
    0xf99d: 0x52a3,
    0xf99e: 0x54bd,
    0xf99f: 0x70c8,
    0xf9a0: 0x88c2,
    0xf9a1: 0x8aaa,
    0xf9a2: 0x5ec9,
    0xf9a3: 0x5ff5,
    0xf9a4: 0x637b,
    0xf9a5: 0x6bae,
    0xf9a6: 0x7c3e,
    0xf9a7: 0x7375,
    0xf9a8: 0x4ee4,
    0xf9a9: 0x56f9,
    0xf9aa: 0x5be7,
    0xf9ab: 0x5dba,
    0xf9ac: 0x601c,
    0xf9ad: 0x73b2,
    0xf9ae: 0x7469,
    0xf9af: 0x7f9a,
    0xf9b0: 0x8046,
    0xf9b1: 0x9234,
    0xf9b2: 0x96f6,
    0xf9b3: 0x9748,
    0xf9b4: 0x9818,
    0xf9b5: 0x4f8b,
    0xf9b6: 0x79ae,
    0xf9b7: 0x91b4,
    0xf9b8: 0x96b7,
    0xf9b9: 0x60e1,
    0xf9ba: 0x4e86,
    0xf9bb: 0x50da,
    0xf9bc: 0x5bee,
    0xf9bd: 0x5c3f,
    0xf9be: 0x6599,
    0xf9bf: 0x6a02,
    0xf9c0: 0x71ce,
    0xf9c1: 0x7642,
    0xf9c2: 0x84fc,
    0xf9c3: 0x907c,
    0xf9c4: 0x9f8d,
    0xf9c5: 0x6688,
    0xf9c6: 0x962e,
    0xf9c7: 0x5289,
    0xf9c8: 0x677b,
    0xf9c9: 0x67f3,
    0xf9ca: 0x6d41,
    0xf9cb: 0x6e9c,
    0xf9cc: 0x7409,
    0xf9cd: 0x7559,
    0xf9ce: 0x786b,
    0xf9cf: 0x7d10,
    0xf9d0: 0x985e,
    0xf9d1: 0x516d,
    0xf9d2: 0x622e,
    0xf9d3: 0x9678,
    0xf9d4: 0x502b,
    0xf9d5: 0x5d19,
    0xf9d6: 0x6dea,
    0xf9d7: 0x8f2a,
    0xf9d8: 0x5f8b,
    0xf9d9: 0x6144,
    0xf9da: 0x6817,
    0xf9db: 0x7387,
    0xf9dc: 0x9686,
    0xf9dd: 0x5229,
    0xf9de: 0x540f,
    0xf9df: 0x5c65,
    0xf9e0: 0x6613,
    0xf9e1: 0x674e,
    0xf9e2: 0x68a8,
    0xf9e3: 0x6ce5,
    0xf9e4: 0x7406,
    0xf9e5: 0x75e2,
    0xf9e6: 0x7f79,
    0xf9e7: 0x88cf,
    0xf9e8: 0x88e1,
    0xf9e9: 0x91cc,
    0xf9ea: 0x96e2,
    0xf9eb: 0x533f,
    0xf9ec: 0x6eba,
    0xf9ed: 0x541d,
    0xf9ee: 0x71d0,
    0xf9ef: 0x7498,
    0xf9f0: 0x85fa,
    0xf9f1: 0x96a3,
    0xf9f2: 0x9c57,
    0xf9f3: 0x9e9f,
    0xf9f4: 0x6797,
    0xf9f5: 0x6dcb,
    0xf9f6: 0x81e8,
    0xf9f7: 0x7acb,
    0xf9f8: 0x7b20,
    0xf9f9: 0x7c92,
    0xf9fa: 0x72c0,
    0xf9fb: 0x7099,
    0xf9fc: 0x8b58,
    0xf9fd: 0x4ec0,
    0xf9fe: 0x8336,
    0xf9ff: 0x523a,
    0xfa00: 0x5207,
    0xfa01: 0x5ea6,
    0xfa02: 0x62d3,
    0xfa03: 0x7cd6,
    0xfa04: 0x5b85,
    0xfa05: 0x6d1e,
    0xfa06: 0x66b4,
    0xfa07: 0x8f3b,
    0xfa08: 0x884c,
    0xfa09: 0x964d,
    0xfa0a: 0x898b,
    0xfa0b: 0x5ed3,
}

for log in inf_log:
    path, inf_result = log.split(":('")
    print(f'{hex(int(Path(path).stem))} {hex(ord(inf_result[0]))}')