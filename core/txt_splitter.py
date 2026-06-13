
def split_txt(txt_path, max_chars=8000):
    with open(txt_path,"r",encoding="utf-8") as f:
        text = f.read()

    parts = [text[i:i+max_chars] for i in range(0,len(text),max_chars)]

    for i,p in enumerate(parts):
        with open(txt_path.replace(".txt", f"_part{i+1}.txt"),"w",encoding="utf-8") as f:
            f.write(p)
