from collections import Counter
import operator
import re

char_after_th = re.compile(r"th(\w)", re.IGNORECASE)
char_after_t = re.compile(r"t(\w)", re.IGNORECASE)
char_before_e = re.compile(r"(\w)e", re.IGNORECASE)
char_before_h = re.compile(r"(\w)h", re.IGNORECASE)
three_letter_words = re.compile(r"(\w{3})")

def replace_dict(string, d):
  pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
  result = pattern.sub(lambda x: d[x.group()], string)
  return result


def get_re_result_freq(text, rex, groupnum=0):
  """
  computes the frequency of a result from a regulare expression in a text.
  :param text: text to check against
  :param rex: regular expression
  :param groupnum: the number of the group to use as the key in the frequency dictionary, can also be group name if named groups are used.
  :return: dict containing key value pairs of str, float
  """
  counts = Counter([match.group(groupnum) for match in rex.finditer(text)])
  total = sum([counts[character] for character in counts])
  return {character: counts[character] / float(total) for character in counts}

def get_largest_key_value_pair(dictionary):
  """
  Returns the key value pair where value has the highest magnitude
  :param dictionary: dict containing keyvalue pairs where key is comparable
  :return: tuple containing key value pair with largest magnitude value
  """
  return max(dictionary.iteritems(), key=operator.itemgetter(1))


class cypher_decriptor:

  def __init__(self, calibrate_file, language="en_US"):
    self.calibrate_file = calibrate_file
    with open(calibrate_file) as f:
      text = f.read().lower()

    counts = Counter([character for character in text if ord('a') <= ord(character) <= ord('z')])
    total_chars = sum([counts[character] for character in counts])
    self.calibrated_character_freq = {character : total_chars / counts[character] for character in counts}
    self.calibrated_char_after_t_freq = get_re_result_freq(text, char_after_t, groupnum=1)
    self.calibrated_char_before_e_freq = get_re_result_freq(text, char_before_e, groupnum=1)
    self.calibrated_char_before_h_freq = get_re_result_freq(text, char_before_h, groupnum=1)
    self.calibrated_three_letter_words_freq = get_re_result_freq(text, three_letter_words, groupnum=1)


  def decrypt(self, input_file):
    """
    Starts decrypting the cyphertext file by providing an initial mapping of the characters.
    :param input_file: File containing cyphertext to decrypt
    :return:
    """
    with open(input_file) as f:
      self.cypher_text = f.read().lower()

    counts = Counter([character for character in self.cypher_text if ord('a') <= ord(character) <= ord('z')])
    total_chars = sum([counts[character] for character in counts])
    input_character_freq = {character : counts[character] / float(total_chars) for character in counts}

    self.mapping = self.__initial_map_frequencies(input_character_freq)

    initial_plaintext = replace_dict(self.cypher_text, self.mapping)

    char_before_e_freq = get_re_result_freq(initial_plaintext, char_before_e)



  def get_mapping(self):
    return self.mapping


  def set_mapping(self, mapping):
    self.mapping = mapping



  def __initial_map_frequencies(self, input_freq):
    input_freq_most_to_least = sorted(input_freq.items(), key=lambda x: -x[1])
    cal_freq_most_to_least = sorted(input_freq.items(), key=lambda x: -x[1])
    return {input_char[0]:output_char[0] for input_char, output_char in zip(input_freq_most_to_least, cal_freq_most_to_least)}