from asciimatics.screen import Screen

def create_colour_list(text, words_to_change: list, base_text_colour: int, background_color:int, highlight_text_colour: list):
    colour_list = [(base_text_colour, Screen.A_NORMAL, background_color)] * len(text)
    for word_index, word in enumerate(words_to_change):
        start = (text.find(word))
        length = len(word)
        for i in range(start, start + length): # start pos, end pos
            colour_list[i] = (highlight_text_colour[word_index], Screen.A_NORMAL, background_color)
    return colour_list