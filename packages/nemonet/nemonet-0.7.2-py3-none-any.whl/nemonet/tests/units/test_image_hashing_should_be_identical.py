from PIL import Image
import imagehash

import unittest


class ReporterTestCase(unittest.TestCase):

    false_screen_shot = "false_screenshot_reden.png"
    true_screen_shot = "screenshot_reden.png"
    base_screen_shot = "base_line_screenshot_reden.png"

    hash_method_dict = {
        'dhash': imagehash.dhash,
        'phash': imagehash.phash,
        'ahash': imagehash.average_hash,
        'crhash' : imagehash.crop_resistant_hash,
        'whash' : imagehash.whash,
        'dvhash' : imagehash.dhash_vertical,
    }

    def test_should_be_indentical_with_dhash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                       name_executing_method=self._testMethodName, hash_method="dhash")

    def test_should_be_indentical_with_phash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                       name_executing_method=self._testMethodName, hash_method="phash")

    def test_should_be_indentical_with_ahash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                       name_executing_method=self._testMethodName, hash_method="ahash")

    def test_should_be_indentical_with_crhash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                               name_executing_method=self._testMethodName, hash_method="crhash")

    def test_should_be_indentical_with_whash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                               name_executing_method=self._testMethodName, hash_method="whash")

    def test_should_be_indentical_with_dvhash(self):
        self.use_image_hashing(first=self.base_screen_shot, second=self.true_screen_shot,
                               name_executing_method=self._testMethodName, hash_method="dvhash")


    def use_image_hashing(self, first, second, name_executing_method="", hash_method="dhash"):
        hash_base_line = self.hash_method_dict[hash_method](Image.open(first))
        hash_compare_base_line = self.hash_method_dict[hash_method](Image.open(second))
        print("%s %s" % (name_executing_method, hash_base_line == hash_compare_base_line))
        print(hash_base_line - hash_compare_base_line)


if __name__ == '__main__':
    unittest.main()