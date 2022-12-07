label_file = "rec_banila_train.txt"
exclude_chr_set = {'\\', '²', '³', '¹', 'ʱ', 'ʲ', 'ʳ', 'ʴ', 'ʵ', 'ʶ', 'ʼ', '˅', 'ˇ', 'ː', '˝', '˪', '˯', 
'˹', '˻',  '́', '̇', '͠', 'ʹ', 'Ϛ',  'ᄒ', 'ᆫ', '‣', '⁃', '⁋', '₃', '⃝', '⃞', '↳', '⇀', '⇄', '⇐', '⇓', '⇛', 
'⇦', '⇨', '⇩', '∎', '∘', '≼', '≽', '⋅', '⋗', '⋯', '⌌', '⌎', '⌜', '⌟', 
'⓵', '⓶', '⓷', '─', '━', '│', '┃', '┌', '┍', '┏', '┓', '└', '┕', '┗', '┛', '├', '┠', '┣', '┤', '┨', '┬', 
'┯', '┷', '┼', '╂', '╺', '▄', '▢', '▮', '▴', '▵', '▸', '▹', '▻', '◉', '◌', '◪', '◯', '◼', '◽', '◾', 
'☐', '☑', '⚪', '⚫', '⚬', 
# Dingbats 0x2700 <= i <= 0x27BF
'✍', '✐', '✔', '✕', '✥', '✳', '✻', '❊', '❋', '❖', '❙', '❚', '❯', 
'❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿', '➀', '➁', '➂', '➃', '➄', '➅', '➆', '➇', '➈', '➉', 
'➊', '➋', '➌', '➍', '➎', '➏', '➐', '➑', 
'➔', '➙', '➜', '➠', '➡', '➢', '➣', '➤', '➥', '➩', '➪', '➭', '➮', '➯', '➲',
# Miscellaneous Mathematical Symbols-A 0x27C0 <= i <= 0x27EF
 '⟦', '⟧', 
# Supplemental Arrows-A Range: 27F0–27FF
 '⟶', '⟹', '⟺', 
# Miscellaneous Mathematical Symbols-BRange: 2980–29FF
'⦁', '⧠', 
# Miscellaneous Symbols and Arrows Range: 2B00–2BFF
'⬞', '⭕', 
# Supplemental Punctuation Range: 2E00–2E7F
'⸢',
# CJK Symbols and Punctuation Range: 3000–303F
'〇', '〖', '〗', '〜', '〮', 
# Halfwidth and Fullwidth Forms Range: FF00–FFEF
'￭'}
dingbat = {'❍', '❏', '❐', '❑', '❒'}


filtered_dict = dict()
with open(label_file, 'r', encoding='utf-8') as label_file:
    for line in label_file:
        if line[-1] == '\n':
            line = line[:-1]
        splited_line = line.split('\t')
        # print(line, splited_line)
        if splited_line[-1] == '':
            continue
        path, gt = splited_line
        # print(f"path: +{path}+, gt: +{gt}+")
        cropped, pdf_name, file_name = path.split('/')
        pdf_set = filtered_dict.get(gt, set())
        pdf_set.add(pdf_name)
        # print(filtered_dict, pdf_set)
        filtered_dict[gt] = pdf_set
for key in sorted(filtered_dict.keys()):
    print(key,":")
    print(f"'{key}', # {list(filtered_dict[key])}")