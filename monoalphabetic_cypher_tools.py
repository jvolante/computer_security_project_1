from collections import Counter
import operator
import re
three_letter_words = re.compile(r"(\w{3})")

def replace_dict(string, d):
  pattern = re.compile('|'.join(d.keys()))
  result = pattern.sub(lambda x: d[x.group()], string)
  return result


def reverse_dict(dictionary):
  """
  Returns a new dictionary with keys that are the original dictionary's values and values
  that are the original dictionary's keys.
  :param dictionary:
  :return: dictionary
  """
  result = dict()
  for k, v in dictionary.iteritems():
    if v in result:
      raise ValueError("Values in the dicitonary must be unique")
    else:
      result[v] = k

  return result


def get_key_with_value(dictionary, value):
  """
  returns the first key found with the specified value.
  if dictionary is not an ordereddict then this function is not stable
  :param dictionary: dictionary containing key/value pairs
  :param value: value to search for
  :return: key with specified value
  """
  for k, v in dictionary.iteritems():
    if value == v:
      return k


def get_sub_dict_for_values(d, values):
  """
  Gets the key/value pairs with the specified values.
  :param d: dictionary
  :param values: values
  :return: dictionary
  """
  result = dict()
  for k, v in d.iteritems():
    if v in values:
      result.update({k, v})
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

def get_key_with_largest_value(dictionary):
  """
  Returns the key with the highest magnitude value.
  """
  return get_largest_key_value_pair(dictionary)[0]

class cypher_decriptor:

  def __init__(self, calibrate_file, language="en_US"):
    self.calibrate_file = calibrate_file
    with open(calibrate_file) as f:
      text = f.read().lower()

    counts = Counter([character for character in text if ord('a') <= ord(character) <= ord('z')])
    total_chars = sum([counts[character] for character in counts])
    self.calibrated_character_freq = {character : counts[character] / float(total_chars) for character in counts}
    self.calibrated_char_after_freq = {chr(ch) : get_re_result_freq(text, re.compile(chr(ch) + r"(\w)"), groupnum=1) for ch in range(ord('a'), ord('z') + 1)}
    self.calibrated_char_before_freq = {chr(ch) : get_re_result_freq(text, re.compile(r"(\w)" + chr(ch)), groupnum=1) for ch in range(ord('a'), ord('z') + 1)}
    self.calibrated_three_letter_words_freq = get_re_result_freq(text, three_letter_words, groupnum=1)


  def guess_initial_mappings(self, input_file):
    """
    Starts decrypting the cyphertext file by providing an initial mapping of the characters.
    :param input_file: File containing cyphertext to decrypt
    :return:
    """
    decoded_letters = set()
    with open(input_file) as f:
      self.cypher_text = f.read().lower()

    counts = Counter([character for character in self.cypher_text if ord('a') <= ord(character) <= ord('z')])
    total_chars = sum([counts[character] for character in counts])

    # get frequency dictionaries that correspond to
    self.cyphertext_character_freq = {character : counts[character] / float(total_chars) for character in counts}
    self.cyphertext_char_after_freq = {chr(ch) : get_re_result_freq(self.cypher_text, re.compile(chr(ch) + r"(\w)"), groupnum=1) for ch in range(ord('a'), ord('z') + 1)}
    self.cyphertext_char_before_freq = {chr(ch) : get_re_result_freq(self.cypher_text, re.compile(r"(\w)" + chr(ch)), groupnum=1) for ch in range(ord('a'), ord('z') + 1)}
    self.cyphertext_three_letter_words_freq = get_re_result_freq(self.cypher_text, three_letter_words, groupnum=1)

    self.mapping = self.__initial_map_frequencies()

    # assume e is mapped correctly
    decoded_letters.add('e')

    # the character that preceeds e is the same the majority of the time, map accordingly
    self.__map_preceding_letter('e')

    # h is now probably mapped correctly
    decoded_letters.add('h')

    # the character that preceeds h is the same the majority of the time, map accordingly
    self.__map_preceding_letter('h')

    # assume t is now mapped correctly
    decoded_letters.add('t')

    # the character that preceeds t is the same the majority of the time, map accordingly
    self.__map_preceding_letter('t')

    #assume s is now mapped correctly
    decoded_letters.add('s')

    # now that we have the letters t h and e out of the way that knocks out the word "the". The three letter groups
    # "and" and "you" trade blows as the second most common three letter group, but we can use the frequency of the
    # first letter of the group to differentiate them. "tha" as in "that" ends up being the third most common three
    # letter grouping in many cases, but since we know the letters t and h we can throw it out.
    reverse_mapping = reverse_dict(self.mapping)
    tmp_three_letter_words = self.cyphertext_three_letter_words_freq.copy()
    del tmp_three_letter_words[replace_dict("the", reverse_mapping)]

    # try to throw out other three letter groups such as "tha" and "thi" (that and this)
    candidates = list()
    while len(candidates) < 2:
      key = get_key_with_largest_value(tmp_three_letter_words)

      for c in replace_dict(key, self.mapping):
        if c in decoded_letters:
          continue

      candidates.append(key)

    # the key where the first letter is more common is probably the word and and the other is probably the word you
    if self.cyphertext_character_freq[candidates[0][0]] > self.cyphertext_character_freq[candidates[1][0]]:
      and_letters = candidates[0]
      you_letters = candidates[1]
    else:
      and_letters = candidates[1]
      you_letters = candidates[0]

    self.swap_mapping(and_letters[0], 'a')
    self.swap_mapping(and_letters[1], 'n')
    self.swap_mapping(and_letters[2], 'd')

    self.swap_mapping(you_letters[0], 'y')
    self.swap_mapping(you_letters[1], 'o')
    self.swap_mapping(you_letters[2], 'u')

    decoded_letters |= set('andyou')

    # delete this because it is no longer up to date and we don't want to use it by accident
    del reverse_mapping

    # we can find q by finding the letter that has "u" after it most of the time
    u_letter = you_letters[2]

    candidates = dict()

    for k, v in self.cyphertext_char_after_freq.iteritems():
      if self.mapping[k] in decoded_letters:
        continue
      elif get_key_with_largest_value(v) == u_letter:
        candidates[k] = v[u_letter]

    q_letter = get_key_with_largest_value(candidates)

    self.swap_mapping(q_letter, 'q')

    decoded_letters.add('q')


  def __map_preceding_letter(self, letter):
    plaintext_before_e = get_largest_key_value_pair(self.calibrated_char_before_freq[letter])
    cyphertext_before_e = get_largest_key_value_pair(self.cyphertext_char_before_freq[get_key_with_value(self.mapping, letter)])

    self.swap_mapping(cyphertext_before_e[0], plaintext_before_e[0])

  def decrypt(self):
    """
    applies the mapping dict to the cyphertext and returns the result
    :return: decrypted cyphertext, str
    """
    return replace_dict(self.cypher_text, self.mapping)


  def swap_mapping(self, key, value):
    """
    swaps the values of key and the key that has the specified value
    :param key: cyphertext letter to make new mapping for
    :param value: new character to be mapped to cyphertext letter
    :return: None.
    """
    tmp = self.mapping[key]

    for k, v in self.mapping.iteritems():
      if value == v:
        self.mapping[k] = tmp
        self.mapping[key] = value
        break


  def get_mapping(self):
    """
    gets the character to character mapping currently being used by the object
    :return: dict containing character to charcter mapping for characters a-z
    """
    return self.mapping


  def set_mapping(self, mapping):
    """
    changes the mapping dict being used by the object completely
    :param mapping: new char to char mapping dict for ALL characters a-z
    :return: None
    """
    self.mapping = {x.lower() : y.lower() for x, y in mapping.iteritems()}


  def update_mapping(self, update_dict):
    """
    updates the mapping dict for new values
    :param update_dict: dict containing character to character mapping characters between a and z
    :return: None
    """
    self.mapping.update({x.lower(): y.lower() for x, y in update_dict.iteritems()})


  def get_calibrated_frequency_dict(self):
    """
    returns the letter frequency dictionary for the calibration file
    :return: dict containing letter frequency table
    """
    return self.calibrated_character_freq


  def get_input_frequency_dict(self):
    """
    returns the letter frequency dictionary for the cyphertext file
    :return: dict containing letter frequency table
    """
    return self.cyphertext_character_freq


  def __initial_map_frequencies(self):
    """
    Pairs letters in the calibration file to letters in the cyphertext file by ordering them from greatest to least
    Cyphertext letter maps to plaintext letter in the returned dictionary.
    frequency and matching the pairs.
    :param input_freq:
    :return: dictionary containing cyphertext letter to plaintext letter mapping.
    """
    cypher_freq_most_to_least = sorted(self.cyphertext_character_freq.items(), key=lambda x: -x[1])
    cal_freq_most_to_least = sorted(self.calibrated_character_freq.items(), key=lambda x: -x[1])
    return {input_char[0]:output_char[0] for input_char, output_char in zip(cypher_freq_most_to_least, cal_freq_most_to_least)}