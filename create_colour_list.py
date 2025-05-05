from asciimatics.screen import Screen

#INPUT: str, list, int, int list
#RETURN: list
#PURPOSE: Creates a list of colour values for every letter in a piece of text, allowing us to colour each letter differently 
def create_colour_list(text, words_to_change: list, base_text_colour: int, background_color:int, highlight_text_colour: list):
    '''
    Creates list which allows for multi-coloured printing
    '''
    colour_list = [(base_text_colour, Screen.A_NORMAL, background_color)] * len(text) # set up the list to be the right length, full of basic data

    # change the necessary values in that last with the custom data
    for word_index, word in enumerate(words_to_change):
        start = (text.find(word))
        length = len(word)
        for i in range(start, start + length): # start pos, end pos
            colour_list[i] = (highlight_text_colour[word_index], Screen.A_NORMAL, background_color)

    return colour_list